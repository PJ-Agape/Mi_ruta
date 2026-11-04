import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "herramientas" / "nuevas"))
import lote_a, lote_b
todas = {**lote_a.UNIDADES, **lote_b.UNIDADES}
for cid, (pos, unidad, preguntas) in todas.items():
    f = R / "fuentes" / "complementarias" / f"{cid}.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    titulos = [u["title"] for u in d["unidades"]]
    if unidad["title"] in titulos:
        print("ya está", cid); continue
    assert len(d["unidades"]) == 4, cid
    claves_ref = set(d["unidades"][0].keys())
    falta = claves_ref - set(unidad.keys())
    assert not falta, (cid, falta)
    d["unidades"].insert(pos, unidad)
    d["evaluacion"].extend(preguntas)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(cid, "→ unidad", pos + 1, "de", len(d["unidades"]), "·", len(d["evaluacion"]), "preguntas")
print(len(todas), "cursos")
