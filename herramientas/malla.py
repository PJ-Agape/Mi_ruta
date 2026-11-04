"""Arma los cursos de Mi Ruta a partir del dossier de módulos.

Uso (desde la raíz del repositorio, después de formaciones.py, complementarias.py y dividir.py):
    python3 herramientas/malla.py

Cada módulo tiene 6 sesiones: 5 de contenido y 1 de cierre. Las sesiones toman su
contenido de las formaciones ya generadas (contenido/<formación>/...), de las sesiones
nuevas del diplomado (fuentes/diplomado/) o de la fusión de dos clases.

Genera:
  - contenido/modulos/<módulo>/<sesión>.md      contenido de cada sesión
  - datos/curso-<curso>.json, datos/indice-<curso>.json, datos/evaluaciones-<curso>.json
    para los 6 cursos y para cada módulo que se puede tomar por separado
  - datos/sitio.json                            lista y orden de los cursos

Los identificadores de las sesiones son únicos en toda la plataforma (<módulo>-s1 …
<módulo>-cierre), así una sesión aprobada cuenta en todos los cursos que incluyen el módulo.
"""
import json
import pathlib
import re
import shutil
import sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / "herramientas" / "nuevas"))
from talleres import TALLERES, EVAL_DJ  # noqa: E402
from referencias import REFS  # noqa: E402
sys.path.insert(0, str(R / "herramientas"))
from formaciones import md  # noqa: E402

CONT = R / "contenido"
DATOS = R / "datos"


def leer_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def titulo_de(curso, clase):
    for m in leer_json(DATOS / f"indice-{curso}.json")["modulos"]:
        for c in m["clases"]:
            if c["id"] == clase:
                return c["titulo"]
    raise KeyError((curso, clase))


def secciones(texto, nivel="### "):
    """Separa un markdown en (introducción, [(título, cuerpo)]) por encabezados de un nivel."""
    partes = re.split(r"(?m)^" + re.escape(nivel), texto)
    intro = partes[0].strip()
    out = []
    for p in partes[1:]:
        t, _, cuerpo = p.partition("\n")
        out.append((t.strip(), cuerpo.strip()))
    return intro, out


def bajar(texto):
    return re.sub(r"(?m)^(#{4,5}) ", lambda m: "#" + m.group(1) + " ", texto)


def unir(intro, secs):
    return (intro + "\n\n" if intro else "") + "\n\n".join(f"### {t}\n\n{c}" for t, c in secs) + "\n"


def fusion_unidad(a, b, titulo_b):
    """Une dos unidades de 90 minutos: la segunda entra como parte del momento «Aprender» de la primera."""
    ia, sa = secciones(a)
    ib, sb = secciones(b)
    aprender_b = next(c for t, c in sb if t.startswith("Aprender"))
    out = []
    for t, c in sa:
        if t.startswith("Aprender"):
            c = c + f"\n\n#### {titulo_b}\n\n" + bajar(aprender_b)
        out.append((t, c))
    return unir(ia, out)


def fusion_clase(a, b, ta, tb):
    """Une dos clases del diplomado: un solo apunte en dos partes, ambas plantillas, una guía y una aplicación."""
    ia, sa = secciones(a)
    ib, sb = secciones(b)
    def toma(secs, pref):
        return [(t, c) for t, c in secs if t.startswith(pref)]
    out = []
    ap = [c for t, c in toma(sa, "Apunte")] + [c for t, c in toma(sb, "Apunte")]
    out.append(("Apunte", f"#### Parte 1. {ta}\n\n" + bajar(ap[0]) + f"\n\n#### Parte 2. {tb}\n\n" + bajar(ap[1])))
    out += toma(sa, "Plantilla") + toma(sb, "Plantilla")
    gu = [(f"Parte 1. {ta}", c) for t, c in toma(sa, "Guía")] + [(f"Parte 2. {tb}", c) for t, c in toma(sb, "Guía")]
    if gu:
        out.append(("Guía de los ejercicios para el relator", "\n\n".join(f"#### {t}\n\n" + bajar(c) for t, c in gu)))
    apl = toma(sa, "Aplicación") + toma(sb, "Aplicación")
    if apl:
        out.append(("Aplicación y bitácora", "\n\n".join(bajar(c) for t, c in apl)))
    intro = " ".join(x for x in (ia, ib) if x)
    return unir(intro, out)


