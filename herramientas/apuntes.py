"""Genera los apuntes de clase en PDF a partir de fuentes/apuntes/<modulo>/sN.md.

Cada apunte profundiza una sesión sin suponer conocimientos previos. El PDF queda en apuntes/<modulo>-sN.pdf
y malla.py lo enlaza en la sesión correspondiente.

Uso (desde la raíz del repositorio; necesita `markdown` de Python y Playwright de Node):
    python3 herramientas/apuntes.py            # todos
    python3 herramientas/apuntes.py ise-1      # solo un módulo
    python3 herramientas/malla.py
"""
import html
import json
import os
import pathlib
import subprocess
import sys
import tempfile

import markdown

R = pathlib.Path(__file__).resolve().parents[1]
FUENTES = R / "fuentes" / "apuntes"
SALIDA = R / "apuntes"
F = (R / "assets" / "fuentes").as_uri()

CSS = """
@font-face { font-family: "Fraunces"; src: url("%(F)s/fraunces-latin-wght-normal.woff2") format("woff2"); font-weight: 100 900; }
@font-face { font-family: "Fraunces"; src: url("%(F)s/fraunces-latin-wght-italic.woff2") format("woff2"); font-weight: 100 900; font-style: italic; }
@font-face { font-family: "Jakarta"; src: url("%(F)s/plus-jakarta-sans-latin-wght-normal.woff2") format("woff2"); font-weight: 200 800; }
@page { size: Letter; margin: 22mm 20mm 20mm 20mm; }
* { box-sizing: border-box; }
html { font-size: 10.6pt; }
body { margin: 0; font-family: "Jakarta", Arial, sans-serif; color: #1d2433; line-height: 1.55; }
.portada { border-bottom: 3px solid #0b2566; padding-bottom: 12pt; margin-bottom: 16pt; }
.portada .marca { display: flex; justify-content: space-between; align-items: baseline; font-size: 9pt; color: #4a5a80; letter-spacing: .04em; text-transform: uppercase; }
.portada .marca b { color: #ef591c; }
.portada .curso { margin: 14pt 0 2pt; font-size: 10pt; color: #1351a4; font-weight: 600; }
.portada h1 { margin: 0; font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: 22pt; line-height: 1.15; color: #0b2566; }
.portada .sesion { margin: 6pt 0 0; font-size: 10pt; color: #4a5a80; }
h2 { font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: 15pt; color: #0b2566; margin: 20pt 0 6pt; padding-bottom: 3pt; border-bottom: 1px solid #d9dfec; break-after: avoid; }
h3 { font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: 12pt; color: #1351a4; margin: 14pt 0 4pt; break-after: avoid; }
p { margin: 0 0 7pt; text-align: left; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 8pt; padding-left: 16pt; }
li { margin: 2pt 0; }
strong { color: #0b2566; }
table { width: 100%%; border-collapse: collapse; margin: 6pt 0 10pt; font-size: 9.4pt; break-inside: auto; }
th { background: #e3ecf8; color: #0b2566; text-align: left; font-weight: 700; }
th, td { border: 1px solid #c9d3e6; padding: 4pt 6pt; vertical-align: top; }
tr { break-inside: avoid; }
h2:first-of-type + ul { background: #fff6e5; border-left: 3px solid #ef591c; padding: 8pt 10pt 8pt 24pt; }
a { color: #1351a4; text-decoration: none; }
""" % {"F": F}

PIE = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5pt;color:#6b7896;padding:0 20mm;display:flex;justify-content:space-between">'
       '<span>Mi Ruta · Apunte de clase · __TITULO__</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

RENDER = """
const { chromium } = require('playwright');
(async () => {
  const trabajos = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage();
  for (const t of trabajos) {
    await p.goto('file://' + t.html); await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: t.pdf, format: 'Letter', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: t.pie,
                  margin: { top: '22mm', bottom: '20mm', left: '20mm', right: '20mm' } });
    console.log('ok', t.pdf.split('/').pop());
  }
  await b.close();
})();
"""


def leer(ruta):
    texto = ruta.read_text(encoding="utf-8")
    meta = {}
    if texto.startswith("---"):
        _, cab, texto = texto.split("---", 2)
        for linea in cab.strip().splitlines():
            k, v = linea.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, texto.strip()


def pagina(meta, cuerpo):
    e = html.escape
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{e(meta["titulo"])}</title><style>{CSS}</style></head><body>'
            f'<header class="portada"><div class="marca"><span><b>Mi Ruta</b> · Apunte de clase</span><span>Material de profundización</span></div>'
            f'<p class="curso">{e(meta["curso"])} · {e(meta["modulo"])}</p><h1>{e(meta["titulo"])}</h1><p class="sesion">{e(meta["sesion"])}</p></header>'
            + markdown.markdown(cuerpo, extensions=["tables", "sane_lists"]) + "</body></html>")


def generar(solo=None):
    SALIDA.mkdir(exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    trabajos = []
    for ruta in sorted(FUENTES.glob("*/s*.md")):
        mid = ruta.parent.name
        if solo and mid not in solo:
            continue
        meta, cuerpo = leer(ruta)
        h = tmp / f"{mid}-{ruta.stem}.html"
        h.write_text(pagina(meta, cuerpo), encoding="utf-8")
        trabajos.append({"html": str(h), "pdf": str(SALIDA / f"{mid}-{ruta.stem}.pdf"), "pie": PIE.replace("__TITULO__", html.escape(meta["titulo"]))})
    (tmp / "trabajos.json").write_text(json.dumps(trabajos), encoding="utf-8")
    (tmp / "render.js").write_text(RENDER, encoding="utf-8")
    subprocess.run(["node", str(tmp / "render.js"), str(tmp / "trabajos.json")], check=True,
                   env={**os.environ, "NODE_PATH": os.environ.get("NODE_PATH", "/opt/npm-tools/node_modules")})


if __name__ == "__main__":
    generar(set(sys.argv[1:]) or None)
