/* Conexión de Mi Ruta con Firebase: cuentas, aprobación, avance en la nube,
   panel de gestión y constancias verificables.

   Expone window.Nube, que usa assets/app.js. Si MIRUTA_CONFIG.firebase es null,
   Nube.habilitada es false y la plataforma sigue en modo local.

   Colecciones de Firestore:
     usuarios/{uid}     nombre, correo, comunidad, rol, estado, cursos, solicitudes
     avance/{uid}       datos: { "hechas:<curso>": [...], "eval:<curso>:<id>": {...} }
     notas/{uid}        datos: { "bitacora:<clase>": "...", "plantilla:<clase>": {...}, ... } (privado)
     constancias/{folio} datos de la constancia emitida (lectura pública por folio)
     tarjetas/{id}      imagen de la tarjeta de una formación en la portada (lectura pública; edita un admin)
*/

const CONFIG = window.MIRUTA_CONFIG || {};
const habilitada = !!(CONFIG.firebase && CONFIG.firebase.apiKey);
const minus = (e) => String(e || "").trim().toLowerCase();
const ADMINS = (CONFIG.administradores || []).map(minus);

let fb = null, auth = null, db = null;
let usuario = null;   // Firebase Auth
let cuenta = null;    // documento usuarios/{uid}
let status = habilitada ? "cargando" : "local"; // local | cargando | invitado | pendiente | activo | pausado | error
let ultimoError = "";
const oyentes = [];
const avisar = () => oyentes.forEach((f) => { try { f(); } catch (e) { console.warn(e); } });

// Claves locales que se sincronizan y a qué documento van.
const CLAVES_AVANCE = /^(hechas|eval):/;
const CLAVES_NOTAS = /^(bitacora|plantilla|tareas):/;

function estado() {
  const activo = status === "activo" && cuenta;
  return {
    habilitada, status, error: ultimoError, usuario, cuenta,
    activo: !!activo,
    esRelator: !!(activo && (cuenta.rol === "relator" || cuenta.rol === "admin")),
    esAdmin: !!(activo && cuenta.rol === "admin"),
  };
}

function conTiempo(p, ms = 10000) {
  return Promise.race([p, new Promise((_, no) => setTimeout(() => no(new Error("Sin respuesta del servidor")), ms))]);
}

async function iniciar() {
  if (!habilitada) return;
  try {
    fb = await import("./vendor/firebase.mjs");
    const app = fb.initializeApp(CONFIG.firebase);
    auth = fb.getAuth(app);
    try {
      db = fb.initializeFirestore(app, { localCache: fb.persistentLocalCache({ tabManager: fb.persistentMultipleTabManager() }) });
    } catch (e) {
      db = fb.initializeFirestore(app, {});
    }
    try { await fb.getRedirectResult(auth); } catch (e) { ultimoError = traducir(e); }
    await new Promise((listo) => {
      let primera = true;
      fb.onAuthStateChanged(auth, async (u) => {
        await alCambiarUsuario(u);
        if (primera) { primera = false; listo(); } else avisar();
      });
    });
  } catch (e) {
    console.warn("Firebase:", e);
    status = "error"; ultimoError = e.message || String(e);
  }
}

async function alCambiarUsuario(u) {
  usuario = u; cuenta = null;
  if (!u) { status = "invitado"; return; }
  try {
    const ref = fb.doc(db, "usuarios", u.uid);
    let snap = await conTiempo(fb.getDoc(ref));
    if (!snap.exists()) {
      const correo = minus(u.email);
      const esAdmin = ADMINS.includes(correo) && (u.emailVerified || (u.providerData || []).some((p) => p.providerId === "google.com"));
      const pendiente = registroPendiente;
      registroPendiente = null;
      await conTiempo(fb.setDoc(ref, {
        nombre: (pendiente && pendiente.nombre) || u.displayName || correo,
        correo: u.email,
        comunidad: (pendiente && pendiente.comunidad) || "",
        rol: esAdmin ? "admin" : "participante",
        estado: esAdmin ? "activo" : "pendiente",
        cursos: [],
        solicitudes: [],
        creado: fb.serverTimestamp(),
        ultimoIngreso: fb.serverTimestamp(),
      }));
      snap = await conTiempo(fb.getDoc(ref));
    }
    cuenta = { uid: u.uid, ...snap.data() };
    status = cuenta.estado === "activo" ? "activo" : (cuenta.estado === "pausado" ? "pausado" : "pendiente");
    ultimoError = "";
    if (status === "activo") {
      try { await traerDatos(); } catch (e) { console.warn("Avance:", e); }
      fb.updateDoc(ref, { ultimoIngreso: fb.serverTimestamp() }).catch(() => {});
    }
  } catch (e) {
    console.warn("Cuenta:", e);
    status = "error"; ultimoError = traducir(e);
  }
}

