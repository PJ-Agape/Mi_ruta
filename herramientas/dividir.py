"""Divide los documentos de cada módulo en una clase por archivo.

Uso (desde la raíz del repositorio):
    python3 herramientas/dividir.py

Lee fuentes/modulo1.md, fuentes/modulo2.md y fuentes/modulo3.md (exportados
desde los documentos del diplomado) y genera:
  - contenido/liderazgo/<id>.md   una clase por archivo
  - datos/indice-liderazgo.json   la lista de módulos y clases

No toca datos/curso-liderazgo.json, que es donde se configuran a mano las
fechas, los enlaces de videollamada, los videos y las presentaciones.
"""
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "fuentes"
SALIDA = RAIZ / "contenido" / "liderazgo"
INDICE = RAIZ / "datos" / "indice-liderazgo.json"

MODULOS = [
    {"n": 1, "titulo": "Cadena de valor del liderazgo y cuadro de mando", "semanas": "1 a 6"},
    {"n": 2, "titulo": "Preparación del líder", "semanas": "7 a 10"},
    {"n": 3, "titulo": "Cómo ganar siendo líder", "semanas": "11 a 15"},
]

# Semana del calendario en que se trabaja cada clase.
SEMANA = {
    "m1-c01": 1, "m1-c02": 1, "m1-c03": 2, "m1-c04": 2, "m1-c05": 3, "m1-c06": 3,
    "m1-c07": 4, "m1-c08": 4, "m1-c09": 5, "m1-c10": 5, "m1-c11": 6,
    "m2-c11": 7, "m2-c12": 7, "m2-c13": 8, "m2-c14": 8, "m2-c15": 9, "m2-c16": 9,
    "m2-s10": 10,
    "m3-c17": 11, "m3-c18": 11, "m3-c19": 12, "m3-c20": 13, "m3-c21": 13,
    "m3-s14": 14, "m3-s15": 15,
}

FORMULA = re.compile(r"```latex\n.*?```", re.S)
FORMULA_TEXTO = "> **Confianza = (Credibilidad + Confiabilidad + Cercanía) ÷ Interés propio**"


def dividir(texto):
    """Devuelve (intro, [(titulo_h2, cuerpo)]) separando por encabezados ##."""
    partes = re.split(r"^## (.+)$", texto, flags=re.M)
    intro = partes[0]
    secciones = [(partes[i].strip(), partes[i + 1].strip()) for i in range(1, len(partes), 2)]
    return intro, secciones


def limpiar_intro(intro):
    lineas = []
    for linea in intro.splitlines():
        if linea.startswith("# "):
            continue
        if re.match(r"^(\w{3} \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})", linea.strip()):
            continue  # línea de fecha y autor del documento
        lineas.append(linea)
    return "\n".join(lineas).strip()


def identificar(modulo, titulo):
    m = re.match(r"^(Clase|Clave|Semana) (\d+)\. (.+)$", titulo)
    if not m:
        return None
    tipo, numero, nombre = m.group(1), int(m.group(2)), m.group(3)
    letra = "s" if tipo == "Semana" else "c"
    return {
        "id": f"m{modulo}-{letra}{numero:02d}",
        "tipo": tipo,
        "numero": numero,
        "titulo": nombre,
        "etiqueta": f"{tipo} {numero}",
    }


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    indice = {"curso": "liderazgo", "modulos": []}
    for mod in MODULOS:
        texto = (FUENTES / f"modulo{mod['n']}.md").read_text(encoding="utf-8")
        texto = FORMULA.sub(FORMULA_TEXTO, texto)
        intro, secciones = dividir(texto)
        intro = limpiar_intro(intro).replace("Este documento desarrolla", "Este módulo reúne")
        clases = []
        for titulo, cuerpo in secciones:
            datos = identificar(mod["n"], titulo)
            if datos is None:
                # Secciones generales del módulo (por ejemplo, "Cómo usar este material").
                intro += f"\n\n### {titulo}\n\n{cuerpo}"
                continue
            datos["semana"] = SEMANA.get(datos["id"])
            (SALIDA / f"{datos['id']}.md").write_text(cuerpo + "\n", encoding="utf-8")
            clases.append(datos)
        indice["modulos"].append({
            "id": f"m{mod['n']}",
            "numero": mod["n"],
            "titulo": mod["titulo"],
            "semanas": mod["semanas"],
            "intro": intro.strip(),
            "clases": clases,
        })
    INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(m["clases"]) for m in indice["modulos"])
    print(f"{total} clases generadas en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
