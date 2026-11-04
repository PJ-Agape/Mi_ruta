"""Genera las formaciones complementarias de Mi Ruta.

Uso (desde la raíz del repositorio):
    python3 herramientas/complementarias.py

Lee cada archivo fuentes/complementarias/<curso>.json, que contiene la ficha del
curso, sus unidades completas y la evaluación, y genera:
  - datos/curso-<curso>.json             ficha del curso
  - contenido/<curso>/m1-uNN.md          una unidad por archivo
  - datos/indice-<curso>.json            módulo, unidades y evaluación
  - datos/evaluaciones-<curso>.json      preguntas de la evaluación

Las unidades usan el mismo formato de 90 minutos que las formaciones de la ruta
(ver unidad_md en formaciones.py).
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from formaciones import unidad_md, md  # noqa: E402
from generalizar import generalizar  # noqa: E402

FICHA = ("id", "titulo", "subtitulo", "descripcion", "categoria", "publico", "modalidad", "duracion")


def generar(archivo):
    c = json.loads(archivo.read_text(encoding="utf-8"))
    cid = c["id"]
    carpeta = RAIZ / "contenido" / cid
    carpeta.mkdir(parents=True, exist_ok=True)
    unidades = c["unidades"]

    ficha = {k: c[k] for k in FICHA if k in c}
    ficha.setdefault("modalidad", "En línea, a tu ritmo")
    ficha.setdefault("duracion", f"{len(unidades)} unidades de 90 min ({len(unidades) * 1.5:g} horas)".replace(".", ","))
    ficha["tipo"] = "complementaria"
    ficha["recursos"] = {}
    (RAIZ / "datos" / f"curso-{cid}.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    clases = []
    for i, u in enumerate(unidades, 1):
        uid = f"m1-u{i:02d}"
        (carpeta / uid).with_suffix(".md").write_text(generalizar(unidad_md(u, u), f"{cid}/{uid}"), encoding="utf-8")
        clases.append({"id": uid, "tipo": "unidad", "numero": f"1.{i}", "etiqueta": f"Unidad {i}",
                       "titulo": md(u["title"]), "tiempo": "90 min"})

    preguntas = [{"pregunta": md(q["q"]), "opciones": [md(o) for o in q["options"]],
                  "correcta": q["correct"], "explicacion": md(q.get("feedback", ""))} for q in c["evaluacion"]]
    evaluaciones = {"m1-eval": {"titulo": f"Evaluación: {c['titulo']}", "aprobacion": 70, "preguntas": preguntas}}
    clases.append({"id": "m1-eval", "tipo": "evaluacion", "etiqueta": "Evaluación",
                   "titulo": evaluaciones["m1-eval"]["titulo"], "tiempo": f"{len(preguntas)} preguntas"})

    indice = {"curso": cid, "modulos": [{"id": "m1", "numero": 1, "titulo": c.get("modulo", c["titulo"]),
                                         "semanas": "", "intro": c.get("intro", ""), "clases": clases}]}
    (RAIZ / "datos" / f"indice-{cid}.json").write_text(
        generalizar(json.dumps(indice, ensure_ascii=False, indent=1), cid) + "\n", encoding="utf-8")
    (RAIZ / "datos" / f"evaluaciones-{cid}.json").write_text(
        generalizar(json.dumps(evaluaciones, ensure_ascii=False, indent=1), cid) + "\n", encoding="utf-8")
    print(f"{cid}: {len(unidades)} unidades, {len(preguntas)} preguntas")


def main():
    for archivo in sorted((RAIZ / "fuentes" / "complementarias").glob("*.json")):
        generar(archivo)


if __name__ == "__main__":
    main()
