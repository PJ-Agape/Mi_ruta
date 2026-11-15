"""Genera el programa «Comunicación digital para la Pastoral» en tres niveles:
comunicacion-y-redes (nivel 1), redes-2 (nivel 2) y redes-3 (nivel 3), con un taller guiado por sesión.

Uso (desde la raíz del repositorio):
    python3 herramientas/nuevas/comunicacion_digital.py
    python3 herramientas/malla.py
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "herramientas"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from cd_n1 import N1, E1, T1, TALLER1  # noqa: E402
from cd_n2 import N2, E2, T2, TALLER2  # noqa: E402
from cd_n3 import N3, E3, T3, TALLER3  # noqa: E402

NIVELES = [
    ("comunicacion-y-redes", "Comunicación y redes · Nivel 1: comunicar con sentido",
     "Propósito, plataformas, formatos, identidad y cuidado de las personas",
     "Para quienes manejan las redes, los grupos de mensajería o los afiches de su grupo: para qué comunica una comunidad cristiana, qué ofrece cada plataforma, qué formatos y medidas usar, cómo construir la identidad visual y el tono de voz, y cómo cuidar a las personas en lo digital.",
     "El primer nivel del programa Comunicación digital para la Pastoral. Cada sesión termina con un taller guiado sobre las cuentas reales de tu grupo.",
     N1, E1, T1),
    ("redes-2", "Comunicación y redes · Nivel 2: crear contenidos",
     "Textos, diseño con Canva, fotografía, video vertical y cobertura de eventos",
     "El nivel de producción: escribir textos con gancho y llamado a la acción, diseñar piezas claras en Canva, fotografiar y editar con el celular, grabar y editar video vertical con subtítulos y música permitida, y cubrir un evento de principio a fin.",
     "Con el nivel 1 aprobado. Aquí se aprende haciendo: cada sesión produce una pieza real para tu grupo.",
     N2, E2, T2),
    ("redes-3", "Comunicación y redes · Nivel 3: gestionar la comunicación",
     "Community manager, calendario editorial, programación, moderación, crisis y métricas",
     "El nivel de gestión: organizar el equipo y las cuentas, planificar con un calendario editorial basado en el año litúrgico, programar y automatizar con criterio, moderar la comunidad y responder a crisis, y medir para tomar decisiones pastorales.",
     "Con los niveles 1 y 2 aprobados. Para quienes coordinan la comunicación de su grupo o parroquia.",
     N3, E3, T3),
]

TALLER = {}
for cid, d in (("comunicacion-y-redes", TALLER1), ("redes-2", TALLER2), ("redes-3", TALLER3)):
    for n, texto in d.items():
        TALLER[(cid, n)] = texto
IDS = [n[0] for n in NIVELES]


def taller_md(cid, n):
    return TALLER.get((cid, n), "")


if __name__ == "__main__":
    import complementarias
    for cid, titulo, sub, desc, intro, unidades, evaluacion, taller in NIVELES:
        assert len(unidades) == 5 and len(evaluacion) == 10, cid
        assert all((cid, n) in TALLER for n in range(1, 6)), cid
        f = {"id": cid, "titulo": titulo, "subtitulo": sub, "categoria": "Herramientas", "publico": "Desde 14 años",
             "descripcion": desc, "modulo": titulo, "intro": intro, "unidades": unidades, "evaluacion": evaluacion, "taller": taller}
        destino = R / "fuentes" / "complementarias" / f"{cid}.json"
        destino.write_text(json.dumps(f, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        complementarias.generar(destino)
        print("ok", cid)
