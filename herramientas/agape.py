"""Convierte las formaciones de agAPPe al formato del aula, con el material ampliado.

Uso (desde la raíz del repositorio):
    python3 herramientas/agape.py ruta/a/contenido.json

Lee el contenido original de agAPPe (data/contenido.json) y, para cada curso
transformado, los archivos de ampliación en fuentes/agape/<curso>/m<N>.json.
Genera:
  - contenido/<curso>/<id>.md            una unidad por archivo
  - datos/indice-<curso>.json            módulos, unidades y evaluaciones
  - datos/evaluaciones-<curso>.json      preguntas de cada evaluación
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "fuentes" / "agape"

CURSOS = {
    # id en agAPPe -> id en el aula
    "curso-dirigentes-agape": "arte-de-encontrarnos",
    "formacion-coordinadores": "coordinar-es-servir",
    "discernimiento-espiritual": "discernimiento-y-oracion",
}


def md(texto):
    """Pasa el HTML simple de agAPPe a markdown."""
    t = texto or ""
    t = re.sub(r"<strong>(.*?)</strong>", r"**\1**", t, flags=re.S)
    t = re.sub(r"<em>(.*?)</em>", r"*\1*", t, flags=re.S)
    t = re.sub(r"<br\s*/?>", "  \n", t)
    return re.sub(r"<[^>]+>", "", t).strip()


def lista(items, numerada=False):
    return "\n".join((f"{i}. " if numerada else "- ") + md(x) for i, x in enumerate(items, 1))


def unidad_md(u, ex):
    """Arma el markdown de una unidad de 90 minutos."""
    p = []
    p.append(f"**Objetivo:** {md(u['objective'])}")
    if ex.get("logros"):
        p.append("**Al terminar esta unidad podrás:**\n\n" + lista(ex["logros"]))
    p.append("**Tiempo estimado:** 90 minutos, en cinco momentos: para comenzar (10 min), aprender (35 min), "
             "Palabra e Iglesia (15 min), cuaderno y práctica (25 min) y oración (5 min).")

    # Para comenzar
    p.append("### Para comenzar (10 min)\n\n" + md(ex["comenzar"]))

    # Aprender
    a = [md(u["intro"])]
    for s in u["sections"]:
        a.append(f"#### {md(s['title'])}\n\n{md(s['body'])}")
    if ex.get("profundizar"):
        a.append(f"#### {ex['profundizar']['titulo']}\n\n{md(ex['profundizar']['texto'])}")
    if ex.get("caso"):
        c = ex["caso"]
        a.append(f"#### Un caso para pensar: {c['titulo']}\n\n{md(c['texto'])}\n\n" + lista(c["preguntas"]))
    if ex.get("claves"):
        a.append("#### Palabras clave\n\n" + "\n".join(f"- **{t}:** {d}" for t, d in ex["claves"]))
    p.append("### Aprender (35 min)\n\n" + "\n\n".join(a))

    # Palabra e Iglesia
    b = u.get("bible") or {}
    pal = [f"#### Palabra de Dios: {md(b.get('ref', ''))}", md(b.get("comment", ""))]
    lec = ex.get("lectio")
    if lec:
        pal.append("**Lectura orante en cuatro pasos:**\n\n" + "\n".join([
            f"1. **Leer:** busca {md(b.get('ref', '').split('·')[0].strip())} en tu Biblia y léelo dos veces, despacio. Subraya la palabra o frase que más te llame la atención.",
            f"2. **Meditar:** {md(lec['meditar'])}",
            f"3. **Orar:** {md(lec['orar'])}",
            f"4. **Vivir:** {md(lec['vivir'])}",
        ]))
    iglesia = u.get("church") or []
    if iglesia:
        items = []
        for c in iglesia:
            fuente = f"[{md(c['source'])}]({c['url']})" if c.get("url") else md(c["source"])
            items.append(f"- **{fuente}.** {md(c['text'])}")
        pal.append("#### La Iglesia nos enseña\n\n" + "\n".join(items))
    p.append("### Palabra e Iglesia (15 min)\n\n" + "\n\n".join(pal))

    # Cuaderno y práctica
    cp = ["#### Para tu cuaderno\n\nResponde por escrito. Nadie más lo va a leer: sé honesto contigo y con Dios.\n\n" +
          lista(u.get("questions") or [], numerada=True)]
    pasos = ex.get("practica") or []
    cp.append("#### Práctica con tu grupo\n\n" + md(u.get("activity", "")) +
              ("\n\n**Paso a paso:**\n\n" + "\n".join(f"- [ ] {md(x)}" for x in pasos) if pasos else ""))
    p.append("### Cuaderno y práctica (25 min)\n\n" + "\n\n".join(cp))

    # Orar
    o = [md(u.get("prayer", ""))]
    if ex.get("idea"):
        o.append(f"> **Para llevar:** {md(ex['idea'])}")
    rec = u.get("resources") or []
    if rec:
        o.append("#### Para profundizar\n\n" + "\n".join(
            f"- [{md(r['title'])}]({r['url']})" + (f": {md(r['note'])}" if r.get("note") else "") for r in rec))
    p.append("### Orar (5 min)\n\n" + "\n\n".join(o))
    return "\n\n".join(p) + "\n"


def main():
    origen = json.load(open(sys.argv[1], encoding="utf-8"))
    for curso in origen["courses"]:
        destino = CURSOS.get(curso["id"])
        if not destino:
            continue
        carpeta = RAIZ / "contenido" / destino
        carpeta.mkdir(parents=True, exist_ok=True)
        indice = {"curso": destino, "modulos": []}
        evaluaciones = {}
        for fase in curso["phases"]:
            n = fase["phaseNum"]
            archivo = FUENTES / destino / f"m{n}.json"
            extra = json.load(open(archivo, encoding="utf-8")) if archivo.exists() else {}
            unidades = list(fase["sessions"]) + extra.get("nuevas_unidades", [])
            clases = []
            for u in unidades:
                ex = extra.get("unidades", {}).get(u["id"])
                if not ex:
                    print(f"  falta ampliación de {destino} {u['id']}: se omite")
                    continue
                uid = "m{}-u{}".format(n, u["id"].split(".")[1].zfill(2))
                (carpeta / f"{uid}.md").write_text(unidad_md(u, ex), encoding="utf-8")
                clases.append({"id": uid, "tipo": "unidad", "numero": u["id"], "etiqueta": f"Unidad {u['id']}",
                               "titulo": md(u["title"]), "tiempo": "90 min"})
            preguntas = list((fase.get("quiz") or {}).get("questions", [])) + extra.get("evaluacion", [])
            if preguntas:
                eid = f"m{n}-eval"
                limpias = []
                for i, q in enumerate(preguntas, 1):
                    texto = re.sub(r"^\d+\.\s*", "", md(q["q"]))
                    limpias.append({"pregunta": texto, "opciones": [md(o) for o in q["options"]],
                                    "correcta": q["correct"], "explicacion": md(q.get("feedback", ""))})
                evaluaciones[eid] = {"titulo": md((fase.get("quiz") or {}).get("title") or f"Evaluación del módulo {n}"),
                                     "aprobacion": 70, "preguntas": limpias}
                clases.append({"id": eid, "tipo": "evaluacion", "etiqueta": "Evaluación",
                               "titulo": evaluaciones[eid]["titulo"], "tiempo": f"{len(limpias)} preguntas"})
            indice["modulos"].append({
                "id": f"m{n}", "numero": n, "titulo": md(extra.get("titulo") or fase["title"]),
                "semanas": "", "intro": md(extra.get("intro") or fase.get("intro", "")), "clases": clases,
            })
        (RAIZ / "datos" / f"indice-{destino}.json").write_text(
            json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (RAIZ / "datos" / f"evaluaciones-{destino}.json").write_text(
            json.dumps(evaluaciones, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        total = sum(1 for m in indice["modulos"] for c in m["clases"] if c["tipo"] == "unidad")
        print(f"{destino}: {total} unidades, {len(evaluaciones)} evaluaciones")


if __name__ == "__main__":
    main()