def parte_de(texto, quiere):
    intro, secs = secciones(texto)
    return unir(intro if quiere(None) else "", [(t, c) for t, c in secs if quiere(t)])


# ---------------- sesiones ----------------
def U(curso, clase):
    return {"tipo": "unidad", "titulo": titulo_de(curso, clase), "texto": (CONT / curso / f"{clase}.md").read_text(encoding="utf-8"), "tiempo": "90 min"}


def FU(curso, a, b, titulo):
    return {"tipo": "unidad", "titulo": titulo, "fusion": True, "tiempo": "90 min",
            "texto": fusion_unidad((CONT / curso / f"{a}.md").read_text(encoding="utf-8"), (CONT / curso / f"{b}.md").read_text(encoding="utf-8"), titulo_de(curso, b))}


def L(clase, titulo=None):
    return {"tipo": "clase", "titulo": titulo or titulo_de("liderazgo", clase), "texto": (CONT / "liderazgo" / f"{clase}.md").read_text(encoding="utf-8"), "tiempo": "Sesión del diplomado"}


def FL(a, b, titulo):
    ta, tb = titulo_de("liderazgo", a), titulo_de("liderazgo", b)
    return {"tipo": "clase", "titulo": titulo, "fusion": True, "tiempo": "Sesión del diplomado",
            "texto": fusion_clase((CONT / "liderazgo" / f"{a}.md").read_text(encoding="utf-8"), (CONT / "liderazgo" / f"{b}.md").read_text(encoding="utf-8"), ta, tb)}


def N(archivo, titulo, tipo="clase"):
    return {"tipo": tipo, "titulo": titulo, "texto": (R / "fuentes" / "diplomado" / archivo).read_text(encoding="utf-8"), "tiempo": "Sesión del diplomado"}


def complementaria(cid):
    f = leer_json(R / "fuentes" / "complementarias" / f"{cid}.json")
    ses = [{"tipo": "unidad", "titulo": md(u["title"]), "tiempo": "90 min",
            "texto": (CONT / cid / f"m1-u{i:02d}.md").read_text(encoding="utf-8")} for i, u in enumerate(f["unidades"], 1)]
    assert len(ses) == 5, (cid, len(ses))
    preguntas = [{"pregunta": md(q["q"]), "opciones": [md(o) for o in q["options"]], "correcta": q["correct"],
                  "explicacion": md(q.get("feedback", ""))} for q in f["evaluacion"]]
    return {"titulo": f["titulo"], "categoria": f["categoria"], "intro": f.get("intro", ""), "sesiones": ses,
            "taller": f.get("taller") or TALLERES[cid], "preguntas": preguntas, "horas": 9,
            "ficha": {k: f[k] for k in ("subtitulo", "descripcion", "publico") if k in f}}


def dj(titulo, ses, clave):
    preguntas = []
    for curso, ev, idx in EVAL_DJ[clave]:
        p = leer_json(DATOS / f"evaluaciones-{curso}.json")[ev]["preguntas"]
        preguntas += [p[i] for i in idx]
    return {"titulo": titulo, "sesiones": ses, "taller": TALLERES[clave], "preguntas": preguntas, "horas": 9}


def dip(titulo, ses, cierre):
    return {"titulo": titulo, "sesiones": ses, "cierre": cierre, "horas": 27}


D, A, C = "discernimiento-y-oracion", "arte-de-encontrarnos", "coordinar-es-servir"
COMPLEMENTARIAS = ["servidores-del-altar", "lectores-y-salmistas", "musica-liturgica", "conocer-la-biblia", "santos-jovenes",
                   "el-credo", "sacramentos", "misiones-juveniles", "ayudante-de-catequesis", "voluntariado-y-doctrina-social",
                   "ecologia-integral", "buen-trato-y-prevencion", "primeros-auxilios", "primeros-auxilios-psicologicos",
                   "comunicacion-y-redes", "dinamicas-y-juegos", "logistica"]


