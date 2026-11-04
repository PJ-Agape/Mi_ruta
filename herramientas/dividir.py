"""Divide los documentos de cada módulo en una clase por archivo.

Uso (desde la raíz del repositorio):
    python3 herramientas/dividir.py

Lee fuentes/modulo1.md a fuentes/modulo6.md (exportados
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

# Cada módulo se puede cursar y certificar por separado. El proyecto integrador
# (módulo 7) solo lo hacen quienes cursan el diplomado completo.
MODULOS = [
    {"n": 1, "fuente": 1, "titulo": "Cadena de valor del liderazgo y cuadro de mando", "semanas": 6, "horas": 48},
    {"n": 2, "fuente": 2, "titulo": "Preparación del líder", "semanas": 4, "horas": 32},
    {"n": 3, "fuente": 3, "titulo": "Cómo ganar siendo líder", "semanas": 3, "horas": 24},
    {"n": 4, "fuente": 4, "titulo": "Comunicación y conflictos", "semanas": 4, "horas": 32},
    {"n": 5, "fuente": 5, "titulo": "Planificación y proyectos", "semanas": 4, "horas": 32},
    {"n": 6, "fuente": 6, "titulo": "Liderazgo que acompaña personas", "semanas": 4, "horas": 32},
    {"n": 7, "fuente": 3, "titulo": "Proyecto integrador y cierre del diplomado", "semanas": 2, "horas": 16,
     "constancia": False,
     "intro": "Esta etapa es solo para quienes cursan el diplomado completo. Reúne en un proyecto aplicado a la propia comunidad las herramientas de los seis módulos y termina con la presentación de los proyectos, la evaluación final y la ceremonia de cierre.\n\nPara recibir el certificado del diplomado se necesitan las constancias de los seis módulos y el proyecto integrador aprobado."},
]

ROMANOS = ["", "I", "II", "III", "IV", "V", "VI", "VII"]

# Semana del módulo en que se trabaja cada clase.
SEMANA = {
    "m1-c01": 1, "m1-c02": 1, "m1-c03": 2, "m1-c04": 2, "m1-c05": 3, "m1-c06": 3,
    "m1-c07": 4, "m1-c08": 4, "m1-c09": 5, "m1-c10": 5, "m1-c11": 6,
    "m2-c11": 1, "m2-c12": 1, "m2-c13": 2, "m2-c14": 2, "m2-c15": 3, "m2-c16": 3, "m2-s10": 4,
    "m3-c17": 1, "m3-c18": 1, "m3-c19": 2, "m3-c20": 3, "m3-c21": 3,
    "m7-s01": 1, "m7-s02": 2,
}
for _m in (4, 5, 6):
    for _c, _w in ((1, 1), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3)):
        SEMANA[f"m{_m}-c{_c:02d}"] = _w
    SEMANA[f"m{_m}-s04"] = 4

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
    for viejo in SALIDA.glob("m*-*.md"):
        viejo.unlink()
    indice = {"curso": "liderazgo", "modulos": []}
    for mod in MODULOS:
        texto = (FUENTES / f"modulo{mod['fuente']}.md").read_text(encoding="utf-8")
        texto = FORMULA.sub(FORMULA_TEXTO, texto)
        intro, secciones = dividir(texto)
        intro = limpiar_intro(intro).replace("Este documento desarrolla", "Este módulo reúne")
        clases = []
        for titulo, cuerpo in secciones:
            es_cierre = titulo.startswith("Semana") and mod["fuente"] == 3
            if (mod["n"] == 7) != es_cierre:
                if mod["n"] != 7 and identificar(mod["n"], titulo) is None:
                    intro += f"\n\n### {titulo}\n\n{cuerpo}"
                continue
            datos = identificar(mod["n"], titulo)
            if datos is None:
                continue
            if datos["tipo"] == "Semana" and mod["n"] != 7:
                datos["etiqueta"] = "Taller del módulo"
            datos["semana"] = SEMANA.get(datos["id"])
            (SALIDA / f"{datos['id']}.md").write_text(cuerpo + "\n", encoding="utf-8")
            clases.append(datos)
        constancia = mod.get("constancia", True)
        indice["modulos"].append({
            "id": f"m{mod['n']}",
            "numero": mod["n"],
            "titulo": mod["titulo"],
            "etiqueta": "Cierre" if mod["n"] == 7 else f"Módulo {ROMANOS[mod['n']]}",
            "semanas": "",
            "duracion": f"{mod['semanas']} semanas · {mod['horas']} horas",
            "constancia": constancia,
            "requiere": [] if mod["n"] == 1 else ["m1"],
            "intro": mod.get("intro", intro).strip(),
            "clases": clases,
        })
    INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(m["clases"]) for m in indice["modulos"])
    horas = sum(m["horas"] for m in MODULOS)
    print(f"{total} clases en {len(MODULOS)} etapas, {horas} horas, generadas en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
