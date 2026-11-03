/* Estudio AGP: aula virtual estática.
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
  var ROMANOS = ["", "I", "II", "III", "IV", "V", "VI"];

  /* ---------- utilidades ---------- */

  var almacen = {
    leer: function (clave, defecto) {
      try {
        var v = localStorage.getItem("agp:" + clave);
        return v === null ? defecto : JSON.parse(v);
      } catch (e) { return defecto; }
    },
    guardar: function (clave, valor) {
      try { localStorage.setItem("agp:" + clave, JSON.stringify(valor)); } catch (e) { /* sin almacenamiento */ }
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

  function modoRelator() { return almacen.leer("modoRelator", false); }

  function cargarSitio() {
    if (sitio) return Promise.resolve(sitio);
    return pedir("datos/sitio.json").then(function (s) {
      sitio = s;
      document.getElementById("marca-nombre").textContent = s.nombre;
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

  function hechas(cursoId) { return almacen.leer("hechas:" + cursoId, []); }

  function marcarHecha(cursoId, claseId, valor) {
    var lista = hechas(cursoId).filter(function (x) { return x !== claseId; });
    if (valor) lista.push(claseId);
    almacen.guardar("hechas:" + cursoId, lista);
  }

  function progreso(curso) {
    var h = hechas(curso.id);
    var n = curso.clases.filter(function (c) { return h.indexOf(c.id) >= 0; }).length;
    return { hechas: n, total: curso.clases.length, pct: curso.clases.length ? Math.round(100 * n / curso.clases.length) : 0 };
  }

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
    document.title = titulo ? titulo + " · " + (sitio ? sitio.nombre : "Estudio AGP") : (sitio ? sitio.nombre : "Estudio AGP");
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
      var html = '<section class="portada"><h1>' + esc(sitio.nombre) + "</h1><p>" + esc(sitio.lema) + "</p></section>";
      html += lista.map(function (c) {
        var p = progreso(c);
        return '<article class="tarjeta curso-tarjeta">' + (c.institucion ? '<p class="institucion">' + esc(c.institucion) + "</p>" : "") + '<h2>' + esc(c.titulo) + '</h2><p class="subtitulo">' + esc(c.subtitulo) +
          "</p><p>" + esc(c.descripcion) + "</p><p class=\"meta\">" + [c.duracion, c.modalidad, c.publico].filter(Boolean).map(esc).join(" · ") + "</p>" +
          barraProgreso(p) + '<div class="botones"><a class="boton principal" href="#/curso/' + esc(c.id) + '">Entrar al curso</a></div></article>';
      }).join("");
      pintar(html);
    });
  }

  function vistaCurso(id) {
    return cargarCurso(id).then(function (c) {
      var p = progreso(c);
      var h = hechas(c.id);
      var siguiente = c.clases.filter(function (x) { return h.indexOf(x.id) < 0; })[0];
      var html = '<nav class="migas"><a href="#/">Inicio</a></nav>';
      html += '<section class="portada"><p class="subtitulo">' + (c.institucion ? esc(c.institucion) + " · " : "") + esc(c.subtitulo) + "</p><h1>" + esc(c.titulo) + "</h1><p>" + esc(c.descripcion) + "</p>" +
        '<ul class="etiquetas"><li>' + esc(c.duracion) + "</li><li>" + esc(c.modalidad) + "</li>" + (c.publico ? "<li>" + esc(c.publico) + "</li>" : "") + "</ul>" +
        barraProgreso(p) +
        '<div class="botones">' +
        (siguiente ? '<a class="boton principal" href="#/clase/' + esc(c.id) + "/" + esc(siguiente.id) + '">' + (p.hechas ? "Continuar" : "Comenzar") + "</a>" : "") +
        (c.programa ? '<a class="boton" href="#/curso/' + esc(c.id) + '/programa">Programa</a>' : "") +
        (c.sesiones && c.sesiones.length ? '<a class="boton" href="#/curso/' + esc(c.id) + '/sesiones">Sesiones en vivo</a>' : "") + "</div></section>";

      c.modulos.forEach(function (m) {
        html += '<section class="tarjeta modulo"><h2>Módulo ' + ROMANOS[m.numero] + ". " + esc(m.titulo) + "</h2>" + (m.semanas ? '<p class="semanas">Semanas ' + esc(m.semanas) + "</p>" : "");
        if (m.intro) html += '<details><summary>Sobre este módulo</summary><div class="texto">' + md(m.intro) + "</div></details>";
        html += '<ol class="lista-clases">' + m.clases.map(function (cl) {
          var hecha = h.indexOf(cl.id) >= 0;
          return '<li class="' + (hecha ? "hecha" : "") + '"><a href="#/clase/' + esc(c.id) + "/" + esc(cl.id) + '">' +
            '<span class="estado" aria-label="' + (hecha ? "Completada" : "Pendiente") + '">' + (hecha ? "&#10003;" : "") + "</span>" +
            '<span><span class="etiqueta-clase">' + esc(cl.etiqueta) + "</span>" + esc(cl.titulo) + "</span>" +
            '<span class="semana">' + esc(duracionClase(cl)) + "</span></a></li>";
        }).join("") + "</ol></section>";
      });
      if (c.credito) html += '<p class="credito">' + esc(c.credito) + "</p>";
      pintar(html, c.titulo);
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
        '<ol class="sesiones">' + c.sesiones.map(function (s) {
          var cuando = [s.fecha, s.hora, s.lugar].filter(Boolean).join(" · ") || "Fecha por definir";
          var enlace = s.enlace || "";
          return '<li><span class="num">Semana ' + esc(s.semana) + '</span><span><span class="tema">' + esc(s.tema) +
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
      if (cl.tipo === "evaluacion") {
        return pedir("datos/evaluaciones-" + cursoId + ".json").then(function (ev) {
          if (!ev[cl.id]) throw new Error("La evaluación no existe.");
          armarEvaluacion(c, cl, i, ev[cl.id]);
        });
      }
      return pedir("contenido/" + cursoId + "/" + claseId + ".md", "texto").then(function (texto) {
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
    html += '<header class="clase-cabecera"><span class="etiqueta-clase">Módulo ' + ROMANOS[cl.modulo.numero] + " · " + esc(cl.etiqueta) + "</span>" +
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
    var clave = "eval:" + c.id + ":" + cl.id;
    var previo = almacen.leer(clave, null);
    // Las opciones se barajan en cada intento para que la posición no delate la respuesta.
    var ordenes = ev.preguntas.map(function (p) {
      var o = p.opciones.map(function (_, j) { return j; });
      for (var a = o.length - 1; a > 0; a--) { var b = Math.floor(Math.random() * (a + 1)); var t = o[a]; o[a] = o[b]; o[b] = t; }
      return o;
    });
    var html = '<nav class="migas"><a href="#/">Inicio</a> / <a href="#/curso/' + esc(c.id) + '">' + esc(c.titulo) + "</a></nav>";
    html += '<header class="clase-cabecera"><span class="etiqueta-clase">Módulo ' + ROMANOS[cl.modulo.numero] + " · Evaluación</span>" +
      "<h1>" + esc(ev.titulo) + '</h1><p class="meta">' + ev.preguntas.length + " preguntas · se aprueba con " + ev.aprobacion + "%</p></header>";
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

  /* ---------- enrutador ---------- */

  function ruta() {
    var partes = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean).map(decodeURIComponent);
    var tarea;
    if (partes[0] === "curso" && partes[1] && partes[2] === "programa") tarea = vistaPrograma(partes[1]);
    else if (partes[0] === "curso" && partes[1] && partes[2] === "sesiones") tarea = vistaSesiones(partes[1]);
    else if (partes[0] === "curso" && partes[1]) tarea = vistaCurso(partes[1]);
    else if (partes[0] === "clase" && partes[1] && partes[2]) tarea = vistaClase(partes[1], partes[2]);
    else tarea = vistaInicio();
    return tarea.catch(error);
  }

  var interruptor = document.getElementById("modo-relator");
  interruptor.checked = modoRelator();
  interruptor.addEventListener("change", function () {
    almacen.guardar("modoRelator", interruptor.checked);
    ruta();
  });

  window.addEventListener("hashchange", ruta);
  cargarSitio().then(ruta).catch(error);
})();