def modulos():
    M = {cid: complementaria(cid) for cid in COMPLEMENTARIAS}
    M["dj-discernimiento"] = dj("Oración y discernimiento vocacional", [U(D, f"m1-u0{i}") for i in range(1, 6)], "dj-discernimiento")
    M["dj-identidad"] = dj("Identidad y espiritualidad del agente pastoral", [U(A, "m1-u01"), U(A, "m1-u02"), U(A, "m1-u05"), U(A, "m1-u06"), U(A, "m5-u01")], "dj-identidad")
    M["dj-acogida"] = dj("Acogida y vida de grupo", [U(A, "m2-u01"), U(A, "m2-u02"), U(A, "m2-u03"), U(A, "m2-u04"), U(A, "m1-u04")], "dj-acogida")
    M["dj-escucha"] = dj("Escucha y acompañamiento", [U(A, "m1-u03"), U(A, "m3-u01"), U(A, "m3-u02"), U(A, "m3-u04"), U(A, "m5-u04")], "dj-escucha")
    M["dj-metodologia"] = dj("Metodología y animación de grupos", [U(A, "m4-u01"), U(A, "m4-u02"), U(A, "m4-u03"), U(A, "m4-u04"), U(A, "m3-u03")], "dj-metodologia")
    M["dj-eucaristia"] = dj("Eucaristía y vida litúrgica del grupo", [U(A, f"m6-u0{i}") for i in range(1, 6)], "dj-eucaristia")
    M["dj-coordinar"] = dj("Coordinar, planificar y administrar", [FU(C, "m1-u01", "m1-u03", "Coordinar es servir, con la Eucaristía en el centro del equipo"), U(C, "m1-u02"), U(C, "m2-u01"), U(C, "m2-u02"), U(C, "m3-u02")], "dj-coordinar")
    M["dj-conducir"] = dj("Conducir el equipo", [U(C, "m2-u03"), U(C, "m3-u01"), U(C, "m3-u03"), U(C, "m4-u01"), U(C, "m4-u02")], "dj-conducir")
    M["dj-proyectar"] = dj("Proyectar el grupo: cuidado, relevo y envío", [U(A, "m5-u02"), U(C, "m4-u03"), U(C, "m5-u02"), U(C, "m5-u03"), U(A, "m5-u05")], "dj-proyectar")
    s02 = (CONT / "liderazgo" / "m7-s02.md").read_text(encoding="utf-8")
    presentar = parte_de(s02, lambda t: t is None or t.startswith(("Presentaciones", "Rúbrica", "Pauta")))
    ceremonia = parte_de(s02, lambda t: t is not None and not t.startswith(("Presentaciones", "Rúbrica", "Pauta")))
    M["dip-1"] = dip("I · Fundamentos del liderazgo personal", [L(f"m1-c0{i}") for i in range(1, 6)], N("cierre-i.md", "Cierre: taller y evaluación del módulo", "taller"))
    M["dip-2"] = dip("II · Autoridad, decisiones y gestión del grupo", [L("m1-c06"), L("m1-c07"), L("m1-c08"), FL("m1-c09", "m1-c10", "Atraer y conectar"), L("m1-c11")], N("cierre-ii.md", "Cierre: taller y evaluación del módulo", "taller"))
    M["dip-3"] = dip("III · Formación de equipos y delegación", [L("m2-c11"), L("m2-c12"), L("m2-c13"), L("m2-c14"), FL("m2-c15", "m2-c16", "Hacer que las cosas pasen y cuidar el impulso")], dict(L("m2-s10", "Cierre: jornada del módulo"), tipo="taller"))
    M["dip-4"] = dip("IV · Gestión del tiempo, autocuidado y legado", [L(f"m3-c{i}") for i in range(17, 22)], N("cierre-iv.md", "Cierre: taller y evaluación del módulo", "taller"))
    M["dip-5"] = dip("V · Comunicación y mediación de conflictos", [L("m4-c01"), L("m4-c02"), FL("m4-c03", "m4-c04", "Decir lo difícil: mensaje DESC y conversaciones difíciles"), L("m4-c05"), L("m4-c06")], dict(L("m4-s04", "Cierre: taller de protocolo de comunicación"), tipo="taller"))
    M["dip-6"] = dip("VI · Planificación y gestión de proyectos", [FL("m5-c01", "m5-c02", "De la visión al plan, leyendo la realidad"), L("m5-c03"), L("m5-c04"), L("m5-c05"), L("m5-c06")], dict(L("m5-s04", "Cierre: taller del plan anual del grupo"), tipo="taller"))
    M["dip-7"] = dip("VII · Acompañamiento y desarrollo de personas", [L("m6-c01"), L("m6-c02"), FL("m6-c03", "m6-c04", "Reconocer, corregir y motivar"), L("m6-c05"), L("m6-c06")], dict(L("m6-s04", "Cierre: taller del plan de acompañamiento"), tipo="taller"))
    M["dip-8"] = dip("VIII · Proyecto integrador", [L("m7-s01", "Taller de lanzamiento del proyecto"), N("asesoria-1.md", "Asesoría 1: diagnóstico"), N("asesoria-2.md", "Asesoría 2: plan de acción"), N("asesoria-3.md", "Asesoría 3: ejecución y evidencias"),
                                                     {"tipo": "clase", "titulo": "Presentaciones de los proyectos", "texto": presentar, "tiempo": "Sesión del diplomado"}],
                     {"tipo": "taller", "titulo": "Cierre: evaluación del diplomado y ceremonia", "texto": ceremonia, "tiempo": "Sesión del diplomado"})
    return M