/* ---------- ingreso ---------- */

let registroPendiente = null;

function traducir(e) {
  const c = (e && e.code) || "";
  const m = {
    "auth/invalid-credential": "El correo o la contraseña no son correctos.",
    "auth/wrong-password": "La contraseña no es correcta.",
    "auth/user-not-found": "No hay una cuenta con ese correo.",
    "auth/email-already-in-use": "Ya existe una cuenta con ese correo. Prueba ingresar o recuperar tu contraseña.",
    "auth/weak-password": "La contraseña debe tener al menos 6 caracteres.",
    "auth/invalid-email": "El correo no es válido.",
    "auth/popup-closed-by-user": "Se cerró la ventana de Google antes de terminar.",
    "auth/too-many-requests": "Demasiados intentos. Espera unos minutos y vuelve a intentar.",
    "auth/network-request-failed": "No hay conexión. Revisa tu internet.",
    "permission-denied": "No tienes permiso para hacer esto.",
  };
  return m[c] || (e && e.message) || String(e);
}

async function ingresarGoogle() {
  const proveedor = new fb.GoogleAuthProvider();
  proveedor.setCustomParameters({ prompt: "select_account" });
  try {
    await fb.signInWithPopup(auth, proveedor);
  } catch (e) {
    if (e && (e.code === "auth/popup-blocked" || e.code === "auth/operation-not-supported-in-this-environment")) {
      await fb.signInWithRedirect(auth, proveedor);
      return;
    }
    throw new Error(traducir(e));
  }
}

async function ingresarCorreo(correo, clave) {
  try { await fb.signInWithEmailAndPassword(auth, correo.trim(), clave); }
  catch (e) { throw new Error(traducir(e)); }
}

async function registrar({ nombre, comunidad, correo, clave }) {
  registroPendiente = { nombre: nombre.trim(), comunidad: comunidad.trim() };
  try {
    const cred = await fb.createUserWithEmailAndPassword(auth, correo.trim(), clave);
    try { await fb.updateProfile(cred.user, { displayName: nombre.trim() }); } catch (e) { /* no es grave */ }
    try { await fb.sendEmailVerification(cred.user); } catch (e) { /* no es grave */ }
  } catch (e) {
    registroPendiente = null;
    throw new Error(traducir(e));
  }
}

async function recuperarClave(correo) {
  try { await fb.sendPasswordResetEmail(auth, correo.trim()); }
  catch (e) { throw new Error(traducir(e)); }
}

async function salir() { await fb.signOut(auth); }

async function actualizarPerfil({ nombre, comunidad }) {
  await fb.updateDoc(fb.doc(db, "usuarios", usuario.uid), { nombre, comunidad });
  cuenta = { ...cuenta, nombre, comunidad };
  avisar();
}

async function solicitarCurso(cursoId) {
  const ref = fb.doc(db, "usuarios", usuario.uid);
  try {
    await conTiempo(fb.updateDoc(ref, { solicitudes: fb.arrayUnion(cursoId) }));
  } catch (e) {
    throw new Error("No se pudo enviar la solicitud (" + traducir(e) + "). Avísale a tu relator.");
  }
  // Se relee la cuenta desde el servidor para confirmar que la solicitud quedó registrada.
  const snap = await conTiempo(fb.getDoc(ref));
  cuenta = { uid: usuario.uid, ...snap.data() };
  if ((cuenta.solicitudes || []).indexOf(cursoId) < 0) throw new Error("La solicitud no quedó registrada. Vuelve a intentarlo o avísale a tu relator.");
  avisar();
}

/* ---------- avance y notas ---------- */

const PREFIJO = "agp:";
let cola = {}, temporizador = null;

function claveLocal(k) { return PREFIJO + (usuario && status === "activo" ? "u:" + usuario.uid + ":" : "") + k; }

async function traerDatos() {
  const [av, no] = await Promise.all([
    conTiempo(fb.getDoc(fb.doc(db, "avance", usuario.uid))),
    conTiempo(fb.getDoc(fb.doc(db, "notas", usuario.uid))),
  ]);
  const datos = Object.assign({}, av.exists() ? av.data().datos : {}, no.exists() ? no.data().datos : {});
  // Primer ingreso: el avance que la persona tenía en este navegador, sin cuenta, pasa a su cuenta.
  if (!av.exists() && !no.exists()) {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith(PREFIJO) || k.startsWith(PREFIJO + "u:")) continue;
      const corta = k.slice(PREFIJO.length);
      if (CLAVES_AVANCE.test(corta) || CLAVES_NOTAS.test(corta)) {
        try { datos[corta] = JSON.parse(localStorage.getItem(k)); cola[corta] = datos[corta]; } catch (e) { /* dato dañado */ }
      }
    }
    if (Object.keys(cola).length) setTimeout(subir, 500);
  }
  Object.keys(datos).forEach((k) => {
    try { localStorage.setItem(PREFIJO + "u:" + usuario.uid + ":" + k, JSON.stringify(datos[k])); } catch (e) { /* sin espacio */ }
  });
}

