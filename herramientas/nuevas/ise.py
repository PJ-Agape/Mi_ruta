"""Genera el curso «Profundización ISE» (Integridad en el Servicio Eclesial, CECh 2020) en tres partes:
ise-1, ise-2 e ise-3, con las veinte orientaciones del documento.

Uso (desde la raíz del repositorio):
    python3 herramientas/nuevas/ise.py
    python3 herramientas/malla.py
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "herramientas"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from ise_1 import P1, E_P1, T_P1  # noqa: E402
from ise_2 import P2, E_P2, T_P2  # noqa: E402
from ise_3 import P3, E_P3, T_P3  # noqa: E402

PUBLICO = "Desde 14 años; para todos los que tienen un servicio en la Iglesia"
PARTES = [
    ("ise-1", "Profundización ISE · Parte 1: testimonio, justicia y buen trato",
     "El documento y sus orientaciones 1 a 8",
     "Qué es el documento Integridad en el Servicio Eclesial, de dónde viene y a quién se dirige; y sus orientaciones sobre el testimonio, la justicia social y el trato justo, las relaciones laborales, la administración transparente de los bienes, las relaciones respetuosas y la valoración de la diversidad.",
     "Primera parte del curso. Ten el documento a mano: cada sesión estudia una o dos orientaciones, estándar por estándar, con casos de la vida pastoral.",
     P1, E_P1, T_P1),
    ("ise-2", "Profundización ISE · Parte 2: autoridad, poder y ambientes sanos",
     "Orientaciones 9 a 13 y estructuras de prevención",
     "La autoridad como servicio, la participación y la corrección fraterna; el desequilibrio de poder y el abuso de conciencia; las fronteras físicas y emocionales con niños, jóvenes y adultos vulnerables; los resguardos del acompañamiento; y la política y las estructuras de prevención de la Iglesia en Chile.",
     "Con la parte 1 aprobada. Es el corazón del documento: léela con calma y convérsala con tu equipo.",
     P2, E_P2, T_P2),
    ("ise-3", "Profundización ISE · Parte 3: responder, servir con calidad y cuidarse",
     "Orientaciones 14 a 20 y restablecimiento de la comunión",
     "Cómo responder a una denuncia o revelación; la atención preferente a las víctimas y el restablecimiento de la comunión; el servicio responsable, la confidencialidad y la formación permanente; la prudencia con regalos, ayudas y donaciones; los registros; y el cuidado de sí mismo.",
     "Con las partes 1 y 2 aprobadas. Termina con un compromiso personal y comunitario de integridad.",
     P3, E_P3, T_P3),
]
IDS = [p[0] for p in PARTES]

if __name__ == "__main__":
    import complementarias
    for cid, titulo, sub, desc, intro, unidades, evaluacion, taller in PARTES:
        assert len(unidades) == 5 and len(evaluacion) == 10, cid
        for e in evaluacion:
            assert 0 <= e["correct"] < len(e["options"]), (cid, e["q"])
        f = {"id": cid, "titulo": titulo, "subtitulo": sub, "categoria": "Cuidado", "publico": PUBLICO,
             "descripcion": desc, "modulo": titulo, "intro": intro, "unidades": unidades, "evaluacion": evaluacion, "taller": taller}
        destino = R / "fuentes" / "complementarias" / f"{cid}.json"
        destino.write_text(json.dumps(f, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        complementarias.generar(destino)
        print("ok", cid)