CURSOS = [
 {"id": "dirigente-juvenil", "titulo": "Dirigente juvenil", "subtitulo": "Discernir, animar, acompañar y coordinar un grupo de pastoral juvenil",
  "descripcion": "La formación base para quienes quieren servir como dirigentes: parte por el discernimiento vocacional y recorre la identidad del agente pastoral, la vida de grupo, la escucha, la metodología, la Eucaristía, el buen trato y la coordinación del equipo.",
  "publico": "Desde 13 años", "elige": 2,
  "obligatorios": ["dj-discernimiento", "dj-identidad", "dj-acogida", "dj-escucha", "dj-metodologia", "dj-eucaristia", "buen-trato-y-prevencion", "dj-coordinar", "dj-conducir", "dj-proyectar"],
  "optativos": ["dinamicas-y-juegos", "primeros-auxilios", "comunicacion-y-redes", "primeros-auxilios-psicologicos", "logistica"]},
 {"id": "diplomado", "titulo": "Diplomado en liderazgo para equipos de pastoral juvenil", "subtitulo": "Conducir equipos, acompañar personas y gestionar proyectos",
  "descripcion": "Para dirigentes con experiencia que asumen la conducción de equipos. Ocho módulos con constancia propia: liderazgo personal, autoridad y decisiones, formación de equipos, gestión del tiempo y legado, comunicación y conflictos, planificación de proyectos, acompañamiento de personas y un proyecto integrador. Modalidad mixta: sesiones presenciales o en línea con el relator y trabajo personal.",
  "publico": "Desde 17 años, con el curso Dirigente juvenil aprobado", "elige": 1, "modalidad": "Mixta: encuentros con relator y trabajo personal",
  "obligatorios": [f"dip-{i}" for i in range(1, 9)],
  "optativos": ["primeros-auxilios-psicologicos", "comunicacion-y-redes", "voluntariado-y-doctrina-social", "logistica"],
  "requiere": {"dip-2": ["dip-1"], **{f"dip-{i}": ["dip-1", "dip-2"] for i in range(3, 8)}, "dip-8": [f"dip-{i}" for i in range(1, 8)]}},
 {"id": "servicio-liturgico", "titulo": "Servicio litúrgico", "subtitulo": "El altar, la Palabra y el canto",
  "descripcion": "Para jóvenes que sirven en la celebración: servidores del altar, lectores y salmistas, y música litúrgica, con el buen trato como base del servicio.",
  "publico": "Desde 13 años", "elige": 1,
  "obligatorios": ["servidores-del-altar", "lectores-y-salmistas", "musica-liturgica", "buen-trato-y-prevencion"],
  "optativos": ["conocer-la-biblia", "santos-jovenes"]},
 {"id": "fe-y-catequesis", "titulo": "Fe y catequesis", "subtitulo": "Conocer la fe y ayudar a transmitirla",
  "descripcion": "Para quienes quieren conocer mejor su fe y apoyar la catequesis de niños y jóvenes: la Biblia, los santos jóvenes y el servicio de ayudante de catequesis.",
  "publico": "Desde 14 años", "elige": 1,
  "obligatorios": ["conocer-la-biblia", "santos-jovenes", "ayudante-de-catequesis", "buen-trato-y-prevencion"],
  "optativos": ["dinamicas-y-juegos", "comunicacion-y-redes"]},
 {"id": "mision-y-servicio", "titulo": "Misión y servicio", "subtitulo": "Salir al encuentro y cuidar la casa común",
  "descripcion": "Para jóvenes que quieren salir al encuentro: voluntariado y doctrina social, ecología integral, misiones juveniles y la logística que las hace posibles.",
  "publico": "Desde 14 años", "elige": 1,
  "obligatorios": ["voluntariado-y-doctrina-social", "ecologia-integral", "misiones-juveniles", "logistica", "buen-trato-y-prevencion"],
  "optativos": ["primeros-auxilios", "dinamicas-y-juegos"]},
 {"id": "catequista", "titulo": "Catequista y agente de pastoral", "subtitulo": "Transmitir la fe y servir en la comunidad",
  "descripcion": "Forma catequistas con mirada de agente de pastoral: conocen la fe y los sacramentos, preparan y animan la catequesis, acompañan personas, animan grupos y coordinan con la comunidad.",
  "publico": "Desde 16 años", "elige": 2,
  "obligatorios": ["dj-identidad", "conocer-la-biblia", "el-credo", "sacramentos", "ayudante-de-catequesis", "dj-metodologia", "dj-escucha", "dj-eucaristia", "buen-trato-y-prevencion", "dj-coordinar"],
  "optativos": ["santos-jovenes", "dinamicas-y-juegos", "comunicacion-y-redes", "primeros-auxilios-psicologicos", "logistica"]},
]