function guardado(clave, valor) {
  if (status !== "activo") return;
  if (!CLAVES_AVANCE.test(clave) && !CLAVES_NOTAS.test(clave)) return;
  cola[clave] = valor;
  clearTimeout(temporizador);
  temporizador = setTimeout(subir, 1200);
}

async function subir() {
  const pendientes = cola; cola = {};
  const avance = {}, notas = {};
  Object.keys(pendientes).forEach((k) => { (CLAVES_AVANCE.test(k) ? avance : notas)[k] = pendientes[k]; });
  const tareas = [];
  if (Object.keys(avance).length) tareas.push(fb.setDoc(fb.doc(db, "avance", usuario.uid), { datos: avance, actualizado: fb.serverTimestamp() }, { merge: true }));
  if (Object.keys(notas).length) tareas.push(fb.setDoc(fb.doc(db, "notas", usuario.uid), { datos: notas }, { merge: true }));
  try { await Promise.all(tareas); }
  catch (e) { console.warn("No se pudo guardar en la nube:", e); Object.assign(cola, pendientes); }
}

window.addEventListener("pagehide", () => { if (Object.keys(cola).length) subir(); });

/* ---------- imágenes de las tarjetas de la portada ---------- */

async function leerTarjetas() {
  if (!habilitada || !db) return {};
  const snap = await conTiempo(fb.getDocs(fb.collection(db, "tarjetas")));
  const r = {};
  snap.docs.forEach((d) => {
    const x = d.data();
    if (x.imagen) r[d.id] = x.imagen;
    if (typeof x.velo === "number") r[d.id + ":velo"] = x.velo;
  });
  return r;
}

async function guardarTarjeta(id, imagen) {
  await conTiempo(fb.setDoc(fb.doc(db, "tarjetas", id), { imagen: imagen || "", actualizado: fb.serverTimestamp(), por: usuario.uid }, { merge: true }));
}

// Opacidad del velo sobre la imagen (0 a 0,9).
async function guardarVelo(id, velo) {
  await conTiempo(fb.setDoc(fb.doc(db, "tarjetas", id), { velo, actualizado: fb.serverTimestamp(), por: usuario.uid }, { merge: true }));
}

/* ---------- gestión (relatores y administradores) ---------- */

async function listarUsuarios() {
  const snap = await conTiempo(fb.getDocs(fb.collection(db, "usuarios")));
  return snap.docs.map((d) => ({ uid: d.id, ...d.data() }));
}

async function actualizarUsuario(uid, cambios) {
  await fb.updateDoc(fb.doc(db, "usuarios", uid), cambios);
}

async function avanceDe(uid) {
  const s = await conTiempo(fb.getDoc(fb.doc(db, "avance", uid)));
  return s.exists() ? (s.data().datos || {}) : {};
}

function nuevoFolio() {
  const letras = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let r = "";
  const azar = crypto.getRandomValues(new Uint32Array(6));
  for (let i = 0; i < 6; i++) r += letras[azar[i] % letras.length];
  return "MR-" + new Date().getFullYear() + "-" + r;
}

async function emitirConstancia(datos) {
  const folio = nuevoFolio();
  await fb.setDoc(fb.doc(db, "constancias", folio), {
    ...datos, folio, emitidaPor: usuario.uid, firmante: cuenta.nombre, emitida: fb.serverTimestamp(),
  });
  return folio;
}

async function leerConstancia(folio) {
  const s = await conTiempo(fb.getDoc(fb.doc(db, "constancias", folio)));
  return s.exists() ? s.data() : null;
}

async function constanciasDe(uid) {
  const q = fb.query(fb.collection(db, "constancias"), fb.where("uid", "==", uid));
  const s = await conTiempo(fb.getDocs(q));
  return s.docs.map((d) => d.data());
}

async function todasLasConstancias() {
  const s = await conTiempo(fb.getDocs(fb.collection(db, "constancias")));
  return s.docs.map((d) => d.data());
}

window.Nube = {
  habilitada,
  listo: iniciar(),
  estado,
  alCambiar: (f) => oyentes.push(f),
  claveLocal,
  guardado,
  ingresarGoogle: (...a) => ingresarGoogle(...a),
  ingresarCorreo,
  registrar,
  recuperarClave,
  salir,
  actualizarPerfil,
  solicitarCurso,
  leerTarjetas,
  guardarTarjeta,
  guardarVelo,
  listarUsuarios,
  actualizarUsuario,
  avanceDe,
  emitirConstancia,
  leerConstancia,
  constanciasDe,
  todasLasConstancias,
};
