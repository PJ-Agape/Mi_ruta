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
  function acceso(curso) {
    if (!Nube.habilitada) return "libre";
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
      solicitar: ["Inscríbete en este curso", "Al solicitar la inscripción, un relator la revisará y te habilitará el curso.", '<button class="boton principal" data-solicitar="' + esc(curso.id) + '">Solicitar inscripción</button>'],
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

  function duracionClase(cl) {
    return cl.semana ? "Semana " + cl.semana : (cl.tiempo || "");
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

  function vistaInicio() {
    return Promise.all(sitio.cursos.map(cargarCurso)).then(function (lista) {
      var html = '<section class="portada"><h1 class="logo-titulo">' + nombreConEstilo(sitio.nombre) + "</h1>" + FIRMA + "<p>" + esc(sitio.lema) + "</p></section>";
      function tarjeta(c) {
        var p = progreso(c);
        var ceja = c.tipo === "curso" ? "Curso" : (c.categoria ? esc(c.categoria) : (c.institucion ? esc(c.institucion) : ""));
        return '<article class="tarjeta curso-tarjeta">' + (ceja ? '<p class="institucion">' + ceja + "</p>" : "") + '<h2>' + esc(c.titulo) + '</h2><p class="subtitulo">' + esc(c.subtitulo) +
          "</p><p>" + esc(c.descripcion) + "</p><p class=\"meta\">" + [c.duracion, c.modalidad, c.publico].filter(Boolean).map(esc).join(" · ") + "</p>" +
          barraProgreso(p) + '<div class="botones"><a class="boton principal" href="#/curso/' + esc(c.id) + '">Entrar al curso</a></div></article>';
      }
      var e = cuentaActual();
      if (Nube.habilitada && e.status === "invitado") {
        html += '<section class="tarjeta acceso-inicio"><h2>Bienvenido a Mi Ruta</h2><p>Crea tu cuenta para inscribirte en los cursos y guardar tu avance en todos tus dispositivos.</p><div class="botones"><a class="boton principal" href="#/ingresar">Ingresar o crear cuenta</a></div></section>';
      } else if (Nube.habilitada && e.status === "pendiente") {
        html += '<section class="tarjeta acceso-inicio"><h2>Hola, ' + esc(e.cuenta.nombre) + '</h2><p>Tu cuenta está en revisión. Mientras tanto, explora los cursos y solicita la inscripción en los que te interesen.</p><div class="botones"><a class="boton" href="#/perfil">Mi cuenta</a></div></section>';
      } else if (Nube.habilitada && e.activo && !e.esRelator) {
        var mios = lista.filter(function (c) { return (e.cuenta.cursos || []).indexOf(c.id) >= 0; });
        html += '<section class="seccion-inicio"><h2 class="seccion-titulo">Mis cursos</h2>' +
          (mios.length ? mios.map(function (c) {
            var p = progreso(c);
            return '<a class="mi-curso" href="#/curso/' + esc(c.id) + '"><span class="mi-curso-titulo">' + esc(c.titulo) + "</span>" + barraProgreso(p) + "</a>";
          }).join("") : '<p class="seccion-bajada">Todavía no tienes cursos habilitados. Elige uno abajo y solicita la inscripción.</p>') + "</section>";
      }
      var ruta = lista.filter(function (c) { return c.tipo === "curso"; }).sort(function (a, b) { return (a.orden || 0) - (b.orden || 0); });
      var extras = lista.filter(function (c) { return c.tipo !== "curso"; });
      if (ruta.length) {
        html += '<section class="seccion-inicio"><h2 class="seccion-titulo">Cursos</h2>' +
          '<p class="seccion-bajada">Cada curso reúne módulos obligatorios y optativos de seis sesiones. Un módulo aprobado vale en todos los cursos que lo incluyen.</p>' + ruta.map(tarjeta).join("") + "</section>";
      }
      if (extras.length) {
        html += '<section class="seccion-inicio"><h2 class="seccion-titulo">Módulos que puedes tomar por separado</h2>' +
          '<p class="seccion-bajada">Formaciones breves de seis sesiones. Si después te inscribes en un curso que las incluye, se te reconocen.</p>';
        var categoria = null;
        extras.forEach(function (c) {
          if (c.categoria && c.categoria !== categoria) {
            categoria = c.categoria;
            html += '<h3 class="categoria-titulo">' + esc(categoria) + "</h3>";
          }
          html += tarjeta(c);
        });
        html += "</section>";
      }
      pintar(html);
    });
  }

  function vistaCurso(id) {
    return cargarCurso(id).then(function (c) {
      var p = progreso(c);
      var h = hechas(c.id);
      var siguiente = c.clases.filter(function (x) { return h.indexOf(x.id) < 0 && !moduloBloqueado(c, x.modulo); })[0];
      var html = '<nav class="migas"><a href="#/">Inicio</a></nav>';
      html += '<section class="portada"><p class="subtitulo">' + (c.tipo === "curso" ? "Curso · " : (c.categoria ? esc(c.categoria) + " · " : (c.institucion ? esc(c.institucion) + " · " : ""))) + esc(c.subtitulo) + "</p><h1>" + esc(c.titulo) + "</h1><p>" + esc(c.descripcion) + "</p>" +
        '<ul class="etiquetas"><li>' + esc(c.duracion) + "</li><li>" + esc(c.modalidad) + "</li>" + (c.publico ? "<li>" + esc(c.publico) + "</li>" : "") + "</ul>" +
        (acceso(c) === "libre" ? barraProgreso(p) : "") +
        '<div class="botones">' +
        (siguiente && acceso(c) === "libre" ? '<a class="boton principal" href="#/clase/' + esc(c.id) + "/" + esc(siguiente.id) + '">' + (p.hechas ? "Continuar" : "Comenzar") + "</a>" : "") +
        (c.programa ? '<a class="boton" href="#/curso/' + esc(c.id) + '/programa">Programa</a>' : "") +
        (c.sesiones && c.sesiones.length ? '<a class="boton" href="#/curso/' + esc(c.id) + '/sesiones">Sesiones en vivo</a>' : "") + "</div></section>";

      var tipoAcceso = acceso(c);
      if (tipoAcceso !== "libre") html += '<section class="tarjeta">' + bloqueAcceso(c, tipoAcceso) + "</section>";
      var vistoOpt = false;
      if (c.tipo === "curso") html += '<h2 class="seccion-titulo">Módulos obligatorios</h2><p class="seccion-bajada">Se cursan en orden: cada uno se habilita al completar el anterior.</p>';
      c.modulos.forEach(function (m) {
        var hm = m.clases.filter(function (x) { return h.indexOf(x.id) >= 0; }).length;
        if (m.tipo === "optativo" && !vistoOpt) {
          vistoOpt = true;
          html += '<h2 class="seccion-titulo">Módulos optativos</h2><p class="seccion-bajada">Elige ' + (c.elige === 1 ? "uno" : c.elige) + '. Puedes cursarlos en cualquier momento.</p>';
        }
        html += '<section class="tarjeta modulo"><h2>' + esc(etiquetaModulo(m)) + ". " + esc(m.titulo) + "</h2>" +
          (m.semanas ? '<p class="semanas">Semanas ' + esc(m.semanas) + "</p>" : "") +
          (m.duracion || m.constancia ? '<p class="semanas">' + [m.duracion ? esc(m.duracion) : "", m.constancia ? '<span class="chip-constancia">Constancia propia</span>' : ""].filter(Boolean).join(" · ") +
            (m.constancia ? " · " + hm + " de " + m.clases.length + " completadas" : "") + "</p>" : "");
        if (m.intro) html += '<details><summary>Sobre este módulo</summary><div class="texto">' + md(m.intro) + "</div></details>";
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
        }).join("") + "</ol></section>";
      });
      if (c.credito) html += '<p class="credito">' + esc(c.credito) + "</p>";
      pintar(html, c.titulo);
      activarSolicitudes();
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

    var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>";
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

    if (ocultas) html += '<p class="aviso">Esta clase incluye una guía para el relator. Actívala con el interruptor «Vista relator» de la parte superior.</p>';

    html += '<div class="botones"><button class="boton ' + (hecha ? "hecho" : "principal") + '" id="marcar">' +
      (hecha ? "&#10003; Clase completada" : "Marcar como completada") + "</button></div>";

    html += navegacionClases(c, i);

    pintar(html, cl.titulo);
    activarClase(c, cl);
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
    html += navegacionClases(c, i);
    pintar(html, ev.titulo);

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

  function vistaPerfil() {
    var e = cuentaActual();
    if (!Nube.habilitada) { location.hash = "#/"; return Promise.resolve(); }
    if (e.status === "invitado") { location.hash = "#/ingresar"; return Promise.resolve(); }
    if (!e.cuenta) { pintar(migas() + '<section class="tarjeta"><h1>Mi cuenta</h1><p class="aviso error">' + esc(e.error || "No se pudo cargar tu cuenta.") + '</p><div class="botones"><button class="boton" id="salir">Salir</button></div></section>', "Mi cuenta"); enlazarSalir(); return Promise.resolve(); }
    var c = e.cuenta;
    var html = migas("Mi cuenta") + '<section class="tarjeta"><h1>Mi cuenta</h1>' +
      '<p class="estado-cuenta estado-' + esc(c.estado) + '">' + esc(ROLES[c.rol] || c.rol) + " · " + esc(ESTADOS[c.estado] || c.estado) + "</p>" +
      (c.estado === "pendiente" ? '<p class="aviso">Tu cuenta está en revisión. Un relator o administrador la aprobará y te habilitará los cursos que solicites.</p>' : "") +
      (c.estado === "pausado" ? '<p class="aviso">Tu cuenta está en pausa. Conversa con tu relator o con la coordinación de Mi Ruta.</p>' : "") +
      '<form id="form-perfil" class="formulario"><label>Nombre y apellido<input name="nombre" value="' + esc(c.nombre) + '" required></label>' +
      '<label>Comunidad o parroquia<input name="comunidad" value="' + esc(c.comunidad) + '"></label>' +
      '<label>Correo<input value="' + esc(c.correo) + '" disabled></label>' +
      '<div class="botones"><button class="boton principal" type="submit">Guardar cambios</button></div><div class="mensaje" aria-live="polite"></div></form>' +
      '<div class="botones">' +
      (e.activo ? '<a class="boton" href="#/mis-constancias">Mis constancias</a>' : "") +
      (e.esRelator ? '<a class="boton" href="#/gestion">Gestión</a>' : "") +
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
      d.detalle = "por haber aprobado el curso " + c.titulo + ": " + obl.length + " módulos obligatorios y " + (c.elige || 0) + (c.elige === 1 ? " optativo" : " optativos") + ", con un total de " + c.horas + " horas de formación.";
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
    var p = String(iso || "").split("-");
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

  function vistaGestion() {
    var e = cuentaActual();
    if (!e.esRelator) { location.hash = "#/"; return Promise.resolve(); }
    pintar(migas("Gestión") + '<p class="cargando">Cargando participantes…</p>', "Gestión");
    return Promise.all([Nube.listarUsuarios(), Promise.all(sitio.cursos.map(cargarCurso))]).then(function (r) {
      var usuarios = r[0], lista = r[1];
      var porId = {}; lista.forEach(function (c) { porId[c.id] = c; });
      var pendientes = usuarios.filter(function (u) { return u.estado === "pendiente" || (u.estado === "activo" && (u.solicitudes || []).length); });
      var filtro = almacen.leer("gestion:filtro", "");

      function nombreCurso(id) { return porId[id] ? porId[id].titulo : id; }

      function fichaPendiente(u) {
        var sol = (u.solicitudes || []);
        return '<li class="ficha" data-uid="' + esc(u.uid) + '"><div class="ficha-cabeza"><b>' + esc(u.nombre) + '</b><span>' + esc(u.correo) + (u.comunidad ? " · " + esc(u.comunidad) : "") + "</span></div>" +
          (u.estado === "pendiente" ? '<p class="ficha-nota">Cuenta nueva, en revisión.</p>' : "") +
          (sol.length ? '<p class="ficha-nota">Solicita: ' + sol.map(function (id) { return esc(nombreCurso(id)); }).join(", ") + "</p>" : "") +
          '<div class="botones"><button class="boton principal" data-accion="aprobar">' + (u.estado === "pendiente" ? "Aprobar" : "Inscribir") + (sol.length ? " e inscribir" : "") + "</button>" +
          (u.estado === "pendiente" ? '<button class="boton" data-accion="pausar">Rechazar</button>' : '<button class="boton" data-accion="descartar">Descartar solicitud</button>') + "</div></li>";
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

      var html = migas("Gestión") + '<section class="portada"><h1>Gestión</h1><p>Aprueba cuentas, inscribe en cursos, revisa avances y emite constancias.</p>' +
        '<ul class="etiquetas"><li>' + usuarios.length + " cuentas</li><li>" + pendientes.length + " por revisar</li></ul></section>" +
        '<section class="tarjeta"><h2>Por revisar</h2>' + (pendientes.length ? '<ul class="fichas">' + pendientes.map(fichaPendiente).join("") + "</ul>" : '<p class="seccion-bajada">No hay solicitudes pendientes.</p>') + "</section>" +
        '<section class="tarjeta"><h2>Participantes</h2><label class="buscador">Buscar<input id="filtro" value="' + esc(filtro) + '" placeholder="Nombre, correo o comunidad"></label>' +
        '<ul class="fichas">' + participantes.map(fichaParticipante).join("") + "</ul></section>" +
        '<section class="tarjeta"><h2>Constancias emitidas</h2><div id="constancias-emitidas"><button class="boton" id="ver-constancias">Ver constancias emitidas</button></div></section>';
      pintar(html, "Gestión");

      var buscar = document.getElementById("filtro");
      buscar.addEventListener("change", function () { almacen.guardar("gestion:filtro", buscar.value.trim()); vistaGestion(); });

      document.getElementById("ver-constancias").addEventListener("click", function () {
        var caja = document.getElementById("constancias-emitidas");
        caja.innerHTML = '<p class="cargando">Cargando…</p>';
        Nube.todasLasConstancias().then(function (cs) {
          caja.innerHTML = cs.length ? '<ul class="lista-constancias">' + cs.sort(function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); }).map(function (d) {
            return '<li><a href="#/constancia/' + esc(d.folio) + '"><b>' + esc(d.nombre) + " · " + esc(d.titulo) + "</b><span>" + esc(d.folio) + " · " + esc(fechaLarga(d.fecha)) + "</span></a></li>";
          }).join("") + "</ul>" : '<p class="seccion-bajada">Todavía no se han emitido constancias.</p>';
        }).catch(function (er) { caja.innerHTML = '<p class="aviso error">' + esc(er.message) + "</p>"; });
      });

      app.querySelectorAll(".ficha").forEach(function (li) {
        var uid = li.getAttribute("data-uid");
        var u = usuarios.filter(function (x) { return x.uid === uid; })[0];
        var msj = li.querySelector(".mensaje") || li;
        function hecho(promesa) {
          promesa.then(vistaGestion).catch(function (er) { alertaEn(msj, er.message); });
        }
        li.querySelectorAll("[data-accion]").forEach(function (b) {
          var accion = b.getAttribute("data-accion");
          var evento = b.tagName === "SELECT" ? "change" : "click";
          b.addEventListener(evento, function () {
            if (accion === "aprobar") {
              var cursosNuevos = Array.from(new Set((u.cursos || []).concat(u.solicitudes || [])));
              hecho(Nube.actualizarUsuario(uid, { estado: "activo", cursos: cursosNuevos, solicitudes: [] }));
            } else if (accion === "descartar") {
              hecho(Nube.actualizarUsuario(uid, { solicitudes: [] }));
            } else if (accion === "pausar") {
              hecho(Nube.actualizarUsuario(uid, { estado: "pausado" }));
            } else if (accion === "activar") {
              hecho(Nube.actualizarUsuario(uid, { estado: "activo" }));
            } else if (accion === "guardar-cursos") {
              var marcados = Array.from(li.querySelectorAll(".ficha-cursos input:checked")).map(function (x) { return x.value; });
              hecho(Nube.actualizarUsuario(uid, { cursos: marcados, solicitudes: (u.solicitudes || []).filter(function (s) { return marcados.indexOf(s) < 0; }) }));
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
        '<p class="ficha-nota">Antes de emitir, confirma que aprobó las evaluaciones, la asistencia y el trabajo final que pide la formación.</p>' +
        '<div class="botones"><button class="boton principal" data-paso="1">Emitir constancia</button></div><div class="mensaje" aria-live="polite"></div></div>';
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
        Nube.emitirConstancia(datosConstancia(c, partes[1], u, op ? op.h : [])).then(function (folio) {
          msj.className = "mensaje ok";
          msj.innerHTML = 'Constancia emitida: <a href="#/constancia/' + esc(folio) + '">' + esc(folio) + "</a>";
          boton.disabled = false; boton.setAttribute("data-paso", "1"); boton.textContent = "Emitir constancia";
        }).catch(function (er) { boton.disabled = false; msj.className = "mensaje error"; msj.textContent = er.message; });
      });
    }).catch(function (er) { caja.innerHTML = '<p class="aviso error">' + esc(er.message) + "</p>"; });
  }

  /* ---------- cabecera ---------- */

  function actualizarCabecera() {
    var enlace = document.getElementById("cuenta-enlace");
    var caja = document.getElementById("caja-relator");
    var pie = document.getElementById("pie-nota");
    if (!Nube.habilitada) { enlace.hidden = true; caja.hidden = false; return; }
    var e = cuentaActual();
    caja.hidden = true;
    enlace.hidden = false;
    if (e.status === "invitado" || e.status === "error" && !e.cuenta) {
      enlace.textContent = "Ingresar"; enlace.href = "#/ingresar"; enlace.className = "cuenta-boton";
    } else if (e.cuenta) {
      var iniciales = String(e.cuenta.nombre || "?").split(/\s+/).filter(Boolean).slice(0, 2).map(function (x) { return x[0]; }).join("").toUpperCase();
      enlace.textContent = iniciales; enlace.href = "#/perfil"; enlace.className = "cuenta-boton avatar" + (modoRelator() ? " relator" : "");
      enlace.title = e.cuenta.nombre + (modoRelator() ? " · vista relator" : "");
    }
    if (pie) pie.textContent = e.activo ? "Tu avance se guarda en tu cuenta y te acompaña en todos tus dispositivos." : "Con tu cuenta, tu avance te acompaña en todos tus dispositivos.";
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
    var partes = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean).map(decodeURIComponent);
    var tarea;
    actualizarCabecera();
    if (partes[0] === "curso" && partes[1] && partes[2] === "programa") tarea = vistaPrograma(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "sesiones") tarea = vistaSesiones(partes[1]);
    else if (partes[0] === "curso" && partes[1]) tarea = vistaCurso(partes[1]);
    else if (partes[0] === "clase" && partes[1] && partes[2]) tarea = vistaClase(partes[1], partes[2]);
    else if (partes[0] === "ingresar") tarea = vistaIngresar();
    else if (partes[0] === "perfil") tarea = vistaPerfil();
    else if (partes[0] === "gestion") tarea = vistaGestion();
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

  // Al ingresar o salir, se vuelve a dibujar la vista. Después de ingresar, se va a la portada.
  Nube.alCambiar(function () {
    if (/^#\/ingresar/.test(location.hash) && cuentaActual().cuenta) location.hash = "#/";
    else ruta();
  });

  Promise.resolve(Nube.listo).then(cargarSitio).then(ruta).catch(error);
})();