def horas_txt(h):
    return f"{h:g}".replace(".", ",") + " horas"


def corregir(mid, archivo, texto):
    for viejo, nuevo in REFS.get((mid, archivo), []):
        if viejo not in texto:
            raise SystemExit(f"Referencia no encontrada en {mid}/{archivo}: {viejo}")
        texto = texto.replace(viejo, nuevo)
    return texto


def escribir_modulo(mid, m):
    carpeta = CONT / "modulos" / mid
    if carpeta.exists():
        shutil.rmtree(carpeta)
    carpeta.mkdir(parents=True)
    clases, evals = [], {}
    for i, s in enumerate(m["sesiones"], 1):
        sid = f"{mid}-s{i}"
        (carpeta / f"s{i}.md").write_text(corregir(mid, f"s{i}.md", s["texto"]), encoding="utf-8")
        clases.append({"id": sid, "tipo": s["tipo"], "numero": i, "etiqueta": f"Sesión {i}", "titulo": s["titulo"],
                       "tiempo": s["tiempo"], "archivo": f"contenido/modulos/{mid}/s{i}.md"})
    cid = f"{mid}-cierre"
    if "cierre" in m:
        s = m["cierre"]
        (carpeta / "cierre.md").write_text(corregir(mid, "cierre.md", s["texto"]), encoding="utf-8")
        clases.append({"id": cid, "tipo": "taller", "numero": 6, "etiqueta": "Sesión 6 · Cierre", "titulo": s["titulo"],
                       "tiempo": s["tiempo"], "archivo": f"contenido/modulos/{mid}/cierre.md"})
    else:
        clases.append({"id": cid, "tipo": "evaluacion", "numero": 6, "etiqueta": "Sesión 6 · Cierre", "titulo": "Cierre: taller práctico y evaluación",
                       "tiempo": f"Taller y {len(m['preguntas'])} preguntas"})
        evals[cid] = {"titulo": f"Cierre del módulo: {m['titulo']}", "aprobacion": 70, "taller": m["taller"], "preguntas": m["preguntas"]}
    return clases, evals


