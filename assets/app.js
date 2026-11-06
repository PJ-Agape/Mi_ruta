/* Mi Ruta: aula virtual estática.
   Rutas (hash):
     #/                         inicio
     #/curso/<id>               página del curso
     #/curso/<id>/programa      programa del curso
     #/curso/<id>/sesiones      calendario de sesiones en vivo
     #/clase/<id>/<claseId>     una clase
   Los avances se guardan en el almacenamiento local del navegador. */

(function () {
  "use strict";

  var app = document.getElementById("app");
  var sitio = null;
  var cursos = {};
  var ROMANOS = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

  function etiquetaModulo(m) { return m.etiqueta || "Módulo " + ROMANOS[m.numero]; }

  /* ---------- utilidades ---------- */

  // Nube: cuentas y sincronización (assets/nube.js). Sin configuración, modo local.
  var Nube = window.Nube || { habilitada: false, listo: Promise.resolve(), estado: function () { return { habilitada: false, status: "local" }; }, alCambiar: function () {} };
  function cuentaActual() { return Nube.estado(); }

  // Con cuentas activas, cada usuario tiene su propio espacio local, que se sincroniza con la nube.
  function claveLocal(clave) { return Nube.habilitada ? Nube.claveLocal(clave) : "agp:" + clave; }

  var almacen = {
    leer: function (clave, defecto) {
      try {
        var v = localStorage.getItem(claveLocal(clave));
        return v === null ? defecto : JSON.parse(v);
      } catch (e) { return defecto; }
    },
    guardar: function (clave, valor) {
      try { localStorage.setItem(claveLocal(clave), JSON.stringify(valor)); } catch (e) { /* sin almacenamiento */ }
      if (Nube.habilitada) Nube.guardado(clave, valor);
    }
  };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function pedir(url, tipo) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("No se pudo cargar " + url);
      return tipo === "texto" ? r.text() : r.json();
    });
  }

  function md(texto) {
    return window.marked ? window.marked.parse(texto, { gfm: true, breaks: false }) : "<pre>" + esc(texto) + "</pre>";
  }

  // «Mi Ruta» → «Mi <em>Ruta</em>»: la última palabra va en cursiva, como en el logo.
  function nombreConEstilo(nombre) {
    return esc(nombre).replace(/(\S+)$/, "<em>$1</em>");
  }

  var FIRMA = '<p class="firma">by <span class="ag-app" role="img" aria-label="agAPPe">ag<b>APP</b>e</span></p>';

  function modoRelator() {
    if (Nube.habilitada && !cuentaActual().esRelator) return false;
    return almacen.leer("modoRelator", false);
  }

  /* ---------- acceso a los cursos ---------- */

  // libre | ingresar | pendiente | pausado | solicitar | solicitado | error
  function esPropedeutico(c) { return !!(c && (c.propedeutico || (sitio && c.id === sitio.propedeutico))); }
  function acceso(curso) {
    if (!Nube.habilitada || esPropedeutico(curso)) return "libre";
    var e = cuentaActual();
    if (e.status === "invitado") return "ingresar";
    if (e.status === "pendiente") return "pendiente";
    if (e.status === "pausado") return "pausado";
    if (e.status !== "activo") return "error";
    if (e.esRelator) return "libre";
    var c = e.cuenta || {};
    if ((c.cursos || []).indexOf(curso.id) >= 0) return "libre";
    if ((c.solicitudes || []).indexOf(curso.id) >= 0) return "solicitado";
    return "solicitar";
  }

  function bloqueAcceso(curso, tipo) {
    var m = {
      ingresar: ["Ingresa para comenzar", "Crea tu cuenta o ingresa para inscribirte y guardar tu avance en todos tus dispositivos.", '<a class="boton principal" href="#/ingresar">Ingresar o crear cuenta</a>'],
      pendiente: ["Tu cuenta está en revisión", "Un relator o administrador debe aprobar tu cuenta. Mientras tanto, puedes solicitar la inscripción en este curso.", '<button class="boton principal" data-solicitar="' + esc(curso.id) + '">Solicitar inscripción</button>'],
      pausado: ["Tu cuenta está en pausa", "Conversa con tu relator o con la coordinación de Mi Ruta.", ""],
      solicitar: ["Inscríbete en este curso", "Al solicitar la inscripción, un relator la revisará y te habilitará el curso. Desde que te habiliten tendrás 1 semana para empezar y 2 meses para completar" + (curso.modulos && curso.modulos.length > 1 ? " cada módulo (contados desde que lo empiezas)" : " la formación") + "; si no, la inscripción se anula y se pierde el avance.", '<button class="boton principal" data-solicitar="' + esc(curso.id) + '">Solicitar inscripción</button>'],
      solicitado: ["Inscripción solicitada", "Tu solicitud está en revisión. Te habilitaremos el curso apenas sea aprobada.", ""],
      error: ["No pudimos verificar tu cuenta", "Revisa tu conexión y vuelve a intentar.", '<a class="boton" href="#/perfil">Ver mi cuenta</a>'],
    }[tipo];
    if (tipo === "pendiente" && (cuentaActual().cuenta.solicitudes || []).indexOf(curso.id) >= 0) {
      m = ["Tu cuenta está en revisión", "Ya solicitaste este curso. Te habilitaremos apenas un relator apruebe tu cuenta.", ""];
    }
    return '<div class="acceso"><h2>' + m[0] + "</h2><p>" + m[1] + "</p>" + (m[2] ? '<div class="botones">' + m[2] + "</div>" : "") + "</div>";
  }

  function activarSolicitudes() {
    app.querySelectorAll("[data-solicitar]").forEach(function (b) {
      b.addEventListener("click", function () {
        b.disabled = true;
        b.textContent = "Enviando…";
        Nube.solicitarCurso(b.getAttribute("data-solicitar")).then(ruta).catch(function (e) {
          b.disabled = false; b.textContent = "Solicitar inscripción"; alertaEn(b.parentNode, e.message);
        });
      });
    });
  }

  function alertaEn(nodo, texto) {
    var p = document.createElement("p");
    p.className = "aviso error";
    p.textContent = texto;
    nodo.appendChild(p);
  }

  function cargarSitio() {
    if (sitio) return Promise.resolve(sitio);
    return pedir("datos/sitio.json").then(function (s) {
      sitio = s;
      document.getElementById("marca-nombre").innerHTML = nombreConEstilo(s.nombre);
      return s;
    });
  }

  function cargarCurso(id) {
    if (cursos[id]) return Promise.resolve(cursos[id]);
    return Promise.all([pedir("datos/curso-" + id + ".json"), pedir("datos/indice-" + id + ".json")])
      .then(function (r) {
        var curso = r[0];
        curso.modulos = r[1].modulos;
        curso.clases = [];
        curso.modulos.forEach(function (m) {
          m.clases.forEach(function (c) { c.modulo = m; curso.clases.push(c); });
        });
        cursos[id] = curso;
        return curso;
      });
  }

  // El avance es uno solo para toda la plataforma: cada sesión tiene un identificador único,
  // así un módulo aprobado cuenta en todos los cursos que lo incluyen.
  // Se suman las listas antiguas por curso para no perder el avance previo.
  function hechas(cursoId) {
    var todo = almacen.leer("hechas:todo", []);
    var antiguo = cursoId ? almacen.leer("hechas:" + cursoId, []) : [];
    return antiguo.length ? todo.concat(antiguo.filter(function (x) { return todo.indexOf(x) < 0; })) : todo;
  }

  // Un módulo con requisitos queda bloqueado para el participante hasta completar
  // todas las clases de los módulos requeridos. En vista relator se ve todo.
  function moduloBloqueado(curso, m) {
    if (!m.requiere || !m.requiere.length || modoRelator()) return null;
    var h = hechas(curso.id);
    if (moduloCompleto(m, h)) return null;
    var faltan = m.requiere.map(function (id) {
      return curso.modulos.filter(function (x) { return x.id === id; })[0];
    }).filter(function (req) {
      return req && req.clases.some(function (cl) { return h.indexOf(cl.id) < 0; });
    });
    return faltan.length ? faltan : null;
  }

  function marcarHecha(cursoId, claseId, valor) {
    var lista = almacen.leer("hechas:todo", []).filter(function (x) { return x !== claseId; });
    if (valor) lista.push(claseId);
    almacen.guardar("hechas:todo", lista);
    // En cursos de varios módulos, el plazo de 2 meses de cada módulo corre desde su primera sesión.
    var c = cursos[cursoId];
    if (valor && c && c.modulos.length > 1) {
      var m = c.clases.filter(function (cl) { return cl.id === claseId; }).map(function (cl) { return cl.modulo; })[0];
      if (m && !almacen.leer("plazo:" + cursoId + ":" + m.id, null)) almacen.guardar("plazo:" + cursoId + ":" + m.id, new Date().toISOString());
    }
  }

  // Un curso se completa con todos sus módulos obligatorios y la cantidad de optativos
  // que pide (elige); de los optativos se cuentan los más avanzados.
  function progresoCon(curso, h) {
    var hechasDe = function (m) { return m.clases.filter(function (c) { return h.indexOf(c.id) >= 0; }).length; };
    var obl = curso.modulos.filter(function (m) { return m.tipo !== "optativo"; });
    var opt = curso.modulos.filter(function (m) { return m.tipo === "optativo"; });
    var n = 0, total = 0;
    obl.forEach(function (m) { n += hechasDe(m); total += m.clases.length; });
    var elige = Math.min(curso.elige || 0, opt.length);
    if (elige) {
      var tam = opt[0].clases.length;
      opt.map(hechasDe).sort(function (a, b) { return b - a; }).slice(0, elige).forEach(function (x) { n += x; });
      total += elige * tam;
    }
    return { hechas: n, total: total, pct: total ? Math.round(100 * n / total) : 0 };
  }
  function progreso(curso) { return progresoCon(curso, hechas(curso.id)); }
  function moduloCompleto(m, h) { return m.clases.every(function (c) { return h.indexOf(c.id) >= 0; }); }

  /* ---------- plazos: 1 semana para empezar, 2 meses para completar ---------- */
  // Formaciones de un módulo: 2 meses desde la inscripción. Cursos de varios módulos: 2 meses por módulo,
  // desde que la persona empieza ese módulo. Quienes ya estaban inscritos al entrar la regla cuentan desde esa fecha.
  var REGLA_DESDE = "2026-11-06T12:00:00-03:00";
  var DIA = 86400000, SEMANA = 7 * DIA;
  function masMeses(iso, n) { var d = new Date(iso); d.setMonth(d.getMonth() + n); return d.toISOString(); }
  function maxIso(a, b) { return !a ? b : !b ? a : (a > b ? a : b); }
  function aplicaPlazos(c) {
    var e = cuentaActual();
    return !!(Nube.habilitada && e.activo && !e.esRelator && c && !esPropedeutico(c) && (e.cuenta.cursos || []).indexOf(c.id) >= 0);
  }
  function fechaInscripcion(c) {
    var ins = (cuentaActual().cuenta.inscripciones || {})[c.id];
    return maxIso(ins, new Date(REGLA_DESDE).toISOString());
  }
  // Estado de plazos de una formación para la persona: «empezar», «completo», o vencimientos por módulo.
  function plazosDe(c) {
    if (!aplicaPlazos(c)) return null;
    var h = hechas(c.id), ins = fechaInscripcion(c);
    var p = progresoCon(c, h);
    if (p.total && p.hechas >= p.total) return { estado: "completo" };
    var empezado = c.clases.some(function (cl) { return h.indexOf(cl.id) >= 0; });
    // Si un módulo venció y se reinició, la semana para (re)comenzar corre desde ese reinicio.
    if (!empezado) { ins = maxIso(ins, almacen.leer("plazo:" + c.id + ":reinicio", null)); return { estado: "empezar", limite: new Date(new Date(ins).getTime() + SEMANA).toISOString(), inscripcion: ins }; }
    if (c.modulos.length <= 1) return { estado: "curso", modulos: [{ m: c.modulos[0], inicio: ins, vence: masMeses(ins, 2) }] };
    var mods = [];
    c.modulos.forEach(function (m) {
      if (moduloCompleto(m, h)) return;
      var inicio = almacen.leer("plazo:" + c.id + ":" + m.id, null);
      var tiene = m.clases.some(function (cl) { return h.indexOf(cl.id) >= 0; });
      if (!inicio && tiene) inicio = maxIso(ins, new Date(REGLA_DESDE).toISOString());
      if (inicio) mods.push({ m: m, inicio: inicio, vence: masMeses(inicio, 2) });
    });
    return { estado: "curso", modulos: mods };
  }
  function cuentaRegresiva(iso) {
    var ms = new Date(iso).getTime() - Date.now();
    if (ms <= 0) return "unos instantes";
    var d = Math.floor(ms / DIA), hh = Math.floor(ms % DIA / 3600000), mm = Math.floor(ms % 3600000 / 60000);
    var partes = [];
    if (d) partes.push(d + (d === 1 ? " día" : " días"));
    if (hh || d) partes.push(hh + (hh === 1 ? " hora" : " horas"));
    partes.push(mm + (mm === 1 ? " minuto" : " minutos"));
    return partes.length > 1 ? partes.slice(0, -1).join(", ") + " y " + partes[partes.length - 1] : partes[0];
  }
  // Avisos de una formación: para empezar (desde el primer día) y de vencimiento (la última semana).
  function avisosPlazo(c, conTitulo) {
    var pl = plazosDe(c);
    if (!pl || pl.estado === "completo") return "";
    var nombre = conTitulo ? " <b>" + esc(c.titulo) + "</b>" : "";
    if (pl.estado === "empezar") {
      return '<div class="alerta-plazo empezar" data-hasta="' + esc(pl.limite) + '"><b>Empieza a tiempo:</b> si no completas tu primera sesión' + (conTitulo ? " de" + nombre : "") +
        ' dentro de <span class="regresiva">' + cuentaRegresiva(pl.limite) + "</span>, se anulará tu inscripción.</div>";
    }
    return pl.modulos.filter(function (x) { return new Date(x.vence).getTime() - Date.now() <= SEMANA; }).map(function (x) {
      var esCurso = c.modulos.length <= 1;
      return '<div class="alerta-plazo" data-hasta="' + esc(x.vence) + '">' + (esCurso ? "Tu curso" + nombre : "El " + esc(etiquetaModulo(x.m).toLowerCase()) + " «" + esc(x.m.titulo) + "»" + (conTitulo ? " de" + nombre : "")) +
        ' quedará desactivado y perderás tu avance dentro de <span class="regresiva">' + cuentaRegresiva(x.vence) + "</span>.</div>";
    }).join("");
  }
  setInterval(function () {
    document.querySelectorAll(".alerta-plazo[data-hasta] .regresiva").forEach(function (s) {
      s.textContent = cuentaRegresiva(s.parentNode.getAttribute("data-hasta"));
    });
  }, 30000);

  // Borra el avance de las sesiones indicadas (y sus evaluaciones).
  function borrarAvance(cursoId, clases) {
    var ids = clases.map(function (cl) { return cl.id; });
    almacen.guardar("hechas:todo", almacen.leer("hechas:todo", []).filter(function (x) { return ids.indexOf(x) < 0; }));
    if (almacen.leer("hechas:" + cursoId, null)) almacen.guardar("hechas:" + cursoId, almacen.leer("hechas:" + cursoId, []).filter(function (x) { return ids.indexOf(x) < 0; }));
    ids.forEach(function (id) { if (almacen.leer("eval:" + cursoId + ":" + id, null)) almacen.guardar("eval:" + cursoId + ":" + id, null); });
  }

  // Aplica las reglas al ingresar: anula inscripciones no iniciadas, desactiva formaciones vencidas
  // y reinicia módulos vencidos. Lo hace la propia cuenta; el panel «Acompañar» lo aplica también desde el equipo.
  var plazosRevisados = 0;
  function revisarPlazos() {
    var e = cuentaActual();
    if (!Nube.habilitada || !e.activo || e.esRelator || !sitio || Date.now() - plazosRevisados < 5 * 60000) return null;
    plazosRevisados = Date.now();
    var mis = (e.cuenta.cursos || []).slice();
    var vencidos = Object.keys(e.cuenta.vencidos || {});
    return Promise.all(mis.concat(vencidos).filter(function (id, i, a) { return a.indexOf(id) === i && sitio.cursos.indexOf(id) >= 0; }).map(function (id) { return cargarCurso(id).catch(function () { return null; }); }))
      .then(function (cs) {
        var quitar = [], limpiar = [], avisos = [];
        cs.filter(Boolean).forEach(function (c) {
          if (vencidos.indexOf(c.id) >= 0) { // el equipo la desactivó por vencimiento: se borra el avance
            borrarAvance(c.id, c.clases); limpiar.push(c.id);
            if (mis.indexOf(c.id) < 0) avisos.push("Tu inscripción en «" + c.titulo + "» venció y se borró tu avance. Si quieres retomarla, vuelve a solicitarla.");
            return;
          }
          var pl = plazosDe(c);
          if (!pl || pl.estado === "completo") return;
          var ahora = Date.now();
          if (pl.estado === "empezar" && new Date(pl.limite).getTime() < ahora) {
            quitar.push(c.id);
            avisos.push("Se anuló tu inscripción en «" + c.titulo + "» porque no comenzaste dentro de la primera semana. Puedes volver a solicitarla cuando quieras.");
            return;
          }
          (pl.modulos || []).forEach(function (x) {
            if (new Date(x.vence).getTime() >= ahora) return;
            borrarAvance(c.id, x.m.clases);
            almacen.guardar("plazo:" + c.id + ":" + x.m.id, null);
            if (c.modulos.length <= 1) {
              quitar.push(c.id);
              avisos.push("Tu curso «" + c.titulo + "» quedó desactivado porque se cumplieron los 2 meses sin completarlo, y se borró tu avance. Puedes volver a solicitarlo.");
            } else {
              almacen.guardar("plazo:" + c.id + ":reinicio", new Date(ahora).toISOString());
              avisos.push("El " + etiquetaModulo(x.m).toLowerCase() + " «" + x.m.titulo + "» de «" + c.titulo + "» venció sin completarse y se borró su avance. Puedes volver a empezarlo: tendrás 2 meses desde tu primera sesión." + (c.clases.some(function (cl) { return almacen.leer("hechas:todo", []).indexOf(cl.id) >= 0; }) ? "" : " Retoma dentro de una semana para no perder la inscripción.") + "");
            }
          });
        });
        if (avisos.length) {
          try { sessionStorage.setItem("miruta:avisos-plazo", JSON.stringify(avisos)); } catch (er) { /* sin almacenamiento */ }
        }
        if (quitar.length || limpiar.length) return Nube.ajustarMisCursos(quitar, limpiar).catch(function (er) { console.warn("Plazos:", er); });
      });
  }
  // Línea informativa en la página de la formación: hasta cuándo hay plazo.
  function lineaPlazo(c) {
    var pl = plazosDe(c);
    if (!pl || pl.estado === "completo") return "";
    if (pl.estado === "empezar") return '<p class="linea-plazo">Tienes hasta el <b>' + esc(fechaLarga(pl.limite)) + "</b> para completar tu primera sesión. Después, " + (c.modulos.length > 1 ? "cada módulo tiene 2 meses desde que lo empiezas." : "tendrás 2 meses desde tu inscripción para terminar.") + "</p>";
    if (!pl.modulos.length) return "";
    return '<p class="linea-plazo">' + pl.modulos.map(function (x) {
      return (c.modulos.length > 1 ? esc(etiquetaModulo(x.m)) + ": hasta el " : "Plazo para completar: hasta el ") + "<b>" + esc(fechaLarga(x.vence)) + "</b>";
    }).join(" · ") + "</p>";
  }
  function avisosPendientes() {
    var xs = [];
    try { xs = JSON.parse(sessionStorage.getItem("miruta:avisos-plazo") || "[]"); } catch (er) { xs = []; }
    if (!xs.length) return "";
    return '<section class="tarjeta avisos-plazo"><h2>Avisos sobre tus plazos</h2><ul>' + xs.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") +
      '</ul><button class="boton" type="button" id="cerrar-avisos-plazo">Entendido</button></section>';
  }

  function duracionClase(cl) {
    return cl.semana ? "Semana " + cl.semana : (cl.tiempo || "");
  }

  // Enlaces a las secciones de agAPPe que prolongan la formación en la práctica.
  var AG = '<span class="ag-app" aria-label="agAPPe">ag<b>APP</b>e</span>';
  var LOGO_AGAPPE = '<a class="logo-agappe" href="https://pj-agape.github.io/" target="_blank" rel="noopener" aria-label="agAPPe, Pastoral Juvenil Ágape"><img src="assets/agappe-logo.webp" alt="" width="36" height="36"><span><span class="ag-app" aria-hidden="true">ag<b>APP</b>e</span><small>Pastoral Juvenil Ágape</small></span></a>';
  function bloqueAgappe(c) {
    if (!c.agappe || !c.agappe.length) return "";
    return '<section class="agappe-enlaces"><h2 class="seccion-titulo">Vívelo en ' + AG + '</h2><p class="seccion-bajada">Lo que aprendes aquí lo practicas allá, con tu comunidad.</p><div class="agappe-lista">' +
      c.agappe.map(function (x) {
        return '<a class="agappe-item" href="' + esc(x.url) + '" target="_blank" rel="noopener"><b>' + esc(x.titulo) + "</b><span>" + esc(x.texto) + "</span></a>";
      }).join("") + "</div></section>";
  }
  function franjaAgappe(c) {
    if (!c.agappe || !c.agappe.length) return "";
    return '<p class="agappe-franja">Practica en ' + AG + ": " + c.agappe.map(function (x) {
      return '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.titulo) + "</a>";
    }).join(" · ") + "</p>";
  }

  function navegacionClases(c, i) {
    var ant = c.clases[i - 1], sig = c.clases[i + 1];
    return '<nav class="navegacion">' +
      (ant ? '<a href="#/clase/' + esc(c.id) + "/" + esc(ant.id) + '"><small>Anterior</small>' + esc(ant.etiqueta) + ". " + esc(ant.titulo) + "</a>" : "<span></span>") +
      (sig ? '<a class="siguiente" href="#/clase/' + esc(c.id) + "/" + esc(sig.id) + '"><small>Siguiente</small>' + esc(sig.etiqueta) + ". " + esc(sig.titulo) + "</a>" : "<span></span>") +
      "</nav>";
  }

  function barraProgreso(p) {
    return '<div class="progreso"><div class="progreso-barra"><span style="width:' + p.pct + '%"></span></div>' +
      '<div class="progreso-texto">' + p.hechas + " de " + p.total + " completadas</div></div>";
  }

  function pintar(html, titulo) {
    app.innerHTML = html;
    document.title = titulo ? titulo + " · " + (sitio ? sitio.nombre : "Mi Ruta") : (sitio ? sitio.nombre : "Mi Ruta");
    window.scrollTo(0, 0);
  }

  function error(e) {
    pintar('<div class="tarjeta"><h1>No se pudo cargar</h1><p>' + esc(e.message) +
      '</p><p><a href="#/">Volver al inicio</a></p></div>', "Error");
  }

  function enlaceVideo(url) {
    if (!url) return "";
    var m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]{6,})/);
    if (m) return "https://www.youtube-nocookie.com/embed/" + m[1];
    var v = url.match(/vimeo\.com\/(\d+)/);
    if (v) return "https://player.vimeo.com/video/" + v[1];
    var d = url.match(/drive\.google\.com\/file\/d\/([\w-]+)/);
    if (d) return "https://drive.google.com/file/d/" + d[1] + "/preview";
    return "";
  }

  function enlacePresentacion(url) {
    if (!url) return "";
    var m = url.match(/docs\.google\.com\/presentation\/d\/([\w-]+)/);
    if (m) return "https://docs.google.com/presentation/d/" + m[1] + "/embed";
    if (/\.pdf($|\?)/i.test(url)) return url;
    return "";
  }

  /* ---------- vistas ---------- */

  // Íconos de línea para la portada (sin emojis).
  var ICONOS = {
    curso: '<path d="M4 19 C8 19 9 13 12 13 S16 7 20 7"/><circle cx="4" cy="19" r="1.6"/><circle cx="20" cy="7" r="1.6"/>',
    diplomado: '<path d="M3 9 L12 5 L21 9 L12 13 Z"/><path d="M7 11 V15.5 C9.5 17.5 14.5 17.5 17 15.5 V11"/><path d="M21 9 V14"/>',
    "Liturgia": '<path d="M7 4 H17 C17 9 14.5 11 12 11 C9.5 11 7 9 7 4 Z"/><path d="M12 11 V18"/><path d="M8 20 H16"/>',
    "Fe": '<path d="M12 3 V21"/><path d="M7 8 H17"/>',
    "Sagrada Escritura": '<path d="M4 5 H10 A2 2 0 0 1 12 7 V20 A2 2 0 0 0 10 18 H4 Z"/><path d="M20 5 H14 A2 2 0 0 0 12 7 V20 A2 2 0 0 1 14 18 H20 Z"/>',
    "Misión y servicio": '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5 L13.2 13.2 L8.5 15.5 L10.8 10.8 Z"/>',
    "Cuidado": '<path d="M12 20 C5 15 3.5 11.5 3.5 8.5 A4.2 4.2 0 0 1 12 6.8 A4.2 4.2 0 0 1 20.5 8.5 C20.5 11.5 19 15 12 20 Z"/>',
    "Herramientas": '<path d="M14.5 6.5 A4 4 0 0 0 9.3 11.7 L4 17 L7 20 L12.3 14.7 A4 4 0 0 0 17.5 9.5 L15 12 L12 9 Z"/>',
    buscar: '<circle cx="11" cy="11" r="6.5"/><path d="M16 16 L20.5 20.5"/>'
  };
  function icono(nombre, clase) {
    return '<svg class="' + (clase || "icono") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (ICONOS[nombre] || ICONOS.curso) + "</svg>";
  }
  var ORDEN_AREAS = ["Liturgia", "Fe", "Sagrada Escritura", "Misión y servicio", "Cuidado", "Herramientas"];

  /* ---------- imágenes de las tarjetas (las edita un administrador) ---------- */

  var TARJETAS = null;
  var FONDO_INICIO = "_portada"; // la imagen de fondo del encabezado se guarda junto a las de las tarjetas
  function puedeEditarTarjetas() { return !Nube.habilitada || cuentaActual().esAdmin; }
  function cargarTarjetas() {
    if (TARJETAS) return Promise.resolve(TARJETAS);
    var p = Nube.habilitada && Nube.leerTarjetas ? Nube.leerTarjetas() : Promise.resolve(leerTarjetasLocal());
    return p.catch(function (e) { console.warn("Tarjetas:", e); return {}; }).then(function (t) { TARJETAS = t || {}; return TARJETAS; });
  }
  function leerTarjetasLocal() { try { return JSON.parse(localStorage.getItem("agp:tarjetas") || "{}"); } catch (e) { return {}; } }
  function guardarTarjeta(id, imagen) {
    var p;
    if (Nube.habilitada) p = Nube.guardarTarjeta(id, imagen);
    else {
      var t = leerTarjetasLocal();
      if (imagen) t[id] = imagen; else delete t[id];
      try { localStorage.setItem("agp:tarjetas", JSON.stringify(t)); p = Promise.resolve(); }
      catch (e) { p = Promise.reject(new Error("No hay espacio para guardar la imagen en este navegador.")); }
    }
    return p.then(function () { if (imagen) TARJETAS[id] = imagen; else delete TARJETAS[id]; });
  }
  function guardarVelo(id, velo) {
    var p;
    if (Nube.habilitada) p = Nube.guardarVelo(id, velo);
    else {
      var t = leerTarjetasLocal(); t[id + ":velo"] = velo;
      try { localStorage.setItem("agp:tarjetas", JSON.stringify(t)); p = Promise.resolve(); } catch (e) { p = Promise.reject(e); }
    }
    return p.then(function () { TARJETAS[id + ":velo"] = velo; });
  }
  function estiloVelo(v) { return "--velo-a:" + (v * 0.3).toFixed(3) + ";--velo-b:" + v.toFixed(3); }
  var VELO_DEFECTO = 0.45;

  // Recorta la imagen al formato de la tarjeta (16:9) y la comprime para que pese poco.
  function prepararImagen(archivo, ancho, alto) {
    return new Promise(function (ok, no) {
      if (!/^image\//.test(archivo.type)) return no(new Error("El archivo no es una imagen."));
      var url = URL.createObjectURL(archivo);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var W = ancho || 640, H = alto || 360, cv = document.createElement("canvas");
        cv.width = W; cv.height = H;
        var esc0 = Math.max(W / img.width, H / img.height);
        var w = img.width * esc0, h = img.height * esc0;
        var ctx = cv.getContext("2d");
        ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
        ctx.drawImage(img, (W - w) / 2, (H - h) / 2, w, h);
        var tipo = cv.toDataURL("image/webp").indexOf("data:image/webp") === 0 ? "image/webp" : "image/jpeg";
        var datos, q = 0.82;
        do { datos = cv.toDataURL(tipo, q); q -= 0.12; } while (datos.length > 250000 && q > 0.3);
        if (datos.length > 290000) return no(new Error("La imagen es demasiado pesada. Prueba con otra."));
        ok(datos);
      };
      img.onerror = function () { URL.revokeObjectURL(url); no(new Error("No se pudo leer la imagen.")); };
      img.src = url;
    });
  }

  /* ---------- áreas de formación ---------- */

  // Cada área agrupa formaciones (de una institución, una persona o un ámbito). Si sitio.json no trae áreas, todo va en una sola.
  function areas() {
    if (sitio.areas && sitio.areas.length) return sitio.areas;
    return [{ id: "general", titulo: "Formaciones", descripcion: "", cursos: sitio.cursos }];
  }
  function areaDe(cursoId) {
    return areas().filter(function (a) { return a.cursos.indexOf(cursoId) >= 0; })[0] || null;
  }
  function claveArea(id) { return "area-" + id; }

  function metaTile(c) {
    if (c.tipo === "curso") return (c.horas ? c.horas + " h · " : "") + (c.modulos_n || c.modulos.length) + " módulos";
    return esPropedeutico(c) ? "4 encuentros · 4 h" : "6 sesiones · 9 h";
  }
  function tileHTML(c) {
    var ic = c.tipo === "curso" ? (c.nivel === "diplomado" ? "diplomado" : "curso") : c.categoria;
    var p = progreso(c);
    var a = areaDe(c.id);
    var texto = [c.titulo, c.subtitulo, c.categoria, c.descripcion, a ? a.titulo : ""].join(" ").toLowerCase();
    var img = TARJETAS && TARJETAS[c.id];
    return '<a class="tile tile-' + (c.tipo === "curso" ? (c.nivel || "curso") : "modulo") + (img ? " con-imagen" : "") + '" href="#/curso/' + esc(c.id) + '" data-texto="' + esc(texto) + '">' +
      (img ? '<img class="tile-imagen" src="' + esc(img) + '" alt="" loading="lazy">' : "") +
      '<span class="tile-icono">' + icono(ic) + "</span>" +
      '<span class="tile-titulo">' + esc(c.titulo) + "</span>" +
      '<span class="tile-meta">' + esc(metaTile(c)) + "</span>" +
      (p.hechas ? '<span class="tile-avance" style="--pct:' + p.pct + '%"></span>' : "") +
      (c.nuevo ? '<span class="tile-nuevo">Nuevo</span>' : "") + "</a>";
  }

  // Editor de imagen de fondo (administradores): portada de inicio y portada de cada área.
  function editorFondo(clave, fondo, velo) {
    if (!puedeEditarTarjetas()) return "";
    return '<div class="editar-fondo" data-clave="' + esc(clave) + '"><label class="boton">' + (fondo ? "Cambiar fondo" : "Poner imagen de fondo") + '<input type="file" accept="image/*" class="fondo-archivo" hidden></label>' +
      (fondo ? '<button class="boton fondo-quitar" type="button">Quitar fondo</button>' +
        '<label class="control-velo">Velo <input type="range" class="fondo-velo" min="0" max="90" step="5" value="' + Math.round(velo * 100) + '"> <output>' + Math.round(velo * 100) + ' %</output></label>' : "") +
      '<span class="mensaje" aria-live="polite"></span></div>';
  }
  function fondoDe(clave) {
    var fondo = TARJETAS && TARJETAS[clave];
    var velo = TARJETAS && typeof TARJETAS[clave + ":velo"] === "number" ? TARJETAS[clave + ":velo"] : VELO_DEFECTO;
    return { fondo: fondo, velo: velo, attr: fondo ? ' style="--fondo-inicio:url(\'' + esc(fondo) + '\');' + estiloVelo(velo) + '"' : "" };
  }
  function activarFondos() {
    app.querySelectorAll(".editar-fondo").forEach(function (ed) {
      var clave = ed.getAttribute("data-clave");
      var msj = ed.querySelector(".mensaje");
      var portada = ed.closest(".portada");
      var archivo = ed.querySelector(".fondo-archivo");
      archivo.addEventListener("change", function () {
        if (!archivo.files[0]) return;
        msj.className = "mensaje"; msj.textContent = "Guardando…";
        prepararImagen(archivo.files[0], 1600, 640).then(function (d) { return guardarTarjeta(clave, d); }).then(ruta)
          .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
      });
      var quitar = ed.querySelector(".fondo-quitar");
      if (quitar) quitar.addEventListener("click", function () {
        guardarTarjeta(clave, "").then(ruta).catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
      });
      var rango = ed.querySelector(".fondo-velo");
      if (rango) {
        var salida = rango.parentNode.querySelector("output");
        rango.addEventListener("input", function () {
          var v = Number(rango.value) / 100;
          portada.style.setProperty("--velo-a", (v * 0.3).toFixed(3));
          portada.style.setProperty("--velo-b", v.toFixed(3));
          salida.textContent = rango.value + " %";
        });
        rango.addEventListener("change", function () {
          msj.className = "mensaje"; msj.textContent = "Guardando…";
          guardarVelo(clave, Number(rango.value) / 100)
            .then(function () { msj.textContent = "Guardado"; setTimeout(function () { msj.textContent = ""; }, 1500); })
            .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
        });
      }
    });
  }

  function activarFichas(selector) {
    app.querySelectorAll(selector).forEach(function (t) {
      t.addEventListener("click", function (ev) {
        var id = t.getAttribute("href").replace("#/curso/", "");
        var c = FICHAS_INICIO[id];
        if (!c || !window.HTMLDialogElement) return;
        ev.preventDefault();
        abrirFicha(c, t);
      });
    });
  }

  function vistaInicio() {
    return Promise.all([Promise.all(sitio.cursos.map(cargarCurso)), cargarTarjetas()]).then(function (r) {
      var lista = r[0];
      var e = cuentaActual();
      var invitado = Nube.habilitada && e.status === "invitado";
      var f = fondoDe(FONDO_INICIO);
      FICHAS_INICIO = {};
      lista.forEach(function (c) { FICHAS_INICIO[c.id] = c; });
      var html = '<section class="portada portada-inicio' + (f.fondo ? " con-fondo" : "") + '"' + f.attr + '><h1 class="logo-titulo">' + nombreConEstilo(sitio.nombre) + "</h1>" + FIRMA +
        '<p class="portada-lema">Formación para servir: cursos, diplomados y módulos con constancia, a tu ritmo y con tu comunidad.</p>' +
        '<label class="buscador">' + icono("buscar", "icono-buscar") + '<input id="buscar" type="search" placeholder="¿Qué quieres aprender?" autocomplete="off" aria-label="Buscar cursos y módulos"></label>' +
        (invitado ? '<div class="botones"><a class="boton principal" href="#/ingresar">Inscríbete</a><a class="boton" href="#/ingresar">Ingresar</a></div>' : "") +
        editorFondo(FONDO_INICIO, f.fondo, f.velo) + "</section>";

      var prope = lista.filter(esPropedeutico)[0];
      if (prope) {
        var pp = progreso(prope);
        if (pp.hechas < pp.total) {
          html += '<section class="tarjeta comienza-aqui"><p class="subtitulo">Comienza aquí</p><h2>' + esc(prope.titulo) + "</h2>" +
            "<p>Antes de elegir qué estudiar, la pregunta es para qué. Cuatro encuentros breves para descubrir a qué te llama Dios, conocer los caminos en la Iglesia y elegir tu ruta. Abierto para todos, sin inscripción.</p>" +
            (pp.hechas ? barraProgreso(pp) : "") +
            '<div class="botones"><a class="boton principal" href="#/curso/' + esc(prope.id) + '">' + (pp.hechas ? "Continuar" : "Comenzar") + "</a></div></section>";
        }
      }
      html += avisosPendientes();
      if (Nube.habilitada && e.status === "pendiente") {
        var solic = (e.cuenta.solicitudes || []).map(function (id) { var c = lista.filter(function (x) { return x.id === id; })[0]; return c ? c.titulo : id; });
        html += '<section class="tarjeta acceso-inicio"><h2>Hola, ' + esc(e.cuenta.nombre) + '</h2><p>Tu cuenta está en revisión.</p>' +
          (solic.length ? '<p><b>Solicitaste:</b> ' + solic.map(esc).join(", ") + '. Te habilitaremos apenas se apruebe tu cuenta.</p>'
            : '<p>Todavía no solicitas ninguna formación. Elige una, entra a ella y toca <b>Solicitar inscripción</b>.</p>') +
          '<div class="botones"><a class="boton" href="#/perfil">Mi cuenta</a></div></section>';
      } else if (Nube.habilitada && e.activo) {
        // Relatores y administradores también son participantes: ven sus cursos inscritos y los que ya empezaron.
        var cursados = almacen.leer("cursados", []);
        var mios = lista.filter(function (c) { return (esPropedeutico(c) && progreso(c).hechas >= progreso(c).total) || (e.cuenta.cursos || []).indexOf(c.id) >= 0 || (e.esRelator && (cursados.indexOf(c.id) >= 0 || c.tipo !== "curso") && progreso(c).hechas > 0); });
        var alertas = mios.map(function (c) { return avisosPlazo(c, true); }).join("");
        html += '<section class="seccion-inicio"><h2 class="seccion-titulo">Mis cursos</h2>' + alertas +
          (mios.length ? mios.map(function (c) {
            return '<a class="mi-curso" href="#/curso/' + esc(c.id) + '"><span class="mi-curso-titulo">' + esc(c.titulo) + "</span>" + barraProgreso(progreso(c)) + "</a>";
          }).join("") : '<p class="seccion-bajada">' + (e.esRelator ? "Todavía no comienzas ninguna formación. Como " + (e.esAdmin ? "administrador" : "relator") + " puedes entrar a cualquiera: tu avance quedará aquí." : "Todavía no tienes cursos habilitados. Elige uno y solicita la inscripción.") + "</p>") + "</section>";
      }

      if (Nube.habilitada && e.activo) html += '<section class="seccion-inicio" id="proximas-fechas"></section>';
      html += '<section class="seccion-inicio" id="areas-inicio"><h2 class="seccion-titulo">Áreas de formación</h2><div class="areas-lista">' +
        areas().map(function (a) {
          var img = TARJETAS && TARJETAS[claveArea(a.id)];
          var cs = a.cursos.map(function (id) { return FICHAS_INICIO[id]; }).filter(Boolean);
          var n = { cursos: cs.filter(function (c) { return c.tipo === "curso" && c.nivel !== "diplomado"; }).length, dip: cs.filter(function (c) { return c.nivel === "diplomado"; }).length, mod: cs.filter(function (c) { return c.tipo !== "curso"; }).length };
          var cifras = [n.cursos ? n.cursos + (n.cursos === 1 ? " curso" : " cursos") : "", n.dip ? n.dip + (n.dip === 1 ? " diplomado" : " diplomados") : "", n.mod ? n.mod + (n.mod === 1 ? " módulo" : " módulos") : ""].filter(Boolean).join(" · ");
          return '<a class="area-tarjeta" href="#/area/' + esc(a.id) + '"' + (a.descripcion ? ' title="' + esc(a.descripcion) + '"' : "") + ">" +
            (img ? '<img class="area-imagen" src="' + esc(img) + '" alt="" loading="lazy">' : '<span class="area-imagen area-sin-imagen">' + icono("curso") + "</span>") +
            '<b class="area-titulo">' + esc(a.titulo) + '</b><span class="area-cifras">' + esc(cifras) + '</span><span class="area-ir" aria-hidden="true">&rsaquo;</span></a>';
        }).join("") + "</div></section>" +
        '<section class="seccion-inicio" id="resultados-inicio" hidden><h2 class="seccion-titulo">Resultados</h2><div class="tiles">' + lista.map(tileHTML).join("") +
        '</div><p class="sin-resultados" hidden>No encontramos cursos ni módulos con esa búsqueda.</p></section>';

      html += '<section class="seccion-inicio como-funciona"><h2 class="seccion-titulo">Cómo funciona</h2><ol class="pasos">' +
        '<li><b>Comienza aquí</b><span>Haz los cuatro encuentros de «Llamados»: descubre para qué te formas y qué camino quieres seguir.</span></li>' +
        '<li><b>Crea tu cuenta</b><span>Con Google o con tu correo. Es gratis.</span></li>' +
        '<li><b>Elige tu formación</b><span>Entra a un área y elige un curso, un diplomado o un módulo suelto, y solicita la inscripción.</span></li>' +
        '<li><b>Tu relator te acompaña</b><span>Aprueba tu inscripción y te guía en los encuentros con tu comunidad.</span></li>' +
        '<li><b>Avanza y certifícate</b><span>Cada módulo aprobado entrega una constancia verificable con código.</span></li></ol></section>';

      html += '<section class="seccion-inicio ayuda"><h2 class="seccion-titulo">Preguntas frecuentes</h2>' +
        '<details><summary>¿Cuánto cuesta?</summary><p>Nada. Mi Ruta es una iniciativa de agAPPe y la formación es gratuita.</p></details>' +
        '<details><summary>¿Qué es un área de formación?</summary><p>Un conjunto de formaciones de un mismo ámbito o de una misma institución. Dentro de cada área encontrarás sus cursos, diplomados y módulos.</p></details>' +
        '<details><summary>¿Qué diferencia hay entre un curso, un diplomado y un módulo?</summary><p>Un módulo es una formación de seis sesiones. Un curso reúne varios módulos (obligatorios y optativos) en un programa. Un diplomado es una formación más profunda, con constancia por cada módulo y un certificado final.</p></details>' +
        '<details><summary>¿Si ya aprobé un módulo, tengo que repetirlo en otro curso?</summary><p>No. Un módulo aprobado vale en todos los cursos que lo incluyen.</p></details>' +
        '<details><summary>¿Cómo se verifica una constancia?</summary><p>Cada constancia tiene un código. Cualquiera puede verificarla en esta página sin necesidad de cuenta.</p></details>' +
        '<details><summary>Soy menor de edad, ¿puedo inscribirme?</summary><p>Sí, cada formación indica la edad mínima. Crea tu cuenta con conocimiento de tus padres o tutores.</p></details>' +
        "</section>";
      pintar(html);
      activarFondos();
      activarFichas("#resultados-inicio .tile");
      if (Nube.habilitada && e.activo) cargarProximasFechas(Array.from(new Set((e.cuenta.cursos || []).concat(sitio.propedeutico ? [sitio.propedeutico] : [], e.esRelator ? almacen.leer("cursados", []) : []))).filter(function (id) { return sitio.cursos.indexOf(id) >= 0; }));
      var buscar = document.getElementById("buscar");
      buscar.addEventListener("input", function () {
        var q = buscar.value.trim().toLowerCase();
        document.getElementById("areas-inicio").hidden = !!q;
        var res = document.getElementById("resultados-inicio");
        res.hidden = !q;
        var hay = 0;
        res.querySelectorAll(".tile").forEach(function (t) { var ok = !!q && t.getAttribute("data-texto").indexOf(q) >= 0; t.hidden = !ok; if (ok) hay++; });
        res.querySelector(".sin-resultados").hidden = hay > 0;
      });
    });
  }

  function vistaArea(id) {
    var a = areas().filter(function (x) { return x.id === id; })[0];
    if (!a) { location.hash = "#/"; return Promise.resolve(); }
    return Promise.all([Promise.all(a.cursos.map(cargarCurso)), cargarTarjetas()]).then(function (r) {
      var lista = r[0];
      FICHAS_INICIO = {};
      lista.forEach(function (c) { FICHAS_INICIO[c.id] = c; });
      var f = fondoDe(claveArea(a.id));
      var html = '<nav class="migas"><a href="#/">Inicio</a></nav>' +
        '<section class="portada portada-area portada-inicio' + (f.fondo ? " con-fondo" : "") + '"' + f.attr + '>' +
        (a.institucion ? (a.institucion === "agAPPe" ? LOGO_AGAPPE : '<p class="subtitulo">' + esc(a.institucion) + "</p>") : "") +
        "<h1>" + esc(a.titulo) + "</h1>" + (a.descripcion ? '<p class="portada-lema">' + esc(a.descripcion) + "</p>" : "") +
        '<label class="buscador">' + icono("buscar", "icono-buscar") + '<input id="buscar" type="search" placeholder="Buscar en esta área" autocomplete="off" aria-label="Buscar en esta área"></label>' +
        editorFondo(claveArea(a.id), f.fondo, f.velo) + "</section>";

      var cursosL = lista.filter(function (c) { return c.tipo === "curso" && c.nivel !== "diplomado"; });
      var diplomados = lista.filter(function (c) { return c.nivel === "diplomado"; });
      var modulos = lista.filter(function (c) { return c.tipo !== "curso"; });
      var nuevos = lista.filter(function (c) { return c.nuevo; });
      function grupo(gid, titulo, bajada, items) {
        if (!items.length) return "";
        return '<section class="seccion-inicio grupo-tiles" data-grupo="' + gid + '"><h2 class="seccion-titulo">' + titulo + "</h2>" +
          (bajada ? '<p class="seccion-bajada">' + bajada + "</p>" : "") + '<div class="tiles">' + items.map(tileHTML).join("") + "</div></section>";
      }
      var pest = [["todo", "Todo"]];
      if (cursosL.length) pest.push(["cursos", "Cursos"]);
      if (diplomados.length) pest.push(["diplomados", "Diplomados"]);
      if (modulos.length) pest.push(["modulos", "Módulos"]);
      html += '<nav class="pestanas-inicio" role="tablist">' + pest.map(function (t, k) {
        return '<button role="tab" data-ver="' + t[0] + '" aria-selected="' + (k === 0) + '">' + t[1] + "</button>";
      }).join("") + "</nav>";
      html += '<div id="oferta">';
      if (nuevos.length) html += grupo("nuevos", "Nuevos", "", nuevos);
      html += grupo("cursos", "Cursos", "Programas completos con módulos obligatorios y optativos. Al terminar recibes el certificado del curso.", cursosL);
      html += grupo("diplomados", "Diplomados", "Formación de mayor profundidad. Cada módulo entrega su propia constancia.", diplomados);
      var temas = ORDEN_AREAS.filter(function (t) { return modulos.some(function (c) { return c.categoria === t; }); });
      modulos.forEach(function (c) { if (temas.indexOf(c.categoria) < 0) temas.push(c.categoria); });
      if (modulos.length) html += '<section class="seccion-inicio" data-grupo="modulos"><h2 class="seccion-titulo">Módulos por tema</h2><p class="seccion-bajada">Formaciones breves de seis sesiones que puedes tomar por separado. Si después te inscribes en un curso que las incluye, se te reconocen.</p>' +
        temas.map(function (t) {
          return '<div class="grupo-tiles area"><h3 class="categoria-titulo">' + icono(t, "icono-area") + esc(t) + '</h3><div class="tiles">' +
            modulos.filter(function (c) { return c.categoria === t; }).map(tileHTML).join("") + "</div></div>";
        }).join("") + "</section>";
      html += '<p class="sin-resultados" hidden>No encontramos cursos ni módulos con esa búsqueda.</p></div>';
      pintar(html, a.titulo);
      activarFondos();
      activarFichas("#oferta .tile");
      activarOferta();
    });
  }

  var FICHAS_INICIO = {};


  function enfasis(t) { return esc(t).replace(/\*([^*]+)\*/g, "<em>$1</em>"); }

  function abrirFicha(c, origen) {
    var viejo = document.getElementById("ficha-dialogo");
    if (viejo) viejo.remove();
    var tipo = c.tipo === "curso" ? (c.nivel === "diplomado" ? "Diplomado" : "Curso") : "Módulo";
    var ic = c.tipo === "curso" ? (c.nivel === "diplomado" ? "diplomado" : "curso") : c.categoria;
    var cont = c.contenidos || [];
    var obl = cont.filter(function (x) { return x.tipo !== "optativo"; });
    var opt = cont.filter(function (x) { return x.tipo === "optativo"; });
    var indice = c.tipo === "curso"
      ? '<ol class="ficha-indice">' + obl.map(function (x) { return "<li>" + esc(x.titulo) + "</li>"; }).join("") + "</ol>" +
        (opt.length ? '<p class="ficha-optativos"><b>Optativos' + (c.elige ? " (eliges " + c.elige + ")" : "") + ":</b> " + opt.map(function (x) { return esc(x.titulo); }).join(" · ") + "</p>" : "")
      : '<ol class="ficha-indice">' + cont.map(function (x) { return "<li>" + esc(x.titulo) + "</li>"; }).join("") + "</ol>";
    var d = document.createElement("dialog");
    d.id = "ficha-dialogo";
    d.className = "ficha-dialogo";
    d.setAttribute("aria-labelledby", "ficha-titulo");
    var img = TARJETAS && TARJETAS[c.id];
    var editor = puedeEditarTarjetas() ? '<div class="ficha-editor"><h3>Imagen de la tarjeta</h3>' +
      '<p class="ficha-nota">Visible solo para administradores. Se recorta en formato horizontal (16:9) y se comprime automáticamente.</p>' +
      '<div class="botones"><label class="boton">' + (img ? "Cambiar imagen" : "Subir imagen") + '<input type="file" accept="image/*" data-imagen hidden></label>' +
      (img ? '<button class="boton" type="button" data-quitar-imagen>Quitar imagen</button>' : "") + '</div><div class="mensaje" aria-live="polite"></div></div>' : "";
    d.innerHTML = '<div class="ficha-cuerpo">' +
      (img ? '<img class="ficha-imagen" src="' + esc(img) + '" alt="">' : "") +
      '<button class="ficha-cerrar" type="button" aria-label="Cerrar">&times;</button>' +
      '<div class="ficha-cabecera"><span class="tile-icono">' + icono(ic) + '</span><div><p class="ficha-tipo">' + tipo + (c.categoria && c.tipo !== "curso" ? " · " + esc(c.categoria) : "") + '</p><h2 id="ficha-titulo">' + esc(c.titulo) + "</h2></div></div>" +
      '<ul class="etiquetas">' + [c.duracion, c.modalidad, c.publico].filter(Boolean).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" +
      "<p>" + esc(c.descripcion || "") + "</p>" +
      (c.ejes && c.ejes.length ? '<h3>Ejes temáticos</h3><ul class="ficha-ejes">' + c.ejes.map(function (x) { return "<li>" + enfasis(x) + "</li>"; }).join("") + "</ul>" : "") +
      (c.competencias && c.competencias.length ? '<h3>Competencias que aporta</h3><ul class="ficha-competencias">' + c.competencias.map(function (x) { return "<li>" + enfasis(x) + "</li>"; }).join("") + "</ul>" : "") +
      (cont.length ? "<h3>" + (c.tipo === "curso" ? "Módulos" : "Sesiones") + "</h3>" + indice : "") + editor +
      '</div><div class="ficha-acciones"><a class="boton principal" href="#/curso/' + esc(c.id) + '">Ver la formación</a><button class="boton" type="button" data-cerrar>Cerrar</button></div>';
    document.body.appendChild(d);
    function cerrar() { d.close(); }
    d.querySelector(".ficha-cerrar").addEventListener("click", cerrar);
    d.querySelector("[data-cerrar]").addEventListener("click", cerrar);
    d.querySelector(".ficha-acciones a").addEventListener("click", cerrar);
    d.addEventListener("click", function (ev) { if (ev.target === d) cerrar(); });
    function refrescar() {
      app.querySelectorAll('.tile[href="#/curso/' + c.id + '"]').forEach(function (t) {
        var viejo = t.querySelector(".tile-imagen");
        if (viejo) viejo.remove();
        t.classList.toggle("con-imagen", !!TARJETAS[c.id]);
        if (TARJETAS[c.id]) { var im = document.createElement("img"); im.className = "tile-imagen"; im.alt = ""; im.src = TARJETAS[c.id]; t.insertBefore(im, t.firstChild); }
      });
      var pos = d.querySelector(".ficha-cuerpo").scrollTop;
      d.close();
      abrirFicha(c, origen);
      var nuevo = document.getElementById("ficha-dialogo");
      if (nuevo) nuevo.querySelector(".ficha-cuerpo").scrollTop = pos;
    }
    var entrada = d.querySelector("[data-imagen]");
    if (entrada) entrada.addEventListener("change", function () {
      var msj = d.querySelector(".ficha-editor .mensaje");
      if (!entrada.files[0]) return;
      msj.className = "mensaje"; msj.textContent = "Guardando…";
      prepararImagen(entrada.files[0]).then(function (datos) { return guardarTarjeta(c.id, datos); }).then(refrescar)
        .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
    });
    var quitar = d.querySelector("[data-quitar-imagen]");
    if (quitar) quitar.addEventListener("click", function () {
      guardarTarjeta(c.id, "").then(refrescar).catch(function (er) { var msj = d.querySelector(".ficha-editor .mensaje"); msj.className = "mensaje error"; msj.textContent = er.message; });
    });
    d.addEventListener("close", function () { d.remove(); if (origen && document.body.contains(origen)) origen.focus(); });
    if (d.showModal) d.showModal(); else location.hash = "#/curso/" + c.id;
  }

  function activarOferta() {
    var pestanas = app.querySelectorAll("[data-ver]");
    var buscar = document.getElementById("buscar");
    var filtroVer = "todo";
    function aplicar() {
      var q = (buscar.value || "").trim().toLowerCase();
      app.querySelectorAll("#oferta [data-grupo]").forEach(function (g) {
        var id = g.getAttribute("data-grupo");
        var visible = filtroVer === "todo" ? (q ? id !== "nuevos" : true) : id === filtroVer;
        g.hidden = !visible;
      });
      var hay = 0;
      app.querySelectorAll("#oferta .tile").forEach(function (t) {
        var ok = !q || t.getAttribute("data-texto").indexOf(q) >= 0;
        t.hidden = !ok;
        if (ok && !t.closest("[data-grupo]").hidden) hay++;
      });
      app.querySelectorAll("#oferta .area").forEach(function (a) { a.hidden = !a.querySelector(".tile:not([hidden])"); });
      app.querySelector(".sin-resultados").hidden = hay > 0;
    }
    pestanas.forEach(function (b) {
      b.addEventListener("click", function () {
        filtroVer = b.getAttribute("data-ver");
        pestanas.forEach(function (x) { x.setAttribute("aria-selected", String(x === b)); });
        aplicar();
      });
    });
    buscar.addEventListener("input", aplicar);
  }

  function vistaCurso(id) {
    return Promise.all([cargarCurso(id), cargarTarjetas()]).then(function (r) {
      var c = r[0];
      var foto = TARJETAS && TARJETAS[c.id];
      var p = progreso(c);
      var h = hechas(c.id);
      var siguiente = c.clases.filter(function (x) { return h.indexOf(x.id) < 0 && !moduloBloqueado(c, x.modulo); })[0];
      var ar = areaDe(c.id);
      var html = '<nav class="migas"><a href="#/">Inicio</a>' + (ar && areas().length ? ' / <a href="#/area/' + esc(ar.id) + '">' + esc(ar.titulo) + "</a>" : "") + "</nav>";
      html += '<section class="portada' + (foto ? ' portada-foto" style="--fondo-curso:url(\'' + esc(foto) + '\')' : "") + '"><p class="subtitulo">' + (c.tipo === "curso" ? (c.nivel === "diplomado" ? "Diplomado · " : "Curso · ") : (c.categoria ? esc(c.categoria) + " · " : (c.institucion ? esc(c.institucion) + " · " : ""))) + esc(c.subtitulo) + "</p><h1>" + esc(c.titulo) + "</h1><p>" + esc(c.descripcion) + "</p>" +
        '<ul class="etiquetas"><li>' + esc(c.duracion) + "</li><li>" + esc(c.modalidad) + "</li>" + (c.publico ? "<li>" + esc(c.publico) + "</li>" : "") + "</ul>" +
        (c.aviso ? '<p class="aviso revision">' + esc(c.aviso) + "</p>" : "") +
        (acceso(c) === "libre" ? barraProgreso(p) : "") +
        '<div class="botones">' +
        (siguiente && acceso(c) === "libre" ? '<a class="boton principal" href="#/clase/' + esc(c.id) + "/" + esc(siguiente.id) + '">' + (p.hechas ? "Continuar" : "Comenzar") + "</a>" : "") +
        (c.programa ? '<a class="boton" href="#/curso/' + esc(c.id) + '/programa">Programa</a>' : "") +
        (c.sesiones && c.sesiones.length ? '<a class="boton" href="#/curso/' + esc(c.id) + '/sesiones">Sesiones en vivo</a>' : "") + "</div></section>";

      var tipoAcceso = acceso(c);
      if (tipoAcceso !== "libre") html += '<section class="tarjeta">' + bloqueAcceso(c, tipoAcceso) + "</section>";
      html += pestanasCurso(c, "contenido");
      html += avisosPlazo(c, false) + lineaPlazo(c);
      html += bloqueAgappe(c);
      var vistoOpt = false;
      // Con varios módulos, cada uno se pliega: se ve el nombre y el avance, y se despliega el listado de sesiones al tocarlo.
      var plegable = c.modulos.length > 1;
      var abiertos = plegable ? modulosAbiertos(c, siguiente) : null;
      if (plegable) html += '<div class="plegar-todo"><button class="boton mini" type="button" data-plegar="abrir">Desplegar todos</button><button class="boton mini" type="button" data-plegar="cerrar">Plegar todos</button></div>';
      if (c.tipo === "curso") html += '<h2 class="seccion-titulo">Módulos obligatorios</h2><p class="seccion-bajada">Algunos módulos se habilitan al completar otros; lo verás indicado en cada uno.</p>';
      c.modulos.forEach(function (m) {
        var hm = m.clases.filter(function (x) { return h.indexOf(x.id) >= 0; }).length;
        if (m.tipo === "optativo" && !vistoOpt) {
          vistoOpt = true;
          html += '<h2 class="seccion-titulo">Módulos optativos</h2><p class="seccion-bajada">Elige ' + (c.elige === 1 ? "uno" : c.elige) + '. Puedes cursarlos en cualquier momento.</p>';
        }
        var cab = '<h2>' + esc(etiquetaModulo(m)) + ". " + esc(m.titulo) + "</h2>" +
          (m.semanas ? '<p class="semanas">Semanas ' + esc(m.semanas) + "</p>" : "") +
          (m.duracion || m.constancia || plegable ? '<p class="semanas">' + [m.duracion ? esc(m.duracion) : "", m.constancia ? '<span class="chip-constancia">Constancia propia</span>' : ""].filter(Boolean).join(" · ") +
            (m.constancia || plegable ? (m.duracion || m.constancia ? " · " : "") + hm + " de " + m.clases.length + " completadas" : "") + "</p>" : "");
        if (plegable) {
          var bloq = moduloBloqueado(c, m), estadoMod = hm >= m.clases.length ? ["completo", "Completo"] : bloq ? ["bloqueado", "Bloqueado"] : hm ? ["curso", "En curso"] : null;
          html += '<details class="tarjeta modulo plegable" data-modulo="' + esc(m.id) + '"' + (abiertos[m.id] ? " open" : "") + '><summary class="modulo-cab"><div class="modulo-cab-texto">' + cab +
            '<div class="mini-barra" aria-hidden="true"><span style="width:' + Math.round(100 * hm / Math.max(1, m.clases.length)) + '%"></span></div></div>' +
            (estadoMod ? '<span class="estado-modulo ' + estadoMod[0] + '">' + estadoMod[1] + "</span>" : "") + '<span class="flecha" aria-hidden="true"></span></summary><div class="modulo-cuerpo">';
        } else html += '<section class="tarjeta modulo">' + cab;
        if (m.intro) html += '<details><summary>' + (m.intro.indexOf("#### Objetivos") >= 0 ? "Programa del módulo: objetivos, bibliografía y evaluación" : "Sobre este módulo") + '</summary><div class="texto">' + md(m.intro) + "</div></details>";
        var bloqueo = moduloBloqueado(c, m);
        if (bloqueo) {
          html += '<p class="aviso bloqueo">Se habilita al completar ' + bloqueo.map(function (r) { return esc(etiquetaModulo(r)); }).join(" y ") + ".</p>";
        }
        html += '<ol class="lista-clases' + (bloqueo || tipoAcceso !== "libre" ? " bloqueada" : "") + '">' + m.clases.map(function (cl) {
          var hecha = h.indexOf(cl.id) >= 0;
          return '<li class="' + (hecha ? "hecha" : "") + '"><a href="#/clase/' + esc(c.id) + "/" + esc(cl.id) + '">' +
            '<span class="estado" aria-label="' + (hecha ? "Completada" : "Pendiente") + '">' + (hecha ? "&#10003;" : "") + "</span>" +
            '<span><span class="etiqueta-clase">' + esc(cl.etiqueta) + "</span>" + esc(cl.titulo) + "</span>" +
            '<span class="semana">' + esc(duracionClase(cl)) + "</span></a></li>";
        }).join("") + "</ol>" + (plegable ? "</div></details>" : "</section>");
      });
      if (c.credito) html += '<p class="credito">' + esc(c.credito) + "</p>";
      pintar(html, c.titulo);
      activarSolicitudes();
      if (plegable) activarPlegables(c);
    });
  }

  // Módulos abiertos: lo que la persona dejó abierto en esta formación; si no hay nada guardado,
  // solo el módulo donde va (el de la próxima sesión), o el primero.
  function claveAbiertos(c) { return "miruta:abiertos:" + c.id; }
  function modulosAbiertos(c, siguiente) {
    var guardado = null;
    try { guardado = JSON.parse(sessionStorage.getItem(claveAbiertos(c)) || "null"); } catch (e) { guardado = null; }
    var a = {};
    if (guardado && guardado.length) { guardado.forEach(function (id) { a[id] = true; }); return a; }
    var actual = siguiente ? siguiente.modulo : null;
    var m = c.modulos.filter(function (x) { return x.id === (actual && actual.id || actual); })[0] || c.modulos[0];
    if (m) a[m.id] = true;
    return a;
  }
  function activarPlegables(c) {
    var guardar = function () {
      var ids = Array.prototype.map.call(document.querySelectorAll("details.plegable[open]"), function (d) { return d.getAttribute("data-modulo"); });
      try { sessionStorage.setItem(claveAbiertos(c), JSON.stringify(ids.length ? ids : ["-"])); } catch (e) { /* sin almacenamiento */ }
    };
    Array.prototype.forEach.call(document.querySelectorAll("details.plegable"), function (d) { d.addEventListener("toggle", guardar); });
    Array.prototype.forEach.call(document.querySelectorAll("[data-plegar]"), function (b) {
      b.addEventListener("click", function () {
        var abrir = b.getAttribute("data-plegar") === "abrir";
        Array.prototype.forEach.call(document.querySelectorAll("details.plegable"), function (d) { d.open = abrir; });
        guardar();
      });
    });
  }

  function vistaPrograma(id) {
    return Promise.all([cargarCurso(id), pedir("contenido/" + id + "/programa.md", "texto")]).then(function (r) {
      var c = r[0];
      var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" +
        '<article class="tarjeta texto"><h1>Programa</h1>' + md(r[1]) + "</article>";
      pintar(html, "Programa");
    });
  }

  function vistaSesiones(id) {
    return cargarCurso(id).then(function (c) {
      var general = (c.videollamada && c.videollamada.enlace) || "";
      var plataforma = (c.videollamada && c.videollamada.plataforma) || "videollamada";
      var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" +
        '<section class="tarjeta"><h1>Sesiones en vivo</h1><p>Los encuentros-taller son semanales. Cuando una sesión sea por ' + esc(plataforma) +
        ", el botón para entrar aparecerá aquí.</p>" +
        (general ? '<div class="botones"><a class="boton principal" href="' + esc(general) + '" target="_blank" rel="noopener">Entrar a la sala del curso</a></div>' : "") +
        '<ol class="sesiones">' + c.sesiones.map(function (s, k) {
          var titulo = "";
          if (s.modulo && (k === 0 || c.sesiones[k - 1].modulo !== s.modulo)) {
            var mod = c.modulos.filter(function (m) { return m.numero === s.modulo; })[0];
            titulo = '<li class="sesiones-modulo">' + esc(mod ? etiquetaModulo(mod) + ". " + mod.titulo : "Módulo " + s.modulo) + "</li>";
          }
          var cuando = [s.fecha, s.hora, s.lugar].filter(Boolean).join(" · ") || "Fecha por definir";
          var enlace = s.enlace || "";
          return titulo + '<li><span class="num">Semana ' + esc(s.semana) + '</span><span><span class="tema">' + esc(s.tema) +
            '</span><br><span class="cuando">' + esc(cuando) + "</span></span>" +
            (enlace ? '<a class="boton" href="' + esc(enlace) + '" target="_blank" rel="noopener">Entrar</a>' : "<span></span>") + "</li>";
        }).join("") + "</ol></section>";
      pintar(html, "Sesiones en vivo");
    });
  }

  function clasificar(titulo) {
    if (/^Gu[ií]a/i.test(titulo)) return "relator";
    if (/^Plantilla/i.test(titulo)) return "plantilla";
    if (/^(Aplicaci|Bit[aá]cora)/i.test(titulo)) return "aplicacion";
    if (/^Apunte/i.test(titulo)) return "apunte";
    return "otro";
  }

  function nombrePestana(titulo, tipo) {
    if (tipo === "relator") return "Guía del relator";
    if (tipo === "plantilla") return "Plantilla";
    if (tipo === "aplicacion") return /^Bit/i.test(titulo) ? "Bitácora final" : "Aplicación";
    return titulo.replace(/\s*\(.*\)\s*$/, "").replace(/:.*$/, "");
  }

  function vistaClase(cursoId, claseId) {
    var cursados = almacen.leer("cursados", []);
    if (cursados.indexOf(cursoId) < 0) almacen.guardar("cursados", cursados.concat([cursoId]));
    return cargarCurso(cursoId).then(function (c) {
      var i = -1;
      c.clases.forEach(function (x, k) { if (x.id === claseId) i = k; });
      if (i < 0) throw new Error("La clase no existe.");
      var cl = c.clases[i];
      var tipoAcceso = acceso(c);
      if (tipoAcceso !== "libre") {
        pintar('<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" +
          '<section class="tarjeta">' + bloqueAcceso(c, tipoAcceso) + "</section>", cl.titulo);
        activarSolicitudes();
        return;
      }
      var bloqueo = moduloBloqueado(c, cl.modulo);
      if (bloqueo) {
        pintar('<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" +
          '<section class="tarjeta"><h1>' + esc(etiquetaModulo(cl.modulo)) + " todavía no está disponible</h1><p>Para cursar este módulo primero debes completar " +
          bloqueo.map(function (r) { return esc(etiquetaModulo(r)) + ". " + esc(r.titulo); }).join(" y ") +
          '.</p><div class="botones"><a class="boton principal" href="#/curso/' + esc(c.id) + '">Volver al curso</a></div></section>', cl.titulo);
        return;
      }
      if (cl.tipo === "evaluacion") {
        return pedir("datos/evaluaciones-" + cursoId + ".json").then(function (ev) {
          if (!ev[cl.id]) throw new Error("La evaluación no existe.");
          armarEvaluacion(c, cl, i, ev[cl.id]);
        });
      }
      return pedir(cl.archivo || "contenido/" + cursoId + "/" + claseId + ".md", "texto").then(function (texto) {
        armarClase(c, cl, i, texto);
      });
    });
  }

  function armarClase(c, cl, i, texto) {
    var partes = texto.split(/^### (.+)$/m);
    var intro = partes[0].trim();
    var secciones = [];
    for (var k = 1; k < partes.length; k += 2) {
      var tipo = clasificar(partes[k].trim());
      secciones.push({ titulo: partes[k].trim(), tipo: tipo, nombre: nombrePestana(partes[k].trim(), tipo), cuerpo: partes[k + 1] || "" });
    }
    var relator = modoRelator();
    var visibles = secciones.filter(function (s) { return relator || s.tipo !== "relator"; });
    var ocultas = secciones.length - visibles.length;
    var rec = (c.recursos && c.recursos[cl.id]) || {};
    var video = enlaceVideo(rec.video);
    var pres = enlacePresentacion(rec.presentacion);
    var hecha = hechas(c.id).indexOf(cl.id) >= 0;

    var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" + avisosPlazo(c, false);
    html += '<header class="clase-cabecera"><span class="etiqueta-clase">' + esc(etiquetaModulo(cl.modulo)) + " · " + esc(cl.etiqueta) + "</span>" +
      "<h1>" + esc(cl.titulo) + '</h1><p class="meta">' + esc(duracionClase(cl)) + "</p></header>";
    if (intro) html += '<div class="texto">' + md(intro) + "</div>";
    if (video) html += '<div class="medio"><iframe src="' + esc(video) + '" title="Video de la clase" allowfullscreen loading="lazy"></iframe></div>';
    if (pres) html += '<div class="medio"><iframe src="' + esc(pres) + '" title="Presentación de la clase" allowfullscreen loading="lazy"></iframe></div>';
    else if (rec.presentacion) html += '<p><a class="boton" href="' + esc(rec.presentacion) + '" target="_blank" rel="noopener">Abrir la presentación</a></p>';

    html += '<div class="pestanas" role="tablist">' + visibles.map(function (s, k) {
      return '<button class="pestana' + (s.tipo === "relator" ? " relator" : "") + '" role="tab" id="pes-' + k + '" aria-controls="pan-' + k +
        '" aria-selected="' + (k === 0) + '">' + esc(s.nombre) + "</button>";
    }).join("") + "</div>";

    html += visibles.map(function (s, k) {
      var extra = "";
      if (s.tipo === "relator") extra = '<p class="aviso-relator">Esta guía es para quien conduce el encuentro-taller.</p>';
      var acciones = "";
      if (s.tipo === "plantilla") {
        acciones = '<p class="aviso">Puedes escribir en las casillas vacías de las tablas. Se guardan en este dispositivo.</p>' +
          '<div class="panel-acciones"><button class="boton" data-accion="imprimir">Imprimir plantilla</button>' +
          '<button class="boton" data-accion="limpiar">Borrar lo escrito</button></div>';
      }
      if (s.tipo === "aplicacion") {
        acciones = '<div class="bitacora"><label for="bitacora">Mi bitácora</label>' +
          '<textarea id="bitacora" placeholder="Qué hice esta semana, qué funcionó, qué ajustaría…"></textarea>' +
          '<div class="guardado" aria-live="polite"></div></div>';
      }
      return '<section class="panel texto" role="tabpanel" id="pan-' + k + '" aria-labelledby="pes-' + k + '" data-tipo="' + s.tipo + '"' + (k === 0 ? "" : " hidden") + ">" +
        "<h2>" + esc(s.titulo) + "</h2>" + extra + md(s.cuerpo) + acciones + "</section>";
    }).join("");

    if (ocultas) html += '<p class="aviso">Esta clase incluye una guía para el relator. Si eres relator o administrador, actívala con el interruptor «Vista relator» de la parte superior.</p>';

    if (/-cierre$/.test(cl.id)) html += '<section class="tarjeta video-final" id="video-final"></section>';
    html += '<section class="tarjeta debate-clase" id="debate-clase"></section>';
    html += '<p class="reportar"><a href="#/sugerencias?desde=' + encodeURIComponent(location.hash) + '">¿Encontraste un error o tienes una sugerencia sobre esta sesión? Avísanos</a></p>';
    html += '<div class="botones"><button class="boton ' + (hecha ? "hecho" : "principal") + '" id="marcar">' +
      (hecha ? "&#10003; Clase completada" : "Marcar como completada") + "</button></div>";

    html += franjaAgappe(c) + navegacionClases(c, i);

    pintar(html, cl.titulo);
    activarClase(c, cl);
    cargarDebateClase(c, cl);
    if (/-cierre$/.test(cl.id)) cargarVideoFinal(c, cl.modulo);
  }

  function activarClase(c, cl) {
    var pestanas = app.querySelectorAll(".pestana");
    var paneles = app.querySelectorAll(".panel");
    var claveTab = "pestana:" + cl.id;

    function mostrar(k) {
      pestanas.forEach(function (p, j) { p.setAttribute("aria-selected", String(j === k)); });
      paneles.forEach(function (p, j) { p.hidden = j !== k; });
      almacen.guardar(claveTab, k);
    }
    pestanas.forEach(function (p, k) { p.addEventListener("click", function () { mostrar(k); }); });
    var guardada = almacen.leer(claveTab, 0);
    if (guardada > 0 && guardada < pestanas.length) mostrar(guardada);

    // Tareas con casilla
    var tareas = almacen.leer("tareas:" + cl.id, {});
    app.querySelectorAll('.panel input[type="checkbox"]').forEach(function (cb, k) {
      cb.disabled = false;
      var li = cb.closest("li");
      if (li) li.classList.add("tarea");
      cb.checked = !!tareas[k];
      if (li) li.classList.toggle("marcada", cb.checked);
      cb.addEventListener("change", function () {
        tareas[k] = cb.checked;
        almacen.guardar("tareas:" + cl.id, tareas);
        if (li) li.classList.toggle("marcada", cb.checked);
      });
    });

    // Casillas editables en las plantillas
    var campos = almacen.leer("plantilla:" + cl.id, {});
    app.querySelectorAll('.panel[data-tipo="plantilla"] td').forEach(function (td, k) {
      if (td.textContent.trim() !== "") return;
      td.classList.add("campo");
      td.setAttribute("contenteditable", "true");
      td.dataset.k = k;
      if (campos[k]) td.textContent = campos[k];
      td.addEventListener("input", function () {
        campos[k] = td.textContent;
        almacen.guardar("plantilla:" + cl.id, campos);
      });
    });

    app.querySelectorAll('[data-accion="imprimir"]').forEach(function (b) {
      b.addEventListener("click", function () { window.print(); });
    });
    app.querySelectorAll('[data-accion="limpiar"]').forEach(function (b) {
      b.addEventListener("click", function () {
        app.querySelectorAll("td.campo").forEach(function (td) { td.textContent = ""; });
        campos = {};
        almacen.guardar("plantilla:" + cl.id, campos);
      });
    });

    // Bitácora
    var ta = document.getElementById("bitacora");
    if (ta) {
      var aviso = ta.parentNode.querySelector(".guardado");
      var temporizador;
      ta.value = almacen.leer("bitacora:" + cl.id, "");
      ta.addEventListener("input", function () {
        clearTimeout(temporizador);
        temporizador = setTimeout(function () {
          almacen.guardar("bitacora:" + cl.id, ta.value);
          aviso.textContent = "Guardado en este dispositivo";
        }, 400);
      });
    }

    var marcar = document.getElementById("marcar");
    marcar.addEventListener("click", function () {
      var ahora = hechas(c.id).indexOf(cl.id) < 0;
      marcarHecha(c.id, cl.id, ahora);
      marcar.className = "boton " + (ahora ? "hecho" : "principal");
      marcar.innerHTML = ahora ? "&#10003; Clase completada" : "Marcar como completada";
    });
  }

  /* ---------- muro de cada formación ---------- */

  // Con Firebase usa la nube; sin configuración, guarda en este navegador (para probar).
  var Foro = {
    leer: function (c) {
      if (Nube.habilitada) return Nube.leerForo(c);
      try { return Promise.resolve(JSON.parse(localStorage.getItem("agp:foro:" + c) || "{}")); } catch (e) { return Promise.resolve({}); }
    },
    guardar: function (c, cambios) {
      if (Nube.habilitada) return Nube.guardarForo(c, cambios);
      return Foro.leer(c).then(function (f) { localStorage.setItem("agp:foro:" + c, JSON.stringify(Object.assign(f, cambios))); });
    },
    mensajes: function (c) {
      if (Nube.habilitada) return Nube.mensajesCurso(c);
      try { return Promise.resolve(JSON.parse(localStorage.getItem("agp:foro-msg:" + c) || "[]")); } catch (e) { return Promise.resolve([]); }
    },
    publicar: function (c, hilo, texto) {
      if (Nube.habilitada) return Nube.publicarMensaje(c, hilo, texto);
      return Foro.mensajes(c).then(function (l) {
        l.push({ id: "m" + Date.now(), hilo: hilo, texto: texto, uid: "local", nombre: modoRelator() ? "Relator (prueba)" : "Tú", rol: modoRelator() ? "relator" : "participante", fecha: new Date().toISOString(), borrado: false });
        localStorage.setItem("agp:foro-msg:" + c, JSON.stringify(l));
      });
    },
    borrar: function (c, id) {
      if (Nube.habilitada) return Nube.borrarMensaje(c, id);
      return Foro.mensajes(c).then(function (l) {
        l.forEach(function (m) { if (m.id === id) { m.borrado = true; m.texto = ""; } });
        localStorage.setItem("agp:foro-msg:" + c, JSON.stringify(l));
      });
    },
  };

  function yoForo() {
    if (!Nube.habilitada) return { uid: "local", equipo: modoRelator() };
    var e = cuentaActual();
    return { uid: e.cuenta ? e.cuenta.uid : "", equipo: !!e.esRelator };
  }
  function debatibles(c) { return c.clases.filter(function (x) { return x.tipo !== "evaluacion"; }); }
  var PREGUNTA_DEF = "¿Qué idea de esta sesión te parece más importante para tu servicio, y cómo la pondrías en práctica? Después, responde al aporte de algún compañero.";
  function bienvenidaDef(c) {
    return "¡Bienvenidos y bienvenidas a " + c.titulo + "! Este es el espacio de nuestra comunidad de curso. Para comenzar, preséntate: tu nombre, tu comunidad o parroquia, en qué sirves y qué esperas de esta formación.";
  }
  function directricesDef(f) {
    return "- Avanza a tu ritmo, procurando completar al menos una sesión por semana.\n" +
      "- Participa en el debate de cada sesión: comparte tu aporte y responde al de al menos un compañero." + (f.obligatorio ? " **La participación es obligatoria para completar cada sesión.**" : "") + "\n" +
      "- Escribe con respeto y caridad: aquí todos aprendemos de todos.\n" +
      "- Cuida la privacidad: no publiques datos personales ni situaciones de terceros, especialmente de menores.\n" +
      "- Las dudas sobre el programa escríbelas en este mismo espacio; tu relator te responderá.\n" +
      "- Para aprobar cada módulo: completar sus sesiones, el taller y la evaluación de cierre" + (f.obligatorio ? ", y participar en sus debates." : ".");
  }
  function fechaCorta(iso) {
    try { return new Date(iso).toLocaleString("es-CL", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); } catch (e) { return ""; }
  }
  function participoEn(msgs, uid, hilo) {
    return msgs.some(function (m) { return m.hilo === hilo && m.uid === uid && !m.borrado; });
  }

  function hiloHTML(msgs, hilo, placeholder, yo) {
    var lista = msgs.filter(function (m) { return m.hilo === hilo; }).sort(function (a, b) { return String(a.fecha).localeCompare(String(b.fecha)); });
    return '<div class="hilo">' + (lista.length ? lista.map(function (m) {
      if (m.borrado) return '<article class="msg borrado"><p>Mensaje eliminado.</p></article>';
      var propio = m.uid === yo.uid;
      return '<article class="msg' + (m.rol === "relator" || m.rol === "admin" ? " msg-equipo" : "") + '"><header><b>' + esc(m.nombre || "Participante") + "</b>" +
        (m.rol === "relator" || m.rol === "admin" ? '<span class="msg-rol">Relator</span>' : "") + "<time>" + esc(fechaCorta(m.fecha)) + "</time>" +
        (propio || yo.equipo ? '<button class="msg-borrar" type="button" data-borrar="' + esc(m.id) + '">Borrar</button>' : "") + "</header>" +
        "<p>" + esc(m.texto).replace(/\n/g, "<br>") + "</p></article>";
    }).join("") : '<p class="seccion-bajada">Todavía no hay mensajes. ¡Sé el primero!</p>') + "</div>" +
      '<form class="msg-form" data-hilo="' + esc(hilo) + '"><textarea maxlength="3000" required placeholder="' + esc(placeholder) + '"></textarea>' +
      '<div class="botones"><button class="boton principal" type="submit">Publicar</button></div><div class="mensaje" aria-live="polite"></div></form>';
  }

  function textoEditable(id, titulo, texto, yo, filas) {
    return '<div class="muro-texto" data-editable="' + esc(id) + '">' + (titulo ? "<h3>" + esc(titulo) + "</h3>" : "") +
      '<div class="texto">' + md(texto) + "</div>" +
      (yo.equipo ? '<div class="muro-editar" hidden><textarea rows="' + (filas || 5) + '">' + esc(texto) + '</textarea><div class="botones"><button class="boton principal" type="button" data-guardar>Guardar</button><button class="boton" type="button" data-cancelar>Cancelar</button></div><div class="mensaje" aria-live="polite"></div></div>' +
        '<button class="boton boton-chico" type="button" data-editar>Editar</button>' : "") + "</div>";
  }

  function activarMuro(c, alGuardar) {
    var yo = yoForo();
    app.querySelectorAll(".msg-form").forEach(function (f) {
      f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var ta = f.querySelector("textarea"), msj = f.querySelector(".mensaje"), b = f.querySelector("button");
        var texto = ta.value.trim();
        if (!texto) return;
        b.disabled = true; msj.className = "mensaje"; msj.textContent = "Publicando…";
        Foro.publicar(c.id, f.getAttribute("data-hilo"), texto).then(ruta).catch(function (er) { b.disabled = false; msj.className = "mensaje error"; msj.textContent = er.message; });
      });
    });
    app.querySelectorAll("[data-borrar]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (b.getAttribute("data-seguro") !== "1") { b.setAttribute("data-seguro", "1"); b.textContent = "¿Borrar? Confirmar"; return; }
        Foro.borrar(c.id, b.getAttribute("data-borrar")).then(ruta).catch(function (er) { b.textContent = er.message; });
      });
    });
    app.querySelectorAll("[data-editable]").forEach(function (box) {
      var ed = box.querySelector(".muro-editar"), bEd = box.querySelector("[data-editar]");
      if (!ed) return;
      bEd.addEventListener("click", function () { ed.hidden = false; bEd.hidden = true; });
      box.querySelector("[data-cancelar]").addEventListener("click", function () { ed.hidden = true; bEd.hidden = false; });
      box.querySelector("[data-guardar]").addEventListener("click", function () {
        var msj = ed.querySelector(".mensaje");
        msj.className = "mensaje"; msj.textContent = "Guardando…";
        alGuardar(box.getAttribute("data-editable"), ed.querySelector("textarea").value.trim()).then(ruta)
          .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
      });
    });
    var vi = document.getElementById("muro-video");
    if (vi) vi.addEventListener("change", function () { Foro.guardar(c.id, { video: vi.checked }).then(ruta); });
    var ob = document.getElementById("muro-obligatorio");
    if (ob) ob.addEventListener("change", function () { Foro.guardar(c.id, { obligatorio: ob.checked }).then(ruta); });
    void yo;
  }

  function vistaMuro(cursoId, seccion, claseId) {
    return Promise.all([cargarCurso(cursoId), Foro.leer(cursoId), Foro.mensajes(cursoId)]).then(function (r) {
      var c = r[0], f = r[1] || {}, msgs = r[2] || [];
      var tipoAcceso = acceso(c);
      if (tipoAcceso !== "libre") { location.hash = "#/curso/" + c.id; return; }
      var base = cabeceraAula(c, "muro");
      var yo = yoForo();
      var preguntas = f.preguntas || {};
      seccion = seccion || "bienvenida";
      var pest = [["bienvenida", "Bienvenida y presentaciones"], ["programa", "Programa y directrices"], ["debates", "Debates por sesión"]];
      var html = base +
        '<nav class="pestanas-inicio muro-pestanas">' + pest.map(function (p) {
          return '<a class="pestana-enlace" href="#/curso/' + esc(c.id) + "/muro/" + p[0] + '" aria-current="' + (seccion === p[0] || (seccion === "s" && p[0] === "debates")) + '">' + p[1] + "</a>";
        }).join("") + "</nav>";

      if (seccion === "bienvenida") {
        html += '<section class="tarjeta">' + textoEditable("bienvenida", "Palabras del relator", f.bienvenida || bienvenidaDef(c), yo, 4) + "</section>" +
          '<section class="tarjeta"><h2>Presentaciones</h2>' + hiloHTML(msgs, "bienvenida", "Preséntate: tu nombre, tu comunidad, en qué sirves y qué esperas de esta formación.", yo) + "</section>";
      } else if (seccion === "programa") {
        var cont = c.contenidos || [];
        html += '<section class="tarjeta"><h2>Programa</h2><ul class="etiquetas claras"><li>' + esc(c.duracion) + "</li><li>" + esc(c.modalidad) + "</li>" + (c.publico ? "<li>" + esc(c.publico) + "</li>" : "") + "</ul>" +
          (c.descripcion ? "<p>" + esc(c.descripcion) + "</p>" : "") +
          (c.competencias && c.competencias.length ? "<h3>Competencias</h3><ul>" + c.competencias.map(function (x) { return "<li>" + enfasis(x) + "</li>"; }).join("") + "</ul>" : "") +
          (cont.length ? "<h3>" + (c.tipo === "curso" ? "Módulos" : "Sesiones") + '</h3><ol class="ficha-indice">' + cont.map(function (x) { return "<li>" + esc(x.titulo) + (x.tipo === "optativo" ? " (optativo)" : "") + "</li>"; }).join("") + "</ol>" : "") +
          '<p><a class="boton" href="#/curso/' + esc(c.id) + '">Ver la formación completa</a></p></section>' +
          '<section class="tarjeta">' + textoEditable("directrices", "Directrices", f.directrices || directricesDef(f), yo, 8) +
          (yo.equipo ? '<label class="interruptor-muro"><input type="checkbox" id="muro-obligatorio"' + (f.obligatorio ? " checked" : "") + "> Participación obligatoria en los debates: sin participar, el participante no puede marcar la sesión como completada.</label>" : "") + "</section>" +
          (f.video || yo.equipo ? '<section class="tarjeta"><h2>Presentación final en video</h2>' +
            (yo.equipo ? '<label class="interruptor-muro"><input type="checkbox" id="muro-video"' + (f.video ? " checked" : "") + "> Pedir en cada módulo una presentación grabada en YouTube, evaluada con rúbrica.</label>" : "") +
            (f.video ? '<p>Al cierre de cada módulo grabas una presentación de 3 a 5 minutos y envías el enlace de YouTube en la sesión de cierre. Tu relator la evalúa con esta rúbrica:</p>' + rubricaHTML() +
              (yo.equipo ? "<h3>Consignas por módulo</h3>" + c.modulos.map(function (m) { return textoEditable("consigna:" + m.id, etiquetaModulo(m) + ". " + m.titulo, (f.consignas || {})[m.id] || consignaDef(m), yo, 6); }).join("") +
                '<p><a class="boton principal" href="#/curso/' + esc(c.id) + '/entregas">Revisar presentaciones</a></p>' : "") : "") + "</section>" : "") +
          '<section class="tarjeta"><h2>Dudas sobre el programa</h2>' + hiloHTML(msgs, "programa", "Escribe tu duda sobre el programa o las directrices.", yo) + "</section>";
      } else if (seccion === "s" && claseId) {
        var cl = c.clases.filter(function (x) { return x.id === claseId; })[0];
        if (!cl) { location.hash = "#/curso/" + c.id + "/muro/debates"; return; }
        html += '<section class="tarjeta"><p class="etiqueta-clase">' + esc(etiquetaModulo(cl.modulo)) + " · " + esc(cl.etiqueta || "") + "</p><h2>" + esc(cl.titulo) + "</h2>" +
          textoEditable("pregunta:" + cl.id, "Para el debate", preguntas[cl.id] || cl.debate || PREGUNTA_DEF, yo, 9) +
          (f.obligatorio ? '<p class="aviso">La participación en este debate es obligatoria para completar la sesión.</p>' : "") +
          '<p><a class="boton" href="#/clase/' + esc(c.id) + "/" + esc(cl.id) + '">Ir a la sesión</a></p></section>' +
          '<section class="tarjeta"><h2>Debate</h2>' + hiloHTML(msgs, cl.id, "Comparte tu aporte o responde a un compañero.", yo) + "</section>";
      } else {
        var deb = debatibles(c);
        var mios = deb.filter(function (x) { return participoEn(msgs, yo.uid, x.id); }).length;
        html += '<section class="tarjeta como-debate"><h2>Cómo funcionan los debates</h2><ol>' +
          "<li><b>Estudia la sesión</b> en la pestaña Contenido.</li>" +
          "<li><b>Vuelve aquí</b> y entra al debate de esa sesión: verás un caso o una pregunta sobre lo que estudiaste.</li>" +
          "<li><b>Comparte tu respuesta</b> y lee las de tus compañeros. Responde al menos a uno: así aprendemos juntos.</li></ol>" +
          (f.obligatorio ? '<p class="aviso">En esta formación participar es obligatorio: hasta que escribas en el debate de una sesión, no podrás marcarla como completada.</p>' : "") + "</section>" +
          '<section class="tarjeta"><h2>Debates por sesión</h2>' +
          (yo.equipo ? "" : '<p class="ficha-nota">Participaste en ' + mios + " de " + deb.length + " debates.</p>") +
          c.modulos.map(function (m) {
            var cls = m.clases.filter(function (x) { return x.tipo !== "evaluacion"; });
            if (!cls.length) return "";
            return "<h3>" + esc(etiquetaModulo(m)) + ". " + esc(m.titulo) + '</h3><ul class="debates-lista">' + cls.map(function (x) {
              var n = msgs.filter(function (m2) { return m2.hilo === x.id && !m2.borrado; }).length;
              var yoSi = participoEn(msgs, yo.uid, x.id);
              return '<li><a href="#/curso/' + esc(c.id) + "/muro/s/" + esc(x.id) + '"><span>' + esc(x.etiqueta || "") + ". " + esc(x.titulo) + '</span><span class="debate-estado">' + n + (n === 1 ? " mensaje" : " mensajes") +
                (yo.equipo ? "" : (yoSi ? ' · <b class="ok">Participaste</b>' : (f.obligatorio ? ' · <b class="pendiente">Pendiente</b>' : ""))) + "</span></a></li>";
            }).join("") + "</ul>";
          }).join("") + "</section>";
      }
      pintar(html, "Muro · " + c.titulo);
      activarMuro(c, function (id, texto) {
        if (id.indexOf("pregunta:") === 0) { var p = Object.assign({}, preguntas); p[id.slice(9)] = texto; return Foro.guardar(c.id, { preguntas: p }); }
        if (id.indexOf("consigna:") === 0) { var q = Object.assign({}, f.consignas || {}); q[id.slice(9)] = texto; return Foro.guardar(c.id, { consignas: q }); }
        var cambio = {}; cambio[id] = texto; return Foro.guardar(c.id, cambio);
      });
    });
  }

  // Resumen del muro en la página de la formación.
  function cargarResumenMuro(c) {
    var caja = document.getElementById("muro-curso");
    if (!caja) return;
    Promise.all([Foro.leer(c.id), Foro.mensajes(c.id)]).then(function (r) {
      var f = r[0] || {}, msgs = (r[1] || []).filter(function (m) { return !m.borrado; }), yo = yoForo();
      var deb = debatibles(c);
      var nB = msgs.filter(function (m) { return m.hilo === "bienvenida"; }).length;
      var mios = deb.filter(function (x) { return participoEn(msgs, yo.uid, x.id); }).length;
      var u = "#/curso/" + esc(c.id) + "/muro/";
      caja.innerHTML = '<h2 class="seccion-titulo">Muro del curso</h2><div class="muro-accesos">' +
        '<a href="' + u + 'bienvenida"><b>Bienvenida y presentaciones</b><span>' + nB + (nB === 1 ? " presentación" : " presentaciones") + "</span></a>" +
        '<a href="' + u + 'programa"><b>Programa y directrices</b><span>Lo que se espera de ti en esta formación</span></a>' +
        '<a href="' + u + 'debates"><b>Debates por sesión</b><span>' + (yo.equipo ? deb.length + " debates" : "Participaste en " + mios + " de " + deb.length) + (f.obligatorio ? " · obligatorio" : "") + "</span></a></div>";
    }).catch(function () { caja.remove(); });
  }

  // Debate de la sesión, al final de cada clase. Si es obligatorio, sin participar no se puede marcar como completada.
  function cargarDebateClase(c, cl) {
    var caja = document.getElementById("debate-clase");
    if (!caja || cl.tipo === "evaluacion") { if (caja) caja.remove(); return; }
    Promise.all([Foro.leer(c.id), Foro.mensajes(c.id)]).then(function (r) {
      var f = r[0] || {}, msgs = (r[1] || []).filter(function (m) { return !m.borrado; }), yo = yoForo();
      var n = msgs.filter(function (m) { return m.hilo === cl.id; }).length;
      var yoSi = participoEn(msgs, yo.uid, cl.id);
      var pregunta = (f.preguntas || {})[cl.id] || cl.debate || PREGUNTA_DEF;
      void pregunta;
      caja.className = "recordatorio-debate";
      caja.innerHTML = "Esta sesión tiene un debate en el muro de la formación (" + n + (n === 1 ? " mensaje" : " mensajes") + ")" + (yo.equipo ? "" : (yoSi ? ". Ya participaste." : (f.obligatorio ? ". <b>Participar es obligatorio para completarla.</b>" : "."))) +
        ' <a href="#/curso/' + esc(c.id) + "/muro/s/" + esc(cl.id) + '">' + (yoSi || yo.equipo ? "Ver el debate" : "Ir al debate") + "</a>";
      var marcar = document.getElementById("marcar");
      if (f.obligatorio && !yo.equipo && !yoSi && marcar && hechas(c.id).indexOf(cl.id) < 0) {
        marcar.disabled = true;
        marcar.title = "Primero participa en el debate de esta sesión";
        marcar.insertAdjacentHTML("afterend", '<span class="ficha-nota marcar-nota">Para completar esta sesión, primero participa en su debate.</span>');
      }
    }).catch(function () { caja.remove(); });
  }

  /* ---------- presentación final en video (YouTube) ---------- */

  var RUBRICA = [
    { id: "contenido", nombre: "Dominio del contenido", peso: 30, niveles: [
      "No se apoya en los contenidos del módulo o tiene errores importantes.",
      "Menciona ideas del módulo de forma superficial o con errores.",
      "Explica las ideas centrales, con pequeñas imprecisiones.",
      "Explica con precisión las ideas centrales del módulo y las relaciona entre sí."] },
    { id: "consigna", nombre: "Respuesta a la consigna y aplicación", peso: 30, niveles: [
      "No responde a la consigna.",
      "Responde parcialmente o con propuestas genéricas.",
      "Responde la consigna con propuestas adecuadas, pero poco desarrolladas.",
      "Responde por completo o resuelve el caso con propuestas concretas, realistas y fundamentadas."] },
    { id: "orden", nombre: "Organización y claridad", peso: 20, niveles: [
      "Sin estructura reconocible.",
      "Desordenada o muy fuera del tiempo pedido.",
      "Estructura reconocible, con algunos saltos o levemente fuera de tiempo.",
      "Introducción, desarrollo y cierre claros; respeta el tiempo (3 a 5 minutos)."] },
    { id: "comunicacion", nombre: "Comunicación", peso: 20, niveles: [
      "No se entiende.",
      "Cuesta seguirla: audio o imagen deficientes, o lectura textual.",
      "Se entiende bien, con detalles mejorables.",
      "Habla con claridad, buen volumen y lenguaje adecuado; mira a cámara; audio e imagen se entienden bien."] },
  ];
  var NIVELES = ["Insuficiente", "Suficiente", "Bueno", "Logrado"];
  var APRUEBA_VIDEO = 70;
  function notaRubrica(crit) {
    var t = 0;
    RUBRICA.forEach(function (r) { t += r.peso * (Number(crit[r.id]) || 0) / 4; });
    return Math.round(t);
  }
  function consignaDef(m) {
    return "Elige **una** de estas dos opciones y grábate en un video de **3 a 5 minutos**:\n\n" +
      "**A. Pregunta de desarrollo.** Explica con tus palabras la idea central del módulo «" + m.titulo + "» y cómo cambia tu manera de servir. Da un ejemplo concreto de tu comunidad.\n\n" +
      "**B. Resolver una problemática.** Toma el caso del taller de cierre de este módulo y explica qué harías, paso a paso, y por qué, apoyándote en lo visto en las sesiones.";
  }
  function rubricaHTML() {
    return '<div class="tabla-rubrica"><table><thead><tr><th>Criterio</th>' + NIVELES.slice().reverse().map(function (n, k) { return "<th>" + n + " (" + (4 - k) + ")</th>"; }).join("") + "</tr></thead><tbody>" +
      RUBRICA.map(function (r) {
        return "<tr><th>" + esc(r.nombre) + "<small>" + r.peso + " %</small></th>" + r.niveles.slice().reverse().map(function (d) { return "<td>" + esc(d) + "</td>"; }).join("") + "</tr>";
      }).join("") + '</tbody></table></div><p class="ficha-nota">Se aprueba con ' + APRUEBA_VIDEO + " % o más.</p>";
  }
  var GUIA_YOUTUBE = '<details class="guia-youtube"><summary>Cómo subir tu video a YouTube</summary><ol>' +
    "<li>Entra a YouTube con tu cuenta de Google. Si no tienes canal, toca tu foto → <b>Crear un canal</b> (puede llevar tu nombre).</li>" +
    "<li>Toca <b>Crear → Subir video</b> y elige tu grabación. Puedes grabar con el celular en horizontal, en un lugar silencioso y con buena luz.</li>" +
    "<li>En <b>Visibilidad</b> elige <b>No listado</b>: solo lo ve quien tenga el enlace. No uses «Privado», porque tu relator no podría verlo.</li>" +
    "<li>Toca <b>Compartir → Copiar enlace</b> y pégalo aquí abajo.</li></ol>" +
    '<p class="ficha-nota">Cuida la privacidad: no muestres a otras personas sin su permiso, sobre todo a menores, ni datos personales. Si eres menor de edad, hazlo con un adulto responsable.</p></details>';

  var Entregas = {
    leer: function (c, m) {
      if (Nube.habilitada) return Nube.leerEntrega(c, m);
      return Promise.resolve(Entregas._local()[c + "~" + m + "~local"] || null);
    },
    enviar: function (c, m, url, com) {
      if (Nube.habilitada) return Nube.enviarEntrega(c, m, url, com);
      var t = Entregas._local(), id = c + "~" + m + "~local";
      t[id] = Object.assign(t[id] || {}, { id: id, curso: c, modulo: m, uid: "local", nombre: "Tú", url: url, comentario: com, fecha: new Date().toISOString() });
      localStorage.setItem("agp:entregas", JSON.stringify(t)); return Promise.resolve();
    },
    delCurso: function (c) {
      if (Nube.habilitada) return Nube.entregasCurso(c);
      var t = Entregas._local();
      return Promise.resolve(Object.keys(t).map(function (k) { return Object.assign({ id: k }, t[k]); }).filter(function (x) { return x.curso === c; }));
    },
    evaluar: function (id, ev) {
      if (Nube.habilitada) return Nube.evaluarEntrega(id, ev);
      var t = Entregas._local();
      t[id].evaluacion = Object.assign({}, ev, { porNombre: "Relator (prueba)", fecha: new Date().toISOString() });
      localStorage.setItem("agp:entregas", JSON.stringify(t)); return Promise.resolve();
    },
    _local: function () { try { return JSON.parse(localStorage.getItem("agp:entregas") || "{}"); } catch (e) { return {}; } },
  };
  function esYoutube(u) { return /^https:\/\/(www\.|m\.)?(youtube\.com|youtu\.be)\/.+/.test(u); }
  function idYoutube(u) {
    var m = String(u).match(/(?:youtu\.be\/|v=|shorts\/|embed\/|live\/)([\w-]{11})/);
    return m ? m[1] : "";
  }
  function estadoEntrega(e) {
    if (!e) return "Sin enviar";
    if (!e.evaluacion) return "Enviada, en revisión";
    return (e.evaluacion.nota >= APRUEBA_VIDEO ? "Aprobada" : "Por mejorar") + " · " + e.evaluacion.nota + " %";
  }

  // Sección en la sesión de cierre de cada módulo.
  function cargarVideoFinal(c, m) {
    var caja = document.getElementById("video-final");
    if (!caja) return;
    Promise.all([Foro.leer(c.id), Entregas.leer(c.id, m.id)]).then(function (r) {
      var f = r[0] || {}, e = r[1], yo = yoForo();
      if (!f.video) { caja.remove(); return; }
      var consigna = (f.consignas || {})[m.id] || consignaDef(m);
      var ev = e && e.evaluacion;
      var html = '<h2>Presentación final en video</h2><div class="texto">' + md(consigna) + "</div>" +
        '<details class="guia-youtube"><summary>Rúbrica de evaluación</summary>' + rubricaHTML() + "</details>" + GUIA_YOUTUBE;
      if (yo.equipo && Nube.habilitada) {
        html += '<p><a class="boton principal" href="#/curso/' + esc(c.id) + '/entregas">Revisar las presentaciones de esta formación</a></p>';
      } else {
        html += '<p class="estado-entrega"><b>Estado:</b> ' + esc(estadoEntrega(e)) + "</p>";
        if (ev) {
          html += '<div class="evaluacion-video"><h3>Evaluación de ' + esc(ev.porNombre || "tu relator") + "</h3><ul>" + RUBRICA.map(function (rr) {
            var n = Number(ev.criterios && ev.criterios[rr.id]) || 0;
            return "<li><b>" + esc(rr.nombre) + ":</b> " + (n ? NIVELES[n - 1] + " (" + n + ")" : "—") + "</li>";
          }).join("") + "</ul>" + (ev.retro ? '<p class="retro-video">' + esc(ev.retro).replace(/\n/g, "<br>") + "</p>" : "") + "</div>";
        }
        html += '<form id="form-video" class="formulario"><label>Enlace de tu video en YouTube<input name="url" type="url" required placeholder="https://youtu.be/…" value="' + esc(e ? e.url : "") + '"></label>' +
          '<label>Comentario para tu relator (opcional)<textarea name="comentario" maxlength="1000" rows="2">' + esc(e ? e.comentario || "" : "") + "</textarea></label>" +
          '<div class="botones"><button class="boton principal" type="submit">' + (e ? "Actualizar enlace" : "Enviar mi presentación") + '</button></div><div class="mensaje" aria-live="polite"></div></form>';
      }
      caja.innerHTML = html;
      var form = document.getElementById("form-video");
      if (form) form.addEventListener("submit", function (evt) {
        evt.preventDefault();
        var url = form.url.value.trim(), msj = form.querySelector(".mensaje");
        if (!esYoutube(url)) { msj.className = "mensaje error"; msj.textContent = "Pega un enlace de YouTube (youtube.com o youtu.be)."; return; }
        msj.className = "mensaje"; msj.textContent = "Enviando…";
        Entregas.enviar(c.id, m.id, url, form.comentario.value.trim()).then(function () { cargarVideoFinal(c, m); })
          .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
      });
    }).catch(function () { caja.remove(); });
  }

  // Página del equipo para revisar y evaluar las presentaciones de una formación.
  function vistaEntregas(cursoId) {
    var yo = yoForo();
    return Promise.all([cargarCurso(cursoId), Entregas.delCurso(cursoId)]).then(function (r) {
      var c = r[0], lista = r[1] || [];
      var base = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a> / Presentaciones</nav>";
      if (!yo.equipo) { pintar(base + '<section class="tarjeta"><p>Esta página es para relatores y administradores.</p></section>', "Presentaciones"); return; }
      var html = base + '<header class="muro-cabecera"><h1>Presentaciones en video</h1><p class="seccion-bajada">' + esc(c.titulo) + "</p></header>" +
        '<details class="guia-youtube"><summary>Rúbrica</summary>' + rubricaHTML() + "</details>";
      c.modulos.forEach(function (m) {
        var es = lista.filter(function (x) { return x.modulo === m.id; }).sort(function (a, b) { return String(a.nombre).localeCompare(String(b.nombre)); });
        html += '<section class="tarjeta"><h2>' + esc(etiquetaModulo(m)) + ". " + esc(m.titulo) + '</h2><p class="ficha-nota">' + es.length + (es.length === 1 ? " presentación" : " presentaciones") + "</p>" +
          es.map(function (x) {
            var ev = x.evaluacion || {}, crit = ev.criterios || {}, vid = idYoutube(x.url);
            return '<article class="entrega" data-id="' + esc(x.id) + '"><header><b>' + esc(x.nombre || "Participante") + "</b><span>" + esc(estadoEntrega(x)) + "</span></header>" +
              '<p><a href="' + esc(x.url) + '" target="_blank" rel="noopener">Abrir en YouTube</a>' + (vid ? ' · <button class="enlace-boton" type="button" data-ver="' + esc(vid) + '">Ver aquí</button>' : "") + "</p>" +
              '<div class="video-marco" hidden></div>' +
              (x.comentario ? '<p class="ficha-nota">Comentario: ' + esc(x.comentario) + "</p>" : "") +
              '<form class="rubrica-form">' + RUBRICA.map(function (rr) {
                return '<label>' + esc(rr.nombre) + " (" + rr.peso + ' %)<select name="' + rr.id + '"><option value="">—</option>' + [4, 3, 2, 1].map(function (n) {
                  return '<option value="' + n + '"' + (Number(crit[rr.id]) === n ? " selected" : "") + ">" + n + " · " + NIVELES[n - 1] + "</option>";
                }).join("") + "</select></label>";
              }).join("") +
              '<label class="ancho">Retroalimentación para el participante<textarea name="retro" rows="3" maxlength="2000">' + esc(ev.retro || "") + "</textarea></label>" +
              '<div class="botones"><button class="boton principal" type="submit">Guardar evaluación</button><span class="nota-calculada"></span></div><div class="mensaje" aria-live="polite"></div></form></article>';
          }).join("") + "</section>";
      });
      pintar(html, "Presentaciones · " + c.titulo);
      app.querySelectorAll("[data-ver]").forEach(function (b) {
        b.addEventListener("click", function () {
          var marco = b.closest(".entrega").querySelector(".video-marco");
          if (!marco.innerHTML) marco.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + esc(b.getAttribute("data-ver")) + '" title="Presentación" allowfullscreen loading="lazy"></iframe>';
          marco.hidden = !marco.hidden;
        });
      });
      app.querySelectorAll(".rubrica-form").forEach(function (f) {
        var salida = f.querySelector(".nota-calculada");
        function calc() {
          var crit = {}; RUBRICA.forEach(function (rr) { crit[rr.id] = Number(f[rr.id].value) || 0; });
          var completo = RUBRICA.every(function (rr) { return crit[rr.id]; });
          salida.textContent = completo ? "Nota: " + notaRubrica(crit) + " % · " + (notaRubrica(crit) >= APRUEBA_VIDEO ? "aprobada" : "por mejorar") : "";
          return { crit: crit, completo: completo };
        }
        f.addEventListener("change", calc); calc();
        f.addEventListener("submit", function (evt) {
          evt.preventDefault();
          var x = calc(), msj = f.querySelector(".mensaje");
          if (!x.completo) { msj.className = "mensaje error"; msj.textContent = "Evalúa los cuatro criterios."; return; }
          msj.className = "mensaje"; msj.textContent = "Guardando…";
          Entregas.evaluar(f.closest(".entrega").getAttribute("data-id"), { criterios: x.crit, nota: notaRubrica(x.crit), aprobado: notaRubrica(x.crit) >= APRUEBA_VIDEO, retro: f.retro.value.trim() })
            .then(function () { msj.className = "mensaje ok"; msj.textContent = "Evaluación guardada."; })
            .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
        });
      });
    });
  }

  /* ---------- aula de cada formación: pestañas, participantes, agenda ---------- */

  function pestanasCurso(c, activa) {
    if (acceso(c) !== "libre") return "";
    if (esPropedeutico(c) && Nube.habilitada && !cuentaActual().activo) return "";
    var t = [["contenido", "Contenido", ""], ["muro", "Muro y debates", "/muro"], ["participantes", "Participantes", "/participantes"], ["agenda", "Agenda", "/agenda"]];
    return '<nav class="pestanas-curso" aria-label="Secciones de la formación">' + t.map(function (x) {
      return '<a href="#/curso/' + esc(c.id) + x[2] + '"' + (x[0] === activa ? ' aria-current="page"' : "") + ">" + x[1] + "</a>";
    }).join("") + "</nav>";
  }
  // Encabezado compacto para las secciones del aula (muro, participantes, agenda).
  function cabeceraAula(c, activa) {
    var ar = areaDe(c.id);
    var foto = TARJETAS && TARJETAS[c.id];
    return '<nav class="migas"><a href="#/">Inicio</a>' + (ar ? ' / <a href="#/area/' + esc(ar.id) + '">' + esc(ar.titulo) + "</a>" : "") + ' / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>" +
      '<section class="portada portada-compacta' + (foto ? ' portada-foto" style="--fondo-curso:url(\'' + esc(foto) + '\')' : "") + '"><p class="subtitulo">' + (c.tipo === "curso" ? (c.nivel === "diplomado" ? "Diplomado" : "Curso") : "Módulo") + "</p><h1>" + esc(c.titulo) + "</h1></section>" +
      pestanasCurso(c, activa);
  }

  function consultaN() {
    var m = location.hash.match(/[?&]n=([^&]*)/);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function vistaParticipantes(cursoId) {
    return Promise.all([cargarCurso(cursoId), cargarTarjetas()]).then(function (r) {
      var c = r[0];
      if (acceso(c) !== "libre") { location.hash = "#/curso/" + c.id; return; }
      pintar(cabeceraAula(c, "participantes") + '<p class="cargando">Cargando participantes…</p>', "Participantes · " + c.titulo);
      if (!Nube.habilitada) {
        app.querySelector(".cargando").outerHTML = '<section class="tarjeta"><p>La lista de participantes funciona con las cuentas de la plataforma (Firebase).</p></section>';
        return;
      }
      var yo = Nube.miUid();
      return Nube.personasDeCurso(c.id, esPropedeutico(c)).then(function (ps) {
        ps.sort(function (a, b) { return String(a.nombre).localeCompare(String(b.nombre)); });
        var eq = ps.filter(function (x) { return x.rol === "relator" || x.rol === "admin"; });
        var pa = ps.filter(function (x) { return x.rol !== "relator" && x.rol !== "admin"; });
        function persona(x) {
          return '<li class="persona"><span class="persona-datos"><b>' + esc(x.nombre || "Sin nombre") + (x.uid === yo ? " (tú)" : "") + "</b>" + (x.comunidad ? "<small>" + esc(x.comunidad) + "</small>" : "") + "</span>" +
            (x.uid !== yo ? '<a class="boton boton-chico" href="#/mensajes/' + esc(x.uid) + '?n=' + encodeURIComponent(x.nombre || "") + '">Escribir</a>' : "") + "</li>";
        }
        app.querySelector(".cargando").outerHTML = '<section class="tarjeta"><h2>Quiénes están en esta formación</h2><p class="seccion-bajada">' + pa.length + (pa.length === 1 ? " participante" : " participantes") + ".</p>" +
          (eq.length ? '<h3>Equipo</h3><ul class="personas">' + eq.map(persona).join("") + "</ul>" : "") +
          '<h3>Participantes</h3>' + (pa.length ? '<ul class="personas">' + pa.map(persona).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no hay participantes inscritos.</p>') + "</section>";
      });
    });
  }

  /* agenda */
  var Agenda = {
    leer: function (c) {
      if (Nube.habilitada) return Nube.agendaCurso(c);
      try { return Promise.resolve((JSON.parse(localStorage.getItem("agp:agenda:" + c) || "[]")).filter(function (x) { return !x.borrado; }).map(function (x) { return Object.assign({ curso: c }, x); })); } catch (e) { return Promise.resolve([]); }
    },
    guardar: function (c, d) {
      if (Nube.habilitada) return Nube.guardarFecha(c, d);
      var l = JSON.parse(localStorage.getItem("agp:agenda:" + c) || "[]");
      l.push(Object.assign({ id: "f" + Date.now(), borrado: false }, d)); localStorage.setItem("agp:agenda:" + c, JSON.stringify(l)); return Promise.resolve();
    },
    borrar: function (c, id) {
      if (Nube.habilitada) return Nube.borrarFecha(c, id);
      var l = JSON.parse(localStorage.getItem("agp:agenda:" + c) || "[]");
      l.forEach(function (x) { if (x.id === id) x.borrado = true; }); localStorage.setItem("agp:agenda:" + c, JSON.stringify(l)); return Promise.resolve();
    },
  };
  var TIPOS_FECHA = { entrega: "Entrega", encuentro: "Encuentro", evaluacion: "Evaluación", otro: "Otra fecha" };
  function hoyISO() { var d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function enlaceCalendario(x, titCurso) {
    var d = x.fecha.replace(/-/g, ""), fin;
    if (x.hora) { var h = x.hora.replace(":", "") + "00"; fin = d + "T" + String(Math.min(23, Number(x.hora.slice(0, 2)) + 1)).padStart(2, "0") + x.hora.slice(3) + "00"; d = d + "T" + h; }
    else { var t = new Date(x.fecha + "T12:00:00"); t.setDate(t.getDate() + 1); fin = t.getFullYear() + String(t.getMonth() + 1).padStart(2, "0") + String(t.getDate()).padStart(2, "0"); }
    return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + encodeURIComponent(x.titulo + " · " + titCurso) + "&dates=" + d + "/" + fin + "&details=" + encodeURIComponent((x.detalle || "") + "\n\nMi Ruta");
  }
  function fechaHTML(x, titCurso, cursoId, equipo) {
    var p = x.fecha.split("-"), meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
    return '<li class="fecha fecha-' + esc(x.tipo || "otro") + '"><span class="fecha-dia"><b>' + Number(p[2]) + "</b>" + meses[Number(p[1]) - 1] + "</span>" +
      '<span class="fecha-datos"><span class="fecha-tipo">' + esc(TIPOS_FECHA[x.tipo] || "Fecha") + (x.hora ? " · " + esc(x.hora) + " h" : "") + (cursoId ? "" : "") + "</span><b>" + esc(x.titulo) + "</b>" +
      (x.detalle ? "<small>" + esc(x.detalle) + "</small>" : "") +
      '<span class="fecha-acciones"><a href="' + esc(enlaceCalendario(x, titCurso)) + '" target="_blank" rel="noopener">Agregar a mi calendario</a>' +
      (equipo ? ' · <button class="enlace-boton" type="button" data-borrar-fecha="' + esc(x.id) + '">Quitar</button>' : "") + "</span></span></li>";
  }

  function vistaAgenda(cursoId) {
    return Promise.all([cargarCurso(cursoId), cargarTarjetas(), Agenda.leer(cursoId)]).then(function (r) {
      var c = r[0], lista = (r[2] || []).sort(function (a, b) { return (a.fecha + (a.hora || "")).localeCompare(b.fecha + (b.hora || "")); });
      if (acceso(c) !== "libre") { location.hash = "#/curso/" + c.id; return; }
      var yo = yoForo(), hoy = hoyISO();
      var prox = lista.filter(function (x) { return x.fecha >= hoy; }), pas = lista.filter(function (x) { return x.fecha < hoy; }).reverse();
      var html = cabeceraAula(c, "agenda") + '<section class="tarjeta"><h2>Próximas fechas</h2>' +
        (prox.length ? '<ul class="agenda">' + prox.map(function (x) { return fechaHTML(x, c.titulo, null, yo.equipo); }).join("") + "</ul>" : '<p class="seccion-bajada">No hay fechas próximas. ' + (yo.equipo ? "Agrega la primera abajo." : "Tu relator irá agregando las entregas y encuentros.") + "</p>") + "</section>";
      if (yo.equipo) {
        html += '<section class="tarjeta"><h2>Agregar una fecha</h2><form id="form-fecha" class="form-fecha">' +
          '<label class="ancho">Título<input name="titulo" required maxlength="140" placeholder="Ej.: Entrega de la presentación del módulo 2"></label>' +
          '<label>Fecha<input name="fecha" type="date" required></label><label>Hora (opcional)<input name="hora" type="time"></label>' +
          '<label>Tipo<select name="tipo">' + Object.keys(TIPOS_FECHA).map(function (k) { return '<option value="' + k + '">' + TIPOS_FECHA[k] + "</option>"; }).join("") + "</select></label>" +
          '<label class="ancho">Detalle (opcional)<textarea name="detalle" rows="2" maxlength="1000"></textarea></label>' +
          '<div class="botones ancho"><button class="boton principal" type="submit">Agregar a la agenda</button></div><div class="mensaje ancho" aria-live="polite"></div></form></section>';
      }
      if (pas.length) html += '<section class="tarjeta"><details><summary>Fechas pasadas (' + pas.length + ")</summary>" + '<ul class="agenda pasadas">' + pas.map(function (x) { return fechaHTML(x, c.titulo, null, yo.equipo); }).join("") + "</ul></details></section>";
      pintar(html, "Agenda · " + c.titulo);
      var f = document.getElementById("form-fecha");
      if (f) f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var msj = f.querySelector(".mensaje"); msj.className = "mensaje"; msj.textContent = "Guardando…";
        Agenda.guardar(c.id, { titulo: f.titulo.value.trim(), fecha: f.fecha.value, hora: f.hora.value, tipo: f.tipo.value, detalle: f.detalle.value.trim() }).then(ruta)
          .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
      });
      app.querySelectorAll("[data-borrar-fecha]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (b.getAttribute("data-seguro") !== "1") { b.setAttribute("data-seguro", "1"); b.textContent = "¿Quitar? Confirmar"; return; }
          Agenda.borrar(c.id, b.getAttribute("data-borrar-fecha")).then(ruta);
        });
      });
    });
  }

  // Próximas fechas de mis formaciones (portada).
  function cargarProximasFechas(ids) {
    var caja = document.getElementById("proximas-fechas");
    if (!caja || !ids.length) { if (caja) caja.remove(); return; }
    var hoy = hoyISO();
    Promise.all(ids.map(function (id) { return Promise.all([cargarCurso(id), Agenda.leer(id).catch(function () { return []; })]); })).then(function (rs) {
      var todas = [];
      rs.forEach(function (r) { (r[1] || []).forEach(function (x) { if (x.fecha >= hoy) todas.push(Object.assign({ cursoTitulo: r[0].titulo, cursoId: r[0].id }, x)); }); });
      todas.sort(function (a, b) { return (a.fecha + (a.hora || "")).localeCompare(b.fecha + (b.hora || "")); });
      if (!todas.length) { caja.remove(); return; }
      caja.innerHTML = '<h2 class="seccion-titulo">Próximas fechas</h2><ul class="agenda">' + todas.slice(0, 5).map(function (x) {
        return fechaHTML(x, x.cursoTitulo, x.cursoId, false).replace('<span class="fecha-tipo">', '<span class="fecha-tipo"><a href="#/curso/' + esc(x.cursoId) + '/agenda">' + esc(x.cursoTitulo) + "</a> · ");
      }).join("") + "</ul>";
    }).catch(function () { caja.remove(); });
  }

  /* mensajería */
  var temporizadorChat = null;
  function vistaMensajes(otro, otroNombre) {
    clearTimeout(temporizadorChat);
    if (!Nube.habilitada) { pintar(migas("Mensajes") + '<section class="tarjeta"><h1>Mensajes</h1><p>La mensajería funciona con las cuentas de la plataforma (Firebase).</p></section>', "Mensajes"); return Promise.resolve(); }
    var e = cuentaActual();
    if (!e.activo) { location.hash = "#/perfil"; return Promise.resolve(); }
    var yo = Nube.miUid();
    if (!otro) {
      pintar(migas("Mensajes") + '<section class="tarjeta"><h1>Mensajes</h1><p class="cargando">Cargando…</p></section>', "Mensajes");
      return Nube.misConversaciones().then(function (cs) {
        cs = cs.filter(function (x) { return x.ultimo; }).sort(function (a, b) { return String(b.actualizado).localeCompare(String(a.actualizado)); });
        app.querySelector(".cargando").outerHTML = (cs.length ? '<ul class="conversaciones">' + cs.map(function (x) {
          var o = x.participantes.filter(function (p) { return p !== yo; })[0];
          var nuevo = x.ultimo.uid !== yo && (!x.leido[yo] || x.leido[yo] < x.ultimo.fecha);
          return '<li><a class="' + (nuevo ? "nuevo" : "") + '" href="#/mensajes/' + esc(o) + '?n=' + encodeURIComponent((x.nombres || {})[o] || "") + '"><b>' + esc((x.nombres || {})[o] || "Persona") + "</b><span>" + (x.ultimo.uid === yo ? "Tú: " : "") + esc(x.ultimo.texto) + "</span><time>" + esc(fechaCorta(x.ultimo.fecha)) + "</time></a></li>";
        }).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no tienes conversaciones. Para escribirle a alguien, entra a una formación → <b>Participantes</b> → <b>Escribir</b>.</p>');
      });
    }
    pintar(migas('<a href="#/mensajes">Mensajes</a> / ' + esc(otroNombre || "Conversación")) + '<section class="tarjeta chat"><h1>' + esc(otroNombre || "Conversación") + '</h1><div class="chat-mensajes"><p class="cargando">Cargando…</p></div>' +
      '<form id="form-chat" class="chat-form"><textarea maxlength="2000" required placeholder="Escribe tu mensaje…" rows="2"></textarea><button class="boton principal" type="submit">Enviar</button></form><div class="mensaje" aria-live="polite"></div></section>', "Mensajes");
    var form = document.getElementById("form-chat"), caja = app.querySelector(".chat-mensajes");
    function cargar() {
      return Nube.leerConversacion(otro, otroNombre).then(function (cv) {
        var ms = cv.mensajes.sort(function (a, b) { return String(a.fecha).localeCompare(String(b.fecha)); });
        caja.innerHTML = ms.length ? ms.map(function (m) {
          return '<div class="burbuja' + (m.uid === yo ? " mia" : "") + '"><p>' + esc(m.texto).replace(/\n/g, "<br>") + "</p><time>" + esc(fechaCorta(m.fecha)) + "</time></div>";
        }).join("") : '<p class="seccion-bajada">Escribe el primer mensaje.</p>';
        caja.scrollTop = caja.scrollHeight;
        actualizarBuzon();
        if (location.hash.indexOf("#/mensajes/" + otro) === 0) temporizadorChat = setTimeout(cargar, 10000);
      }).catch(function (er) { caja.innerHTML = '<p class="aviso error">' + esc(er.message) + "</p>"; });
    }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var ta = form.querySelector("textarea"), t = ta.value.trim();
      if (!t) return;
      form.querySelector("button").disabled = true;
      Nube.enviarMensajePrivado(otro, t).then(function () { ta.value = ""; form.querySelector("button").disabled = false; clearTimeout(temporizadorChat); return cargar(); })
        .catch(function (er) { form.querySelector("button").disabled = false; var m = app.querySelector(".chat + .mensaje, .chat .mensaje"); if (m) { m.className = "mensaje error"; m.textContent = er.message; } });
    });
    form.querySelector("textarea").addEventListener("keydown", function (ev) { if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); form.requestSubmit(); } });
    return cargar();
  }

  // Aviso de mensajes nuevos en la cabecera.
  function actualizarBuzon() {
    var b = document.getElementById("enlace-mensajes");
    if (!b || !Nube.habilitada || !cuentaActual().activo) return;
    var yo = Nube.miUid();
    Nube.misConversaciones().then(function (cs) {
      var n = cs.filter(function (x) { return x.ultimo && x.ultimo.uid !== yo && (!x.leido[yo] || x.leido[yo] < x.ultimo.fecha); }).length;
      b.innerHTML = "Mensajes" + (n ? ' <span class="insignia">' + n + "</span>" : "");
    }).catch(function () {});
  }

  /* ---------- evaluaciones ---------- */

  function armarEvaluacion(c, cl, i, ev) {
    var clave = "eval:" + cl.id;
    var previo = almacen.leer(clave, null);
    // Las opciones se barajan en cada intento para que la posición no delate la respuesta.
    var ordenes = ev.preguntas.map(function (p) {
      var o = p.opciones.map(function (_, j) { return j; });
      for (var a = o.length - 1; a > 0; a--) { var b = Math.floor(Math.random() * (a + 1)); var t = o[a]; o[a] = o[b]; o[b] = t; }
      return o;
    });
    var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>";
    html += '<header class="clase-cabecera"><span class="etiqueta-clase">' + esc(etiquetaModulo(cl.modulo)) + (ev.taller ? " · Cierre del módulo" : " · Evaluación") + "</span>" +
      "<h1>" + esc(ev.titulo) + '</h1><p class="meta">' + ev.preguntas.length + " preguntas · se aprueba con " + ev.aprobacion + "%</p></header>";
    if (ev.taller) html += '<section class="taller-cierre"><h2>Taller práctico</h2><div class="texto">' + md(ev.taller) + '</div><p class="ficha-nota">El taller se realiza con tu grupo y tu relator. Después, responde la evaluación.</p></section><h2 class="evaluacion-titulo">Evaluación</h2>';
    html += '<p class="aviso">Responde todas las preguntas y luego revisa tus respuestas. Puedes intentarlo las veces que quieras.' +
      (previo ? " Tu mejor resultado hasta ahora: " + previo.mejor + "%." : "") + "</p>";
    html += '<form id="evaluacion" class="evaluacion">' + ev.preguntas.map(function (p, k) {
      return '<fieldset class="pregunta" data-k="' + k + '"><legend><span class="num">' + (k + 1) + ".</span> " + esc(p.pregunta) + "</legend>" +
        ordenes[k].map(function (j) {
          return '<label class="opcion"><input type="radio" name="p' + k + '" value="' + j + '"> <span>' + esc(p.opciones[j]) + "</span></label>";
        }).join("") + '<p class="retro" hidden></p></fieldset>';
    }).join("") +
      '<div class="resultado" aria-live="polite"></div>' +
      '<div class="botones"><button type="submit" class="boton principal">Revisar respuestas</button>' +
      '<button type="button" class="boton" id="reintentar" hidden>Intentar de nuevo</button></div></form>';
    html += '<section class="tarjeta video-final" id="video-final"></section>';
    html += franjaAgappe(c) + navegacionClases(c, i);
    pintar(html, ev.titulo);
    cargarVideoFinal(c, cl.modulo);

    var form = document.getElementById("evaluacion");
    var resultado = form.querySelector(".resultado");
    var reintentar = document.getElementById("reintentar");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var faltan = 0, buenas = 0;
      ev.preguntas.forEach(function (p, k) {
        if (!form.querySelector('input[name="p' + k + '"]:checked')) faltan++;
      });
      if (faltan) {
        resultado.className = "resultado pendiente";
        resultado.textContent = faltan === 1 ? "Te falta responder 1 pregunta." : "Te faltan " + faltan + " preguntas por responder.";
        return;
      }
      ev.preguntas.forEach(function (p, k) {
        var fs = form.querySelector('.pregunta[data-k="' + k + '"]');
        var elegida = Number(form.querySelector('input[name="p' + k + '"]:checked').value);
        var ok = elegida === p.correcta;
        if (ok) buenas++;
        fs.classList.add(ok ? "correcta" : "incorrecta");
        fs.querySelectorAll("input").forEach(function (inp) { inp.disabled = true; });
        var retro = fs.querySelector(".retro");
        retro.hidden = false;
        retro.innerHTML = "<strong>" + (ok ? "Correcto." : "Respuesta correcta: " + esc(p.opciones[p.correcta]) + ".") + "</strong> " + esc(p.explicacion || "");
      });
      var pct = Math.round(100 * buenas / ev.preguntas.length);
      var aprobado = pct >= ev.aprobacion;
      previo = { mejor: Math.max(pct, previo ? previo.mejor : 0), ultimo: pct };
      almacen.guardar(clave, previo);
      if (aprobado) marcarHecha(c.id, cl.id, true);
      resultado.className = "resultado " + (aprobado ? "aprobado" : "pendiente");
      resultado.textContent = buenas + " de " + ev.preguntas.length + " correctas (" + pct + "%). " +
        (aprobado ? "Evaluación aprobada." : "Necesitas " + ev.aprobacion + "% para aprobar. Repasa las unidades e inténtalo otra vez.");
      form.querySelector('button[type="submit"]').hidden = true;
      reintentar.hidden = false;
    });
    reintentar.addEventListener("click", function () { armarEvaluacion(c, cl, i, ev); });
  }

  /* ---------- cuentas ---------- */

  function migas(extra) {
    return '<nav class="migas"><a href="#/">Inicio</a>' + (extra ? " / " + extra : "") + "</nav>";
  }

  function vistaIngresar() {
    var e = cuentaActual();
    if (!Nube.habilitada) { location.hash = "#/"; return Promise.resolve(); }
    if (e.status !== "invitado" && e.status !== "error") { location.hash = "#/perfil"; return Promise.resolve(); }
    var html = migas() +
      '<section class="tarjeta ingreso"><h1>Ingresar a Mi Ruta</h1>' +
      '<p class="seccion-bajada">Con tu cuenta, tu avance te acompaña en todos tus dispositivos y puedes recibir tus constancias.</p>' +
      '<button class="boton google" id="con-google"><svg viewBox="0 0 48 48" width="20" height="20" aria-hidden="true"><path fill="#ffc107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#ff3d00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4caf50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976d2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>Continuar con Google</button>' +
      '<div class="separador"><span>o con tu correo</span></div>' +
      '<div class="pestanas-ingreso" role="tablist"><button class="pestana" role="tab" aria-selected="true" data-modo="entrar">Ingresar</button><button class="pestana" role="tab" aria-selected="false" data-modo="crear">Crear cuenta</button></div>' +
      '<form id="form-ingreso" class="formulario" novalidate>' +
      '<div class="solo-crear" hidden><label>Nombre y apellido<input name="nombre" autocomplete="name"></label>' +
      '<label>Comunidad o parroquia<input name="comunidad" autocomplete="organization"></label></div>' +
      '<label>Correo<input name="correo" type="email" autocomplete="email" required></label>' +
      '<label>Contraseña<input name="clave" type="password" autocomplete="current-password" minlength="6" required></label>' +
      '<p class="solo-crear nota" hidden>Si tienes menos de 18 años, crea tu cuenta con el conocimiento de tus padres o apoderados.</p>' +
      '<div class="botones"><button class="boton principal" type="submit" id="enviar-ingreso">Ingresar</button>' +
      '<button class="boton enlace" type="button" id="olvide">Olvidé mi contraseña</button></div>' +
      '<div class="mensaje" aria-live="polite"></div></form></section>';
    pintar(html, "Ingresar");

    var modo = "entrar";
    var form = document.getElementById("form-ingreso");
    var mensaje = form.querySelector(".mensaje");
    function decir(texto, tipo) { mensaje.className = "mensaje " + (tipo || ""); mensaje.textContent = texto || ""; }
    function ocupado(si) { form.querySelectorAll("button, input").forEach(function (x) { x.disabled = si; }); document.getElementById("con-google").disabled = si; }

    app.querySelectorAll("[data-modo]").forEach(function (b) {
      b.addEventListener("click", function () {
        modo = b.getAttribute("data-modo");
        app.querySelectorAll("[data-modo]").forEach(function (x) { x.setAttribute("aria-selected", String(x === b)); });
        form.querySelectorAll(".solo-crear").forEach(function (x) { x.hidden = modo !== "crear"; });
        form.clave.setAttribute("autocomplete", modo === "crear" ? "new-password" : "current-password");
        document.getElementById("enviar-ingreso").textContent = modo === "crear" ? "Crear cuenta" : "Ingresar";
        document.getElementById("olvide").hidden = modo === "crear";
        decir("");
      });
    });
    document.getElementById("con-google").addEventListener("click", function () {
      ocupado(true); decir("Abriendo Google…");
      Nube.ingresarGoogle().catch(function (e) { ocupado(false); decir(e.message, "error"); });
    });
    document.getElementById("olvide").addEventListener("click", function () {
      if (!form.correo.value.trim()) { decir("Escribe tu correo y vuelve a tocar «Olvidé mi contraseña».", "error"); form.correo.focus(); return; }
      ocupado(true);
      Nube.recuperarClave(form.correo.value).then(function () {
        ocupado(false); decir("Te enviamos un correo para crear una nueva contraseña. Revisa también la carpeta de spam.", "ok");
      }).catch(function (e) { ocupado(false); decir(e.message, "error"); });
    });
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var datos = { nombre: form.nombre.value.trim(), comunidad: form.comunidad.value.trim(), correo: form.correo.value.trim(), clave: form.clave.value };
      if (!datos.correo || !datos.clave) { decir("Completa tu correo y tu contraseña.", "error"); return; }
      if (modo === "crear" && (!datos.nombre || !datos.comunidad)) { decir("Completa tu nombre y tu comunidad.", "error"); return; }
      if (modo === "crear" && datos.clave.length < 6) { decir("La contraseña debe tener al menos 6 caracteres.", "error"); return; }
      ocupado(true); decir(modo === "crear" ? "Creando tu cuenta…" : "Ingresando…");
      (modo === "crear" ? Nube.registrar(datos) : Nube.ingresarCorreo(datos.correo, datos.clave))
        .catch(function (e) { ocupado(false); decir(e.message, "error"); });
    });
    return Promise.resolve();
  }

  var ESTADOS = { pendiente: "En revisión", activo: "Activa", pausado: "En pausa" };
  var ROLES = { participante: "Participante", relator: "Relator", admin: "Administrador" };
  // Cada perfil contiene a los anteriores: administrador incluye relator, y relator incluye participante.
  var ROLES_INCLUYE = {
    relator: "el de participante: cursas las formaciones, guardas tu avance y recibes constancias.",
    admin: "los de relator y participante: gestionas cuentas y constancias, usas la vista relator y también cursas las formaciones con tu propio avance y constancias.",
  };

  function tituloDe(id) { return cursos[id] && cursos[id].titulo ? cursos[id].titulo : id; }

  function vistaPerfil() {
    if (!sitio.cursos.every(function (id) { return cursos[id]; })) return Promise.all(sitio.cursos.map(cargarCurso)).then(vistaPerfil);
    var e = cuentaActual();
    if (!Nube.habilitada) { location.hash = "#/"; return Promise.resolve(); }
    if (e.status === "invitado") { location.hash = "#/ingresar"; return Promise.resolve(); }
    if (!e.cuenta) { pintar(migas() + '<section class="tarjeta"><h1>Mi cuenta</h1><p class="aviso error">' + esc(e.error || "No se pudo cargar tu cuenta.") + '</p><div class="botones"><button class="boton" id="salir">Salir</button></div></section>', "Mi cuenta"); enlazarSalir(); return Promise.resolve(); }
    var c = e.cuenta;
    var html = migas("Mi cuenta") + '<section class="tarjeta"><h1>Mi cuenta</h1>' +
      '<p class="estado-cuenta estado-' + esc(c.estado) + '">' + esc(ROLES[c.rol] || c.rol) + " · " + esc(ESTADOS[c.estado] || c.estado) + "</p>" +
      (e.activo && ROLES_INCLUYE[c.rol] ? '<p class="ficha-nota">Tu perfil incluye ' + ROLES_INCLUYE[c.rol] + "</p>" : "") +
      (c.estado === "pendiente" ? '<p class="aviso">Tu cuenta está en revisión. Un relator o administrador la aprobará y te habilitará los cursos que solicites.</p>' : "") +
      (c.estado === "pausado" ? '<p class="aviso">Tu cuenta está en pausa. Conversa con tu relator o con la coordinación de Mi Ruta.</p>' : "") +
      ((c.solicitudes || []).length ? '<p class="ficha-nota"><b>Formaciones solicitadas:</b> ' + c.solicitudes.map(function (id) { return esc(tituloDe(id)); }).join(", ") + "</p>" : "") +
      ((c.cursos || []).length ? '<p class="ficha-nota"><b>Formaciones habilitadas:</b> ' + c.cursos.map(function (id) { return esc(tituloDe(id)); }).join(", ") + "</p>" : "") +
      '<form id="form-perfil" class="formulario"><label>Nombre y apellido<input name="nombre" value="' + esc(c.nombre) + '" required></label>' +
      '<label>Comunidad o parroquia<input name="comunidad" value="' + esc(c.comunidad) + '"></label>' +
      '<label>Correo<input value="' + esc(c.correo) + '" disabled></label>' +
      '<div class="botones"><button class="boton principal" type="submit">Guardar cambios</button></div><div class="mensaje" aria-live="polite"></div></form>' +
      '<div class="botones">' +
      (e.activo ? '<a class="boton" href="#/mis-constancias">Mis constancias</a>' : "") +
      (e.esRelator ? '<a class="boton" href="#/gestion">Gestión</a>' : "") +
      '<a class="boton" href="#/sugerencias">Sugerencias y problemas</a>' +
      '<button class="boton" id="salir">Salir</button></div>' +
      (e.esRelator ? '<label class="interruptor claro"><input type="checkbox" id="relator-perfil"' + (modoRelator() ? " checked" : "") + '> <span>Vista relator: mostrar las guías y todos los módulos</span></label>' : "") +
      "</section>";
    pintar(html, "Mi cuenta");
    var form = document.getElementById("form-perfil");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msj = form.querySelector(".mensaje");
      Nube.actualizarPerfil({ nombre: form.nombre.value.trim(), comunidad: form.comunidad.value.trim() })
        .then(function () { msj.className = "mensaje ok"; msj.textContent = "Cambios guardados."; })
        .catch(function (er) { msj.className = "mensaje error"; msj.textContent = er.message; });
    });
    var rel = document.getElementById("relator-perfil");
    if (rel) rel.addEventListener("change", function () { almacen.guardar("modoRelator", rel.checked); actualizarCabecera(); });
    enlazarSalir();
    return Promise.resolve();
  }

  function enlazarSalir() {
    var b = document.getElementById("salir");
    if (b) b.addEventListener("click", function () { Nube.salir().then(function () { location.hash = "#/"; }); });
  }

  /* ---------- constancias ---------- */

  function horasDe(texto) {
    var m = String(texto || "").match(/(\d+(?:,\d+)?)\s*h/);
    return m ? m[1] + " horas" : "";
  }

  // Arma los datos de una constancia: de un módulo, de un módulo que se toma por separado,
  // o el certificado de un curso completo (h es el avance de la persona).
  function datosConstancia(c, alcance, persona, h) {
    h = h || [];
    var d = { uid: persona.uid, nombre: persona.nombre, comunidad: persona.comunidad || "", cursoId: c.id, alcance: alcance, fecha: new Date().toISOString().slice(0, 10) };
    var sesiones = function (m) { return m.clases.filter(function (x) { return !/cierre$/.test(x.id); }).map(function (x) { return x.titulo; }); };
    var horas = function (m) { return horasDe(m.duracion) || m.duracion; };
    if (alcance === "curso" && c.tipo === "curso") {
      var obl = c.modulos.filter(function (m) { return m.tipo !== "optativo"; });
      var opt = c.modulos.filter(function (m) { return m.tipo === "optativo" && moduloCompleto(m, h); }).slice(0, c.elige || 0);
      d.tipo = "certificado";
      d.eyebrow = "CURSO · " + c.titulo.toUpperCase();
      d.titulo = c.titulo;
      d.detalle = "por haber aprobado el curso " + c.titulo + ": " + obl.length + " módulos" + (c.elige ? " obligatorios y " + c.elige + (c.elige === 1 ? " optativo" : " optativos") : "") + ", con un total de " + c.horas + " horas de formación.";
      d.contenidos = obl.concat(opt).map(function (m) { return m.titulo; });
      return d;
    }
    d.tipo = "constancia";
    if (alcance === "curso") {
      var unico = c.modulos[0];
      d.eyebrow = "MÓDULO" + (c.categoria ? " · " + String(c.categoria).toUpperCase() : "");
      d.titulo = c.titulo;
      d.detalle = "6 sesiones aprobadas, con taller y evaluación de cierre · " + horas(unico) + " de formación";
      d.contenidos = sesiones(unico);
      return d;
    }
    var m = c.modulos.filter(function (x) { return x.id === alcance; })[0];
    d.eyebrow = c.titulo.toUpperCase() + " · " + etiquetaModulo(m).toUpperCase();
    d.titulo = m.titulo;
    d.detalle = "6 sesiones aprobadas, con taller y evaluación de cierre · " + horas(m) + " de formación";
    d.contenidos = sesiones(m);
    return d;
  }

  function fechaLarga(iso) {
    var meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
    var t = String(iso || "");
    if (t.indexOf("T") > 0) { var d = new Date(t); if (!isNaN(d)) t = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
    var p = t.split("-");
    return p.length === 3 ? Number(p[2]) + " de " + meses[Number(p[1]) - 1] + " de " + p[0] : "";
  }

  var SELLO = '<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="11.5" fill="#1351a4"/><path d="M9 37 V14 L19 28 L29 14 V31" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="37" cy="34" r="4.2" fill="#ef591c"/></svg>';

  function htmlConstancia(d) {
    var cert = d.tipo === "certificado";
    return '<article class="documento' + (cert ? " certificado" : "") + '"><div class="documento-marco">' +
      '<header class="documento-cabecera"><div class="documento-logo">' + SELLO + '<div><strong>Mi <em>Ruta</em></strong><span>by <span class="ag-app">ag<b>APP</b>e</span></span></div></div>' +
      '<div class="documento-folio">' + (cert ? "Certificado" : "Constancia") + " N.º<br><b>" + esc(d.folio) + "</b></div></header>" +
      '<div class="documento-cuerpo">' +
      (cert ? '<p class="documento-grande">Certificado</p>' : "") +
      '<p class="documento-ceja">' + (cert ? "" : "CONSTANCIA · ") + esc(d.eyebrow) + "</p>" +
      '<p class="documento-otorga">Se otorga a</p><p class="documento-nombre">' + esc(d.nombre) + "</p>" +
      (cert ? '<p class="documento-detalle">' + esc(d.detalle) + "</p>" :
        '<p class="documento-otorga">por haber aprobado la formación</p><p class="documento-curso">' + esc(d.titulo) + '</p><p class="documento-detalle">' + esc(d.detalle) + "</p>") +
      '<p class="documento-contenidos-titulo' + (d.contenidos.length > 4 ? " dos" : "") + '">' + (cert ? "MÓDULOS" : "CONTENIDOS") + '</p><ol class="documento-contenidos' + (d.contenidos.length > 4 ? " dos" : "") + '">' +
      d.contenidos.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ol></div>" +
      '<footer class="documento-pie"><div class="documento-firma"><span>' + esc(d.firmante || "") + "</span>Relator o asesor</div>" +
      '<div class="documento-lugar">' + esc(d.comunidad || "") + "<br>" + esc(fechaLarga(d.fecha)) + "</div>" +
      '<div class="documento-firma"><span></span>' + (cert ? "Párroco" : "Coordinación de Mi Ruta") + "</div></footer>" +
      '<p class="documento-verificar">Verifica este documento en pj-agape.github.io/Mi_ruta con el código ' + esc(d.folio) + "</p>" +
      "</div></article>";
  }

  // En pantalla, la constancia (tamaño carta) se achica para caber; al imprimir vuelve a su tamaño.
  function ajustarDocumento() {
    var cont = app.querySelector(".documento-contenedor");
    var doc = cont && cont.querySelector(".documento");
    if (!doc) return;
    var escala = Math.min(1, cont.clientWidth / 1056);
    doc.style.zoom = escala;
  }
  window.addEventListener("resize", ajustarDocumento);

  function vistaConstancia(folio) {
    pintar(migas("Constancia") + '<p class="cargando">Buscando la constancia…</p>', "Constancia");
    if (!Nube.habilitada) { pintar(migas() + '<section class="tarjeta"><h1>Verificación no disponible</h1><p>Esta plataforma todavía no tiene activadas las cuentas.</p></section>', "Constancia"); return Promise.resolve(); }
    return Nube.leerConstancia(folio).then(function (d) {
      if (!d) {
        pintar(migas("Verificar") + '<section class="tarjeta"><h1>No encontramos esa constancia</h1><p>Revisa que el código esté bien escrito: <b>' + esc(folio) + "</b>.</p></section>", "Constancia");
        return;
      }
      pintar(migas("Constancia") + '<p class="verificada">Documento válido, emitido por Mi Ruta.</p><div class="documento-contenedor">' + htmlConstancia(d) +
        '</div><div class="botones no-imprimir"><button class="boton principal" id="imprimir">Imprimir o guardar en PDF</button></div>', d.titulo);
      document.getElementById("imprimir").addEventListener("click", function () { window.print(); });
      ajustarDocumento();
    });
  }

  function vistaMisConstancias() {
    var e = cuentaActual();
    if (!e.activo) { location.hash = e.status === "invitado" ? "#/ingresar" : "#/perfil"; return Promise.resolve(); }
    return Nube.constanciasDe(e.cuenta.uid).then(function (lista) {
      var html = migas('<a href="#/perfil">Mi cuenta</a> / Mis constancias') + '<section class="tarjeta"><h1>Mis constancias</h1>' +
        (lista.length ? '<ul class="lista-constancias">' + lista.sort(function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); }).map(function (d) {
          return '<li><a href="#/constancia/' + esc(d.folio) + '"><b>' + esc(d.titulo) + '</b><span>' + esc(d.eyebrow) + " · " + esc(fechaLarga(d.fecha)) + "</span></a></li>";
        }).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no tienes constancias. Cuando apruebes una formación, tu relator la emitirá y aparecerá aquí.</p>') +
        "</section>";
      pintar(html, "Mis constancias");
    });
  }

  /* ---------- gestión ---------- */

  function subnavGestion(activa) {
    var e = cuentaActual();
    var items = [["acompanar", "Acompañar"], ["cuentas", "Cuentas y solicitudes"]].concat(e.esAdmin ? [["sugerencias", "Sugerencias y problemas"]] : []);
    return '<nav class="pestanas-curso" aria-label="Gestión">' + items.map(function (x) {
      return '<a href="#/gestion/' + x[0] + '"' + (x[0] === activa ? ' class="activa" aria-current="page"' : "") + ">" + x[1] + "</a>";
    }).join("") + "</nav>";
  }

  function vistaGestion(sub) {
    var e = cuentaActual();
    if (!e.esRelator) { location.hash = "#/"; return Promise.resolve(); }
    if (sub === "cuentas") return vistaCuentas();
    if (sub === "sugerencias" && e.esAdmin) return vistaSoporteAdmin();
    return vistaAcompanar();
  }

  function vistaCuentas() {
    var e = cuentaActual();
    pintar(migas("Gestión") + subnavGestion("cuentas") + '<p class="cargando">Cargando participantes…</p>', "Gestión");
    return Promise.all([Nube.listarUsuarios(), Promise.all(sitio.cursos.map(cargarCurso))]).then(function (r) {
      var usuarios = r[0], lista = r[1];
      var porId = {}; lista.forEach(function (c) { porId[c.id] = c; });
      var pendientes = usuarios.filter(function (u) { return u.estado === "pendiente" || (u.estado === "activo" && (u.solicitudes || []).length); });
      var filtro = almacen.leer("gestion:filtro", "");

      function nombreCurso(id) { return porId[id] ? porId[id].titulo : id; }

      function fichaPendiente(u) {
        var sol = (u.solicitudes || []).filter(function (id) { return porId[id]; });
        var marcar = sol.length ? sol : [];
        return '<li class="ficha" data-uid="' + esc(u.uid) + '"><div class="ficha-cabeza"><b>' + esc(u.nombre) + '</b><span>' + esc(u.correo) + (u.comunidad ? " · " + esc(u.comunidad) : "") + "</span></div>" +
          (u.estado === "pendiente" ? '<p class="ficha-nota">Cuenta nueva, en revisión.</p>' : "") +
          (sol.length ? '<p class="ficha-nota"><b>Solicita:</b> ' + sol.map(function (id) { return esc(nombreCurso(id)); }).join(", ") + "</p>"
            : '<p class="ficha-nota">No ha solicitado ninguna formación. Elige abajo cuáles habilitar.</p>') +
          '<details class="ficha-elegir"' + (sol.length ? "" : " open") + '><summary>Formaciones que se habilitarán (' + marcar.length + ')</summary>' +
          '<fieldset class="ficha-cursos">' + lista.map(function (c) {
            return '<label><input type="checkbox" value="' + esc(c.id) + '"' + (marcar.indexOf(c.id) >= 0 || (u.cursos || []).indexOf(c.id) >= 0 ? " checked" : "") + "> " + esc(c.titulo) + "</label>";
          }).join("") + "</fieldset></details>" +
          '<div class="botones"><button class="boton principal" data-accion="aprobar">' + (u.estado === "pendiente" ? "Aprobar" : "Inscribir") + " y habilitar</button>" +
          (u.estado === "pendiente" ? '<button class="boton" data-accion="pausar">Rechazar</button>' : '<button class="boton" data-accion="descartar">Descartar solicitud</button>') + '</div><div class="mensaje" aria-live="polite"></div></li>';
      }

      function fichaParticipante(u) {
        var cursosU = u.cursos || [];
        return '<li class="ficha" data-uid="' + esc(u.uid) + '"><details><summary><div class="ficha-cabeza"><b>' + esc(u.nombre) + '</b><span>' + esc(ROLES[u.rol] || u.rol) + " · " + esc(ESTADOS[u.estado] || u.estado) +
          (u.comunidad ? " · " + esc(u.comunidad) : "") + " · " + cursosU.length + (cursosU.length === 1 ? " curso" : " cursos") + "</span></div></summary>" +
          '<div class="ficha-cuerpo"><p class="ficha-nota">' + esc(u.correo) + "</p>" +
          '<fieldset class="ficha-cursos"><legend>Cursos habilitados</legend>' + lista.map(function (c) {
            return '<label><input type="checkbox" value="' + esc(c.id) + '"' + (cursosU.indexOf(c.id) >= 0 ? " checked" : "") + "> " + esc(c.titulo) + "</label>";
          }).join("") + "</fieldset>" +
          '<div class="ficha-avance" data-cargar="1"><button class="boton" data-accion="avance">Ver avance y emitir constancias</button></div>' +
          '<div class="botones"><button class="boton principal" data-accion="guardar-cursos">Guardar cursos</button>' +
          (u.estado === "activo" ? '<button class="boton" data-accion="pausar">Poner en pausa</button>' : '<button class="boton" data-accion="activar">Activar</button>') +
          (e.esAdmin && u.uid !== e.cuenta.uid ? '<label class="ficha-rol">Rol <select data-accion="rol">' + Object.keys(ROLES).map(function (k) { return '<option value="' + k + '"' + (u.rol === k ? " selected" : "") + ">" + ROLES[k] + "</option>"; }).join("") + "</select></label>" : "") +
          '</div><div class="mensaje" aria-live="polite"></div></div></details></li>';
      }

      var participantes = usuarios.filter(function (u) {
        if (!filtro) return true;
        var t = (u.nombre + " " + u.correo + " " + (u.comunidad || "")).toLowerCase();
        return t.indexOf(filtro.toLowerCase()) >= 0;
      }).sort(function (a, b) { return String(a.nombre).localeCompare(String(b.nombre)); });

      var html = migas('<a href="#/gestion">Gestión</a> / Cuentas') + subnavGestion("cuentas") + '<section class="portada"><h1>Cuentas y solicitudes</h1><p>Aprueba cuentas, inscribe en cursos, revisa avances y emite constancias.</p>' +
        '<ul class="etiquetas"><li>' + usuarios.length + " cuentas</li><li>" + pendientes.length + " por revisar</li></ul></section>" +
        '<section class="tarjeta"><h2>Por revisar</h2>' + (pendientes.length ? '<ul class="fichas">' + pendientes.map(fichaPendiente).join("") + "</ul>" : '<p class="seccion-bajada">No hay solicitudes pendientes.</p>') + "</section>" +
        '<section class="tarjeta"><h2>Participantes</h2><label class="buscador">Buscar<input id="filtro" value="' + esc(filtro) + '" placeholder="Nombre, correo o comunidad"></label>' +
        '<ul class="fichas">' + participantes.map(fichaParticipante).join("") + "</ul></section>" +
        '<section class="tarjeta"><h2>Constancias emitidas</h2><div id="constancias-emitidas"><button class="boton" id="ver-constancias">Ver constancias emitidas</button></div></section>';
      pintar(html, "Gestión");

      var buscar = document.getElementById("filtro");
      buscar.addEventListener("change", function () { almacen.guardar("gestion:filtro", buscar.value.trim()); vistaCuentas(); });

      document.getElementById("ver-constancias").addEventListener("click", function () {
        var caja = document.getElementById("constancias-emitidas");
        caja.innerHTML = '<p class="cargando">Cargando…</p>';
        Nube.todasLasConstancias().then(function (cs) {
          caja.innerHTML = cs.length ? '<ul class="lista-constancias">' + cs.sort(function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); }).map(function (d) {
            return '<li><a href="#/constancia/' + esc(d.folio) + '"><b>' + esc(d.nombre) + " · " + esc(d.titulo) + "</b><span>" + esc(d.folio) + " · " + esc(fechaLarga(d.fecha)) + "</span></a></li>";
          }).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no se han emitido constancias.</p>';
        }).catch(function (er) { caja.innerHTML = '<p class="aviso error">' + esc(er.message) + "</p>"; });
      });

      app.querySelectorAll(".ficha-elegir").forEach(function (d) {
        d.addEventListener("change", function () {
          d.querySelector("summary").textContent = "Formaciones que se habilitarán (" + d.querySelectorAll("input:checked").length + ")";
        });
      });

      app.querySelectorAll(".ficha").forEach(function (li) {
        var uid = li.getAttribute("data-uid");
        var u = usuarios.filter(function (x) { return x.uid === uid; })[0];
        var msj = li.querySelector(".mensaje") || li;
        function hecho(promesa) {
          promesa.then(vistaCuentas).catch(function (er) { alertaEn(msj, er.message); });
        }
        li.querySelectorAll("[data-accion]").forEach(function (b) {
          var accion = b.getAttribute("data-accion");
          var evento = b.tagName === "SELECT" ? "change" : "click";
          b.addEventListener(evento, function () {
            if (accion === "aprobar") {
              var elegidos = li.querySelector(".ficha-elegir")
                ? Array.from(li.querySelectorAll(".ficha-elegir input:checked")).map(function (x) { return x.value; })
                : (u.solicitudes || []);
              var cursosNuevos = Array.from(new Set((u.cursos || []).concat(elegidos)));
              hecho(Nube.actualizarUsuario(uid, Object.assign({ estado: "activo", cursos: cursosNuevos, solicitudes: [] }, fechasInscripcion(u, cursosNuevos))));
            } else if (accion === "descartar") {
              hecho(Nube.actualizarUsuario(uid, { solicitudes: [] }));
            } else if (accion === "pausar") {
              hecho(Nube.actualizarUsuario(uid, { estado: "pausado" }));
            } else if (accion === "activar") {
              hecho(Nube.actualizarUsuario(uid, { estado: "activo" }));
            } else if (accion === "guardar-cursos") {
              var marcados = Array.from(li.querySelectorAll(".ficha-cursos input:checked")).map(function (x) { return x.value; });
              hecho(Nube.actualizarUsuario(uid, Object.assign({ cursos: marcados, solicitudes: (u.solicitudes || []).filter(function (s) { return marcados.indexOf(s) < 0; }) }, fechasInscripcion(u, marcados))));
            } else if (accion === "rol") {
              hecho(Nube.actualizarUsuario(uid, { rol: b.value }));
            } else if (accion === "avance") {
              mostrarAvance(li.querySelector(".ficha-avance"), u, lista);
            }
          });
        });
      });
    });
  }

  /* ---------- panel de acompañamiento (relatores y administración) ---------- */

  var DIAS_INACTIVO = 14;
  function diasDesde(iso) { return iso ? Math.floor((Date.now() - new Date(iso).getTime()) / 86400000) : null; }
  function haceTexto(iso) {
    var d = diasDesde(iso);
    if (d === null) return "sin registro";
    return d <= 0 ? "hoy" : d === 1 ? "ayer" : "hace " + d + " días";
  }
  function nombreHilo(c, hilo) {
    if (hilo === "bienvenida") return "Presentaciones";
    if (hilo === "programa") return "Dudas del programa";
    var cl = (c.clases || []).filter(function (x) { return x.id === hilo; })[0];
    return cl ? "Debate: " + cl.titulo : "Debate";
  }
  function enlaceHilo(c, hilo) {
    return "#/curso/" + encodeURIComponent(c.id) + "/muro/" + (hilo === "bienvenida" || hilo === "programa" ? hilo : "s/" + encodeURIComponent(hilo));
  }

  function vistaAcompanar() {
    var e = cuentaActual();
    var cab = migas("Gestión") + subnavGestion("acompanar");
    pintar(cab + '<p class="cargando">Revisando mensajes, debates y avances…</p>', "Gestión");
    var yo = Nube.miUid();
    return Promise.all([
      Nube.listarUsuarios(), Promise.all(sitio.cursos.map(cargarCurso)),
      Nube.avances().catch(function () { return []; }),
      Nube.misConversaciones().catch(function () { return []; }),
      e.esAdmin ? Nube.todosSoportes().catch(function () { return []; }) : Promise.resolve([]),
    ]).then(function (r) {
      var usuarios = r[0], cursos = r[1], avs = r[2], convs = r[3], sops = r[4];
      var misCursos = e.esAdmin ? cursos : cursos.filter(function (c) { return (e.cuenta.cursos || []).indexOf(c.id) >= 0 && !esPropedeutico(c); });
      return Promise.all([
        Promise.all(misCursos.map(function (c) { return Nube.mensajesCurso(c.id).catch(function () { return []; }); })),
        Promise.all(misCursos.map(function (c) { return Nube.entregasCurso(c.id).catch(function () { return []; }); })),
      ]).then(function (r2) {
        var foros = r2[0], entregas = r2[1];
        var limite = Date.now() - 60 * 86400000;

        // Debates y dudas cuyo último mensaje es de un participante: esperan una respuesta del equipo.
        var esperan = [];
        misCursos.forEach(function (c, k) {
          var porHilo = {};
          foros[k].filter(function (m) { return !m.borrado; }).forEach(function (m) { (porHilo[m.hilo] = porHilo[m.hilo] || []).push(m); });
          Object.keys(porHilo).forEach(function (h) {
            var xs = porHilo[h].sort(function (a, b) { return String(a.fecha).localeCompare(String(b.fecha)); });
            var ult = xs[xs.length - 1];
            if (ult.rol === "relator" || ult.rol === "admin" || new Date(ult.fecha).getTime() < limite) return;
            var sinRespuesta = 0;
            for (var i = xs.length - 1; i >= 0 && xs[i].rol !== "relator" && xs[i].rol !== "admin"; i--) sinRespuesta++;
            esperan.push({ c: c, hilo: h, ult: ult, n: sinRespuesta });
          });
        });
        esperan.sort(function (a, b) { return String(a.ult.fecha).localeCompare(String(b.ult.fecha)); });

        var porEvaluar = [];
        misCursos.forEach(function (c, k) { entregas[k].filter(function (x) { return !x.evaluacion; }).forEach(function (x) { porEvaluar.push({ c: c, x: x }); }); });

        var noLeidos = convs.filter(function (x) { return x.ultimo && x.ultimo.uid !== yo && (!x.leido[yo] || x.leido[yo] < x.ultimo.fecha); });

        // Participantes a acompañar: inscritos que no han empezado o que dejaron de avanzar.
        var avPor = {}; avs.forEach(function (a) { avPor[a.uid] = a; });
        var sinEmpezar = [], detenidos = [], porVencer = [], ajustes = {}, anuladas = 0, desactivadas = 0;
        var ahora = Date.now(), reglaIso = new Date(REGLA_DESDE).toISOString();
        usuarios.filter(function (u) { return u.estado === "activo" && u.rol === "participante"; }).forEach(function (u) {
          var a = avPor[u.uid] || { datos: {}, actualizado: "" };
          var h = a.datos["hechas:todo"] || [];
          misCursos.forEach(function (c) {
            if ((u.cursos || []).indexOf(c.id) < 0 || esPropedeutico(c)) return;
            var hc = h.concat(a.datos["hechas:" + c.id] || []);
            var pr = progresoCon(c, hc);
            if (pr.total && pr.hechas >= pr.total) return;
            var ins = maxIso((u.inscripciones || {})[c.id], reglaIso);
            if (!pr.hechas) {
              var limite = new Date(maxIso(ins, a.datos["plazo:" + c.id + ":reinicio"])).getTime() + SEMANA;
              if (limite < ahora) { (ajustes[u.uid] = ajustes[u.uid] || { u: u, quitar: [], vencer: [] }).quitar.push(c.id); anuladas++; }
              else sinEmpezar.push({ u: u, c: c, a: a, limite: new Date(limite).toISOString() });
              return;
            }
            // Vencimientos: formación de un módulo, desde la inscripción; cursos, cada módulo desde su primera sesión.
            var vences = [];
            if (c.modulos.length <= 1) vences.push({ m: null, vence: masMeses(ins, 2) });
            else c.modulos.forEach(function (m) {
              if (moduloCompleto(m, hc)) return;
              var ini = a.datos["plazo:" + c.id + ":" + m.id] || (m.clases.some(function (cl) { return hc.indexOf(cl.id) >= 0; }) ? ins : null);
              if (ini) vences.push({ m: m, vence: masMeses(ini, 2) });
            });
            vences.forEach(function (v) {
              var t = new Date(v.vence).getTime();
              if (t < ahora && !v.m) { (ajustes[u.uid] = ajustes[u.uid] || { u: u, quitar: [], vencer: [] }).vencer.push(c.id); desactivadas++; }
              else if (t - ahora <= SEMANA) porVencer.push({ u: u, c: c, a: a, m: v.m, vence: v.vence });
            });
            if (!ajustes[u.uid] || ajustes[u.uid].vencer.indexOf(c.id) < 0) {
              if ((diasDesde(a.actualizado) || 0) > DIAS_INACTIVO) detenidos.push({ u: u, c: c, a: a, hechas: pr.hechas, total: pr.total });
            }
          });
        });
        // Se aplican las reglas: inscripciones sin empezar en 1 semana se anulan; formaciones vencidas se desactivan
        // (el avance lo borra la cuenta de la persona al ingresar, porque solo ella puede escribirlo).
        Object.keys(ajustes).forEach(function (uid) {
          var x = ajustes[uid], quitar = x.quitar.concat(x.vencer);
          var ins = Object.assign({}, x.u.inscripciones || {}); quitar.forEach(function (c) { delete ins[c]; });
          var ven = Object.assign({}, x.u.vencidos || {}); x.vencer.forEach(function (c) { ven[c] = new Date().toISOString(); });
          Nube.actualizarUsuario(uid, { cursos: (x.u.cursos || []).filter(function (c) { return quitar.indexOf(c) < 0; }), inscripciones: ins, vencidos: ven })
            .catch(function (er) { console.warn("Plazos de " + uid + ":", er); });
        });
        porVencer.sort(function (x, y) { return String(x.vence).localeCompare(String(y.vence)); });
        sinEmpezar.sort(function (x, y) { return String(x.limite).localeCompare(String(y.limite)); });
        detenidos.sort(function (x, y) { return String(x.a.actualizado).localeCompare(String(y.a.actualizado)); });
        var pendientes = usuarios.filter(function (u) { return u.estado === "pendiente" || (u.estado === "activo" && (u.solicitudes || []).length); });
        var sopNuevos = sops.filter(function (x) { return x.estado === "nuevo"; });

        function escribir(u) {
          return '<a class="boton mini" href="#/mensajes/' + encodeURIComponent(u.uid) + "?n=" + encodeURIComponent(u.nombre || "") + '">Escribir</a>';
        }
        function filaPersona(x, extra) {
          return '<li class="acomp-fila"><div><b>' + esc(x.u.nombre || x.u.correo) + '</b><span class="acomp-meta">' + esc(x.c.titulo) + (extra ? " · " + extra : "") + "</span></div>" + escribir(x.u) + "</li>";
        }
        function bloque(id, titulo, n, cuerpo, vacio) {
          return '<section class="tarjeta acomp" id="' + id + '"><h2>' + titulo + ' <span class="insignia' + (n ? "" : " cero") + '">' + n + "</span></h2>" + (n ? cuerpo : '<p class="seccion-bajada">' + vacio + "</p>") + "</section>";
        }

        var html = cab + '<section class="portada"><h1>Acompañar</h1><p>Las formaciones se cursan de forma autónoma. Tu tarea como ' + (e.esAdmin ? "administración o relator" : "relator") +
          " es responder, animar el diálogo y orientar a cada participante. Aquí está lo que te espera hoy" + (e.esAdmin ? "" : " en tus formaciones") + ".</p></section>" +
          '<div class="acomp-cifras">' +
            '<a href="#/mensajes" class="acomp-cifra' + (noLeidos.length ? " alerta" : "") + '"><b>' + noLeidos.length + "</b><span>mensajes sin leer</span></a>" +
            '<a href="#/gestion" data-ir="acomp-foro" class="acomp-cifra' + (esperan.length ? " alerta" : "") + '"><b>' + esperan.length + "</b><span>debates o dudas esperan respuesta</span></a>" +
            '<a href="#/gestion" data-ir="acomp-entregas" class="acomp-cifra"><b>' + porEvaluar.length + "</b><span>videos por evaluar</span></a>" +
            '<a href="#/gestion" data-ir="acomp-vencer" class="acomp-cifra' + (porVencer.length ? " alerta" : "") + '"><b>' + porVencer.length + "</b><span>plazos por vencer esta semana</span></a>" +
            '<a href="#/gestion" data-ir="acomp-detenidos" class="acomp-cifra"><b>' + detenidos.length + "</b><span>participantes detenidos</span></a>" +
            '<a href="#/gestion/cuentas" class="acomp-cifra' + (pendientes.length ? " alerta" : "") + '"><b>' + pendientes.length + "</b><span>solicitudes por revisar</span></a>" +
            (e.esAdmin ? '<a href="#/gestion/sugerencias" class="acomp-cifra' + (sopNuevos.length ? " alerta" : "") + '"><b>' + sopNuevos.length + "</b><span>sugerencias o problemas nuevos</span></a>" : "") +
          "</div>" +
          '<details class="tarjeta guia-tutor"><summary><b>Cómo acompañar en Mi Ruta</b></summary>' +
            "<p>Las sesiones están pensadas para que cada participante las curse a su ritmo. El relator no dicta clases: <b>acompaña</b>.</p><ul>" +
            "<li><b>Responde los mensajes</b> dentro de 48 horas, aunque sea para decir «lo reviso y te contesto».</li>" +
            "<li><b>Anima el foro:</b> da la bienvenida a cada presentación, responde las dudas del programa y en cada debate devuelve una pregunta que haga pensar más, nombrando a quien escribió.</li>" +
            "<li><b>Orienta:</b> si alguien se detuvo, escríbele con cercanía, pregúntale cómo está y sugiérele el siguiente paso concreto.</li>" +
            "<li><b>Plazos:</b> cada inscripción tiene 1 semana para empezar y 2 meses para completarse (en los cursos, 2 meses por módulo desde que se empieza). Escribe antes de que venzan: la plataforma anula y desactiva automáticamente.</li>" +
            "<li><b>Evalúa a tiempo</b> los videos finales con la rúbrica, con una retroalimentación breve y alentadora.</li>" +
            "<li><b>Avisa a la administración</b> los problemas de la plataforma o del contenido en <a href=\"#/sugerencias\">Sugerencias y problemas</a>.</li></ul></details>" +
          bloque("acomp-foro", "Debates y dudas que esperan respuesta", esperan.length,
            '<ul class="acomp-lista">' + esperan.map(function (x) {
              return '<li class="acomp-fila"><div><b>' + esc(nombreHilo(x.c, x.hilo)) + '</b><span class="acomp-meta">' + esc(x.c.titulo) + " · " + esc(x.ult.nombre || "Participante") + " · " + haceTexto(x.ult.fecha) +
                (x.n > 1 ? " · " + x.n + " mensajes sin respuesta" : "") + '</span><span class="acomp-extracto">' + esc(String(x.ult.texto || "").slice(0, 160)) + (String(x.ult.texto || "").length > 160 ? "…" : "") + "</span></div>" +
                '<a class="boton mini principal" href="' + enlaceHilo(x.c, x.hilo) + '">Responder</a></li>';
            }).join("") + "</ul>", "Nada pendiente en el foro. Puedes abrir un debate y dejar una pregunta para animar la conversación.") +
          bloque("acomp-entregas", "Presentaciones en video por evaluar", porEvaluar.length,
            '<ul class="acomp-lista">' + porEvaluar.map(function (x) {
              return '<li class="acomp-fila"><div><b>' + esc(x.x.nombre || "Participante") + '</b><span class="acomp-meta">' + esc(x.c.titulo) + " · enviado " + haceTexto(x.x.fecha) + '</span></div><a class="boton mini" href="#/curso/' + encodeURIComponent(x.c.id) + '/entregas">Evaluar</a></li>';
            }).join("") + "</ul>", "No hay videos pendientes de evaluación.") +
          (anuladas || desactivadas ? '<p class="aviso">Se aplicaron las reglas de plazos: ' + [anuladas ? anuladas + (anuladas === 1 ? " inscripción anulada" : " inscripciones anuladas") + " por no empezar en 1 semana" : "", desactivadas ? desactivadas + (desactivadas === 1 ? " formación desactivada" : " formaciones desactivadas") + " por cumplirse los 2 meses" : ""].filter(Boolean).join(" y ") + ".</p>" : "") +
          bloque("acomp-vencer", "Plazos que vencen en los próximos 7 días", porVencer.length,
            '<ul class="acomp-lista">' + porVencer.map(function (x) { return filaPersona(x, (x.m ? esc(etiquetaModulo(x.m)) + " · " : "") + "vence el " + esc(fechaLarga(x.vence))); }).join("") + "</ul>",
            "Nadie tiene un plazo por vencer esta semana.") +
          bloque("acomp-detenidos", "Participantes detenidos (más de " + DIAS_INACTIVO + " días sin avanzar)", detenidos.length,
            '<ul class="acomp-lista">' + detenidos.slice(0, 40).map(function (x) { return filaPersona(x, x.hechas + " de " + x.total + " sesiones · última actividad " + haceTexto(x.a.actualizado)); }).join("") + "</ul>",
            "Todos los que empezaron siguen avanzando.") +
          bloque("acomp-sin", "Inscritos que aún no empiezan", sinEmpezar.length,
            '<ul class="acomp-lista">' + sinEmpezar.slice(0, 40).map(function (x) { return filaPersona(x, "sin sesiones completadas · se anula el " + esc(fechaLarga(x.limite))); }).join("") + "</ul>" +
            (sinEmpezar.length > 40 ? '<p class="seccion-bajada">Y ' + (sinEmpezar.length - 40) + " más.</p>" : ""),
            "Todos los inscritos ya empezaron.");
        pintar(html, "Gestión");
        app.querySelectorAll("[data-ir]").forEach(function (x) {
          x.addEventListener("click", function (ev) {
            ev.preventDefault();
            var dest = document.getElementById(x.getAttribute("data-ir"));
            if (dest) dest.scrollIntoView({ behavior: "smooth", block: "start" });
          });
        });
      });
    });
  }

  /* ---------- sugerencias y problemas ---------- */

  var TIPOS_SOPORTE = { mejora: "Sugerencia de mejora", error: "Problema o error de la plataforma", contenido: "Error o mejora en el contenido de una formación", otro: "Otro" };
  var ESTADOS_SOPORTE = { nuevo: "Recibido", revision: "En revisión", resuelto: "Resuelto", descartado: "No se hará por ahora" };

  function vistaSugerencias() {
    var e = cuentaActual();
    var m = location.hash.match(/[?&]desde=([^&]*)/);
    var desde = m ? decodeURIComponent(m[1]) : "";
    var cab = migas("Sugerencias y problemas") + '<section class="portada"><h1>Sugerencias y problemas</h1><p>¿Encontraste un error, algo que no funciona o una idea para mejorar Mi Ruta o sus formaciones? Escríbele a la administración: cada mensaje se revisa y te responderemos aquí.</p></section>';
    if (!Nube.habilitada || !e.cuenta) {
      pintar(cab + '<section class="tarjeta"><p>Para enviar una sugerencia necesitas ingresar con tu cuenta.</p>' + (Nube.habilitada ? '<a class="boton principal" href="#/ingresar">Ingresar</a>' : "") + "</section>", "Sugerencias");
      return Promise.resolve();
    }
    pintar(cab + '<p class="cargando">Cargando…</p>', "Sugerencias");
    return Nube.misSoportes().catch(function () { return []; }).then(function (mios) {
      mios.sort(function (a, b) { return String(b.creado).localeCompare(String(a.creado)); });
      try { localStorage.setItem("miruta:soporte-visto", JSON.stringify(mios.filter(function (x) { return x.respuesta; }).map(function (x) { return x.id + x.respondido; }))); } catch (er) { /* sin almacenamiento */ }
      var html = cab + '<section class="tarjeta"><h2>Escribir a la administración</h2><form id="form-soporte" class="formulario">' +
        '<label>Tipo<select name="tipo">' + Object.keys(TIPOS_SOPORTE).map(function (k) { return '<option value="' + k + '"' + (desde && k === "contenido" ? " selected" : "") + ">" + TIPOS_SOPORTE[k] + "</option>"; }).join("") + "</select></label>" +
        '<label>¿Qué pasó o qué propones?<textarea name="texto" maxlength="2000" required rows="5" placeholder="Cuéntanos con detalle: qué estabas haciendo, qué esperabas que pasara y qué pasó. Si es una idea, explica para qué serviría."></textarea></label>' +
        (desde ? '<p class="seccion-bajada">Se adjuntará la página donde estabas: <code>' + esc(desde) + "</code></p>" : "") +
        '<input type="hidden" name="pagina" value="' + esc(desde) + '">' +
        '<div class="botones"><button class="boton principal" type="submit">Enviar</button></div><p class="mensaje" role="status"></p></form></section>' +
        '<section class="tarjeta"><h2>Lo que has enviado</h2>' + (mios.length ? '<ul class="acomp-lista">' + mios.map(function (x) {
          return '<li class="soporte-item"><div class="soporte-cab"><b>' + esc(TIPOS_SOPORTE[x.tipo] || x.tipo) + '</b><span class="estado-soporte ' + esc(x.estado) + '">' + esc(ESTADOS_SOPORTE[x.estado] || x.estado) + "</span></div>" +
            '<p class="soporte-texto">' + esc(x.texto) + '</p><span class="acomp-meta">' + esc(fechaLarga(x.creado)) + "</span>" +
            (x.respuesta ? '<div class="soporte-respuesta"><b>Respuesta' + (x.respondidoPor ? " de " + esc(x.respondidoPor) : "") + ":</b> " + esc(x.respuesta) + "</div>" : "") + "</li>";
        }).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no has enviado sugerencias.</p>') + "</section>";
      pintar(html, "Sugerencias");
      var f = document.getElementById("form-soporte");
      f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var b = f.querySelector("button"), msj = f.querySelector(".mensaje");
        var texto = f.texto.value.trim();
        if (texto.length < 5) { msj.className = "mensaje error"; msj.textContent = "Escribe un poco más de detalle."; return; }
        b.disabled = true;
        Nube.enviarSoporte({ tipo: f.tipo.value, texto: texto.slice(0, 2000), pagina: f.pagina.value.slice(0, 300) }).then(function () {
          location.hash = "#/sugerencias"; vistaSugerencias();
        }).catch(function (er) { b.disabled = false; msj.className = "mensaje error"; msj.textContent = er.message; });
      });
    });
  }

  function vistaSoporteAdmin() {
    var cab = migas('<a href="#/gestion">Gestión</a> / Sugerencias') + subnavGestion("sugerencias");
    pintar(cab + '<p class="cargando">Cargando…</p>', "Gestión");
    var filtro = almacen.leer("soporte:filtro", "abiertos");
    return Nube.todosSoportes().then(function (xs) {
      var F = { abiertos: function (x) { return x.estado === "nuevo" || x.estado === "revision"; }, resueltos: function (x) { return x.estado === "resuelto"; }, descartados: function (x) { return x.estado === "descartado"; }, todos: function () { return true; } };
      if (!F[filtro]) filtro = "abiertos";
      var lista = xs.filter(F[filtro]).sort(function (a, b) { return String(b.creado).localeCompare(String(a.creado)); });
      var html = cab + '<section class="portada"><h1>Sugerencias y problemas</h1><p>Lo que participantes y relatores reportan sobre la plataforma y las formaciones. Responde aquí: cada persona ve tu respuesta en su página de sugerencias.</p></section>' +
        '<div class="filtros-soporte">' + Object.keys(F).map(function (k) { return '<button class="boton mini' + (k === filtro ? " principal" : "") + '" data-filtro="' + k + '">' + k[0].toUpperCase() + k.slice(1) + " (" + xs.filter(F[k]).length + ")</button>"; }).join("") + "</div>" +
        (lista.length ? lista.map(function (x) {
          return '<section class="tarjeta soporte-admin" data-id="' + esc(x.id) + '"><div class="soporte-cab"><b>' + esc(TIPOS_SOPORTE[x.tipo] || x.tipo) + '</b><span class="estado-soporte ' + esc(x.estado) + '">' + esc(ESTADOS_SOPORTE[x.estado] || x.estado) + "</span></div>" +
            '<p class="acomp-meta">' + esc(x.nombre || "") + " · " + esc(ROLES[x.rol] || x.rol || "") + " · " + esc(x.correo || "") + " · " + esc(fechaLarga(x.creado)) + "</p>" +
            '<p class="soporte-texto">' + esc(x.texto) + "</p>" + (x.pagina ? '<p class="acomp-meta">Página: <a href="' + esc(x.pagina) + '">' + esc(x.pagina) + "</a></p>" : "") +
            '<form class="formulario soporte-form"><label>Estado<select name="estado">' + Object.keys(ESTADOS_SOPORTE).map(function (k) { return '<option value="' + k + '"' + (k === x.estado ? " selected" : "") + ">" + ESTADOS_SOPORTE[k] + "</option>"; }).join("") + "</select></label>" +
            '<label>Respuesta (la verá quien escribió)<textarea name="respuesta" maxlength="2000" rows="3">' + esc(x.respuesta || "") + "</textarea></label>" +
            '<div class="botones"><button class="boton principal" type="submit">Guardar</button></div><p class="mensaje" role="status"></p></form></section>';
        }).join("") : '<section class="tarjeta"><p class="seccion-bajada">No hay mensajes en esta lista.</p></section>');
      pintar(html, "Gestión");
      app.querySelectorAll("[data-filtro]").forEach(function (b) { b.addEventListener("click", function () { almacen.guardar("soporte:filtro", b.getAttribute("data-filtro")); vistaSoporteAdmin(); }); });
      app.querySelectorAll(".soporte-admin").forEach(function (sec) {
        var f = sec.querySelector("form"), id = sec.getAttribute("data-id");
        var orig = xs.filter(function (x) { return x.id === id; })[0];
        f.addEventListener("submit", function (ev) {
          ev.preventDefault();
          var cambios = { estado: f.estado.value };
          var resp = f.respuesta.value.trim();
          if (resp !== (orig.respuesta || "")) cambios.respuesta = resp.slice(0, 2000);
          f.querySelector("button").disabled = true;
          Nube.responderSoporte(id, cambios).then(vistaSoporteAdmin).catch(function (er) { var m = f.querySelector(".mensaje"); m.className = "mensaje error"; m.textContent = er.message; f.querySelector("button").disabled = false; });
        });
      });
    }).catch(function (er) { pintar(cab + '<section class="tarjeta"><p class="aviso error">' + esc(er.message) + "</p></section>", "Gestión"); });
  }

  // Fecha de inscripción de cada curso habilitado (las nuevas, hoy); al reinscribir se olvida un vencimiento anterior.
  function fechasInscripcion(u, cursosNuevos) {
    var ins = {}, ven = Object.assign({}, u.vencidos || {}), hoy = new Date().toISOString();
    cursosNuevos.forEach(function (c) {
      var nuevo = (u.cursos || []).indexOf(c) < 0;
      ins[c] = nuevo ? hoy : ((u.inscripciones || {})[c] || hoy);
      if (nuevo) delete ven[c];
    });
    return { inscripciones: ins, vencidos: ven };
  }

  function mostrarAvance(caja, u, lista) {
    caja.innerHTML = '<p class="cargando">Cargando avance…</p>';
    Nube.avanceDe(u.uid).then(function (datos) {
      var cursosU = lista.filter(function (c) { return (u.cursos || []).indexOf(c.id) >= 0; });
      if (!cursosU.length) { caja.innerHTML = '<p class="seccion-bajada">No tiene cursos habilitados.</p>'; return; }
      var opciones = [];
      var filas = cursosU.map(function (c) {
        var h = (datos["hechas:todo"] || []).concat(datos["hechas:" + c.id] || []);
        var pg = progresoCon(c, h);
        var html = '<li><b>' + esc(c.titulo) + "</b><span>" + pg.hechas + " de " + pg.total + " (" + pg.pct + "%)</span></li>";
        html += '<li class="sub" data-debates="' + esc(c.id) + '"><span>Participación en debates</span><span>…</span></li>';
        html += '<li class="sub" data-videos="' + esc(c.id) + '" hidden><span>Presentaciones en video</span><span>…</span></li>';
        if (c.tipo === "curso") {
          c.modulos.forEach(function (m) {
            var hm = m.clases.filter(function (x) { return h.indexOf(x.id) >= 0; }).length;
            html += '<li class="sub"><span>' + esc(etiquetaModulo(m)) + ". " + esc(m.titulo) + "</span><span>" + hm + " de " + m.clases.length + "</span></li>";
            opciones.push({ valor: c.id + "|" + m.id, texto: c.titulo + " · " + m.titulo + (hm === m.clases.length ? " (completo)" : " (" + hm + " de " + m.clases.length + ")"), h: h });
          });
          opciones.push({ valor: c.id + "|curso", texto: "Certificado del curso " + c.titulo + (pg.pct === 100 ? " (completo)" : " (" + pg.pct + "%)"), h: h });
        } else {
          opciones.push({ valor: c.id + "|curso", texto: c.titulo + (pg.pct === 100 ? " (completo)" : " (" + pg.pct + "%)"), h: h });
        }
        return html;
      }).join("");
      caja.innerHTML = '<ul class="avance-lista">' + filas + "</ul>" +
        '<div class="emitir"><label>Emitir constancia de<select>' + opciones.map(function (o) { return '<option value="' + esc(o.valor) + '">' + esc(o.texto) + "</option>"; }).join("") + "</select></label>" +
        '<p class="ficha-nota">Solo se emite cuando el módulo está aprobado: todas sus sesiones y la evaluación de cierre, y además los debates y la presentación en video si la formación los exige. La plataforma lo revisa al emitir.</p>' +
        '<div class="botones"><button class="boton principal" data-paso="1">Emitir constancia</button></div><div class="mensaje" aria-live="polite"></div></div>';
      caja.querySelectorAll("[data-videos]").forEach(function (li) {
        var c = lista.filter(function (x) { return x.id === li.getAttribute("data-videos"); })[0];
        Promise.all([Foro.leer(c.id), Entregas.delCurso(c.id)]).then(function (r) {
          if (!r[0] || !r[0].video) return;
          var es = (r[1] || []).filter(function (x) { return x.uid === u.uid; });
          var ap = es.filter(function (x) { return x.evaluacion && x.evaluacion.nota >= APRUEBA_VIDEO; }).length;
          li.hidden = false;
          li.lastChild.innerHTML = ap + " aprobadas de " + c.modulos.length + " módulos · " + es.length + ' enviadas · <a href="#/curso/' + esc(c.id) + '/entregas">revisar</a>';
        }).catch(function () {});
      });
      caja.querySelectorAll("[data-debates]").forEach(function (li) {
        var c = lista.filter(function (x) { return x.id === li.getAttribute("data-debates"); })[0];
        Promise.all([Foro.leer(c.id), Foro.mensajes(c.id)]).then(function (r) {
          var deb = debatibles(c), msgs = r[1] || [];
          var n = deb.filter(function (x) { return participoEn(msgs, u.uid, x.id); }).length;
          var pres = msgs.some(function (m) { return m.hilo === "bienvenida" && m.uid === u.uid && !m.borrado; });
          li.lastChild.textContent = n + " de " + deb.length + (r[0] && r[0].obligatorio ? " (obligatorio)" : "") + (pres ? " · se presentó" : " · sin presentación");
        }).catch(function () { li.lastChild.textContent = "no disponible"; });
      });
      var boton = caja.querySelector("[data-paso]");
      var select = caja.querySelector("select");
      var msj = caja.querySelector(".mensaje");
      boton.addEventListener("click", function () {
        if (boton.getAttribute("data-paso") === "1") {
          boton.setAttribute("data-paso", "2"); boton.textContent = "Confirmar: emitir a " + u.nombre; return;
        }
        boton.disabled = true;
        var partes = select.value.split("|");
        var c = lista.filter(function (x) { return x.id === partes[0]; })[0];
        var op = opciones.filter(function (o) { return o.valor === select.value; })[0];
        msj.className = "mensaje"; msj.textContent = "Revisando requisitos…";
        requisitosAprobacion(c, partes[1], u, op ? op.h : []).then(function (faltan) {
          if (faltan.length) {
            var err = new Error("");
            err.html = "<b>Todavía no se puede emitir: el módulo debe estar aprobado.</b><ul>" + faltan.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + "</ul>";
            throw err;
          }
          return Nube.emitirConstancia(datosConstancia(c, partes[1], u, op ? op.h : []));
        }).then(function (folio) {
          msj.className = "mensaje ok";
          msj.innerHTML = 'Constancia emitida: <a href="#/constancia/' + esc(folio) + '">' + esc(folio) + "</a>";
          boton.disabled = false; boton.setAttribute("data-paso", "1"); boton.textContent = "Emitir constancia";
        }).catch(function (er) {
          boton.disabled = false; boton.setAttribute("data-paso", "1"); boton.textContent = "Emitir constancia";
          msj.className = "mensaje error";
          if (er.html) msj.innerHTML = er.html; else msj.textContent = er.message;
        });
      });
    }).catch(function (er) { caja.innerHTML = '<p class="aviso error">' + esc(er.message) + "</p>"; });
  }

  // Un módulo está aprobado cuando: completó todas sus sesiones (incluida la evaluación de cierre),
  // participó en sus debates si son obligatorios y su presentación en video está aprobada si se pide.
  function requisitosAprobacion(c, alcance, u, h) {
    return Promise.all([Foro.leer(c.id).catch(function () { return {}; }), Foro.mensajes(c.id).catch(function () { return []; }), Entregas.delCurso(c.id).catch(function () { return []; })]).then(function (r) {
      var f = r[0] || {}, msgs = r[1] || [], ents = (r[2] || []).filter(function (x) { return x.uid === u.uid; });
      function faltasModulo(m) {
        var out = [], nombre = c.tipo === "curso" ? etiquetaModulo(m) + " (" + m.titulo + ")" : m.titulo;
        var pend = m.clases.filter(function (x) { return h.indexOf(x.id) < 0; }).length;
        if (pend) out.push(nombre + ": faltan " + pend + (pend === 1 ? " sesión" : " sesiones") + " (o la evaluación de cierre).");
        if (f.obligatorio) {
          var sinDebate = m.clases.filter(function (x) { return x.tipo !== "evaluacion" && !participoEn(msgs, u.uid, x.id); }).length;
          if (sinDebate) out.push(nombre + ": falta participar en " + sinDebate + (sinDebate === 1 ? " debate." : " debates."));
        }
        if (f.video) {
          var e = ents.filter(function (x) { return x.modulo === m.id; })[0];
          if (!e) out.push(nombre + ": no ha enviado la presentación en video.");
          else if (!e.evaluacion) out.push(nombre + ": la presentación en video está pendiente de evaluar.");
          else if (e.evaluacion.nota < APRUEBA_VIDEO) out.push(nombre + ": la presentación en video no alcanza el " + APRUEBA_VIDEO + " % (" + e.evaluacion.nota + " %).");
        }
        return out;
      }
      if (c.tipo !== "curso") return faltasModulo(c.modulos[0]);
      if (alcance !== "curso") return faltasModulo(c.modulos.filter(function (m) { return m.id === alcance; })[0]);
      var faltan = [];
      var obl = c.modulos.filter(function (m) { return m.tipo === "obligatorio"; });
      var opt = c.modulos.filter(function (m) { return m.tipo === "optativo"; });
      obl.forEach(function (m) { faltan = faltan.concat(faltasModulo(m)); });
      var optOk = opt.filter(function (m) { return !faltasModulo(m).length; }).length;
      if (c.elige && optOk < c.elige) faltan.push("Optativos: aprobó " + optOk + " de los " + c.elige + " que exige el curso.");
      return faltan;
    });
  }

  /* ---------- cabecera ---------- */

  function actualizarCabecera() {
    var enlace = document.getElementById("cuenta-enlace");
    var caja = document.getElementById("caja-relator");
    var pie = document.getElementById("pie-nota");
    if (!Nube.habilitada) { enlace.hidden = true; caja.hidden = false; return; }
    var e = cuentaActual();
    // Relatores y administradores tienen el interruptor «Vista relator» en la cabecera (también en Mi cuenta).
    caja.hidden = !e.esRelator;
    if (e.esRelator) document.getElementById("modo-relator").checked = modoRelator();
    enlace.hidden = false;
    if (e.status === "invitado" || e.status === "error" && !e.cuenta) {
      enlace.textContent = "Ingresar"; enlace.href = "#/ingresar"; enlace.className = "cuenta-boton";
    } else if (e.cuenta) {
      var iniciales = String(e.cuenta.nombre || "?").split(/\s+/).filter(Boolean).slice(0, 2).map(function (x) { return x[0]; }).join("").toUpperCase();
      enlace.textContent = iniciales; enlace.href = "#/perfil"; enlace.className = "cuenta-boton avatar" + (modoRelator() ? " relator" : "");
      enlace.title = e.cuenta.nombre + (modoRelator() ? " · vista relator" : "");
    }
    if (pie) pie.textContent = e.activo ? "Tu avance se guarda en tu cuenta y te acompaña en todos tus dispositivos." : "Con tu cuenta, tu avance te acompaña en todos tus dispositivos.";
    var em = document.getElementById("enlace-mensajes");
    if (e.activo) {
      if (!em) {
        em = document.createElement("a");
        em.id = "enlace-mensajes"; em.className = "cuenta-gestion"; em.href = "#/mensajes"; em.textContent = "Mensajes";
        enlace.parentNode.insertBefore(em, enlace);
      }
      actualizarBuzon();
    } else if (em) em.remove();
    if (e.esRelator) {
      if (!document.getElementById("enlace-gestion")) {
        var g = document.createElement("a");
        g.id = "enlace-gestion"; g.className = "cuenta-gestion"; g.href = "#/gestion"; g.textContent = "Gestión";
        enlace.parentNode.insertBefore(g, enlace);
      }
    } else {
      var vieja = document.getElementById("enlace-gestion");
      if (vieja) vieja.remove();
    }
  }

  /* ---------- enrutador ---------- */

  function ruta() {
    var revision = revisarPlazos();
    if (revision) return revision.then(ruta, ruta);
    var partes = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean).map(decodeURIComponent);
    var tarea;
    actualizarCabecera();
    if (partes[0] === "curso" && partes[1] && partes[2] === "programa") tarea = vistaPrograma(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "sesiones") tarea = vistaSesiones(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "muro") tarea = vistaMuro(partes[1], partes[3], partes[4]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "entregas") tarea = vistaEntregas(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "participantes") tarea = vistaParticipantes(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "agenda") tarea = vistaAgenda(partes[1]);
    else if (partes[0] === "mensajes") tarea = vistaMensajes(partes[1] ? partes[1].split("?")[0] : "", consultaN());
    else if (partes[0] === "area" && partes[1]) tarea = vistaArea(partes[1]);
    else if (partes[0] === "curso" && partes[1]) tarea = vistaCurso(partes[1]);
    else if (partes[0] === "clase" && partes[1] && partes[2]) tarea = vistaClase(partes[1], partes[2]);
    else if (partes[0] === "ingresar") tarea = vistaIngresar();
    else if (partes[0] === "perfil") tarea = vistaPerfil();
    else if (partes[0] === "gestion") tarea = vistaGestion(partes[1]);
    else if (partes[0] && partes[0].split("?")[0] === "sugerencias") tarea = vistaSugerencias();
    else if (partes[0] === "mis-constancias") tarea = vistaMisConstancias();
    else if (partes[0] === "constancia" && partes[1]) tarea = vistaConstancia(partes[1]);
    else tarea = vistaInicio();
    return Promise.resolve(tarea).catch(error);
  }

  var interruptor = document.getElementById("modo-relator");
  interruptor.checked = modoRelator();
  interruptor.addEventListener("change", function () {
    almacen.guardar("modoRelator", interruptor.checked);
    ruta();
  });

  window.addEventListener("hashchange", ruta);
  document.addEventListener("click", function (ev) {
    if (ev.target && ev.target.id === "cerrar-avisos-plazo") {
      try { sessionStorage.removeItem("miruta:avisos-plazo"); } catch (er) { /* sin almacenamiento */ }
      var sec = ev.target.closest(".avisos-plazo"); if (sec) sec.remove();
    }
  });

  // Al ingresar o salir, se vuelve a dibujar la vista. Después de ingresar, se va a la portada.
  Nube.alCambiar(function () {
    if (/^#\/ingresar/.test(location.hash) && cuentaActual().cuenta) location.hash = "#/";
    else ruta();
  });

  Promise.resolve(Nube.listo).then(cargarSitio).then(ruta).catch(error);
})();