def main():
    M = modulos()
    for mid, m in M.items():
        assert len(m["sesiones"]) == 5, mid
        m["clases"], m["evals"] = escribir_modulo(mid, m)
    sitio = leer_json(DATOS / "sitio.json")
    lista = []
    for orden, c in enumerate(CURSOS, 1):
        mods, evals = [], {}
        horas_obl = sum(M[x]["horas"] for x in c["obligatorios"])
        horas_opt = c["elige"] * 9
        for tipo, ids in (("obligatorio", c["obligatorios"]), ("optativo", c["optativos"])):
            for k, mid in enumerate(ids, 1):
                m = M[mid]
                if tipo == "obligatorio":
                    req = c.get("requiere", {}).get(mid, [c["obligatorios"][k - 2]] if k > 1 and "requiere" not in c else [])
                else:
                    req = []
                mods.append({"id": mid, "numero": k, "titulo": m["titulo"], "tipo": tipo,
                             "etiqueta": f"Módulo {k}" if tipo == "obligatorio" else "Optativo",
                             "duracion": f"6 sesiones · {horas_txt(m['horas'])}", "constancia": True, "requiere": req,
                             "intro": m.get("intro", ""), "clases": m["clases"]})
                evals.update(m["evals"])
        ficha = {"id": c["id"], "titulo": c["titulo"], "subtitulo": c["subtitulo"], "descripcion": c["descripcion"],
                 "duracion": f"{horas_txt(horas_obl + horas_opt)} · {len(c['obligatorios'])} módulos obligatorios y {c['elige']} optativo{'s' if c['elige'] > 1 else ''}",
                 "modalidad": c.get("modalidad", "En línea, a tu ritmo"), "publico": c["publico"], "tipo": "curso", "orden": orden,
                 "elige": c["elige"], "horas": horas_obl + horas_opt, "recursos": {}}
        escribir(c["id"], ficha, mods, evals)
        lista.append(c["id"])
    for mid in COMPLEMENTARIAS:
        m = M[mid]
        ficha = {"id": mid, "titulo": m["titulo"], **m["ficha"], "categoria": m["categoria"],
                 "duracion": "6 sesiones · 9 horas", "modalidad": "En línea, a tu ritmo", "tipo": "complementaria", "horas": 9, "recursos": {}}
        mods = [{"id": mid, "numero": 1, "titulo": m["titulo"], "tipo": "obligatorio", "etiqueta": "Módulo",
                 "duracion": "6 sesiones · 9 horas", "constancia": False, "requiere": [], "intro": m["intro"], "clases": m["clases"]}]
        escribir(mid, ficha, mods, m["evals"])
        lista.append(mid)
    sitio["cursos"] = lista
    (DATOS / "sitio.json").write_text(json.dumps(sitio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(M)} módulos, {len(CURSOS)} cursos y {len(COMPLEMENTARIAS)} módulos sueltos")


def escribir(cid, ficha, mods, evals):
    (DATOS / f"curso-{cid}.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATOS / f"indice-{cid}.json").write_text(json.dumps({"curso": cid, "modulos": mods}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (DATOS / f"evaluaciones-{cid}.json").write_text(json.dumps(evals, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
