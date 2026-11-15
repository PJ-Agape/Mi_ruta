"""Piezas comunes del programa «Comunicación digital para la Pastoral» (tres niveles)."""

CV = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20190325_christus-vivit.html"
PRESENCIA = "https://www.vatican.va/roman_curia/dpc/documents/20230528_dpc-verso-piena-presenza_es.html"
LEON_2026 = "https://www.vatican.va/content/leo-xiv/es/messages/communications.html"
INTER_MIRIFICA = "https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/vat-ii_decree_19631204_inter-mirifica_sp.html"
ISE = "https://www.iglesia.cl/prevenirabusos/documentos/ise.pdf"
LEY_DATOS = "https://www.bcn.cl/balance-legislativo/detalle/ficha_LEY_21719_2024-12-13"
META_SUITE = "https://www.facebook.com/business/tools/meta-business-suite"
TIKTOK_PROG = "https://ads.tiktok.com/business/es-LA/blog/introducing-video-scheduler-now-you-can-plan-tiktoks-in-advance"
YT_AYUDA = "https://support.google.com/youtube"
WA_COMUNIDADES = "https://www.whatsapp.com/communities/learning?lang=es_LA"
CANVA = "https://www.canva.com"
CANVA_ONG = "https://www.canva.com/canva-for-nonprofits/eligibility-guidelines/"
BUFFER = "https://buffer.com/pricing"
METRICOOL = "https://metricool.com/es/premium/"

C_CV = ("Christus vivit 86-90", CV,
        "El ambiente digital es un lugar donde los jóvenes viven, se informan y se relacionan; ofrece grandes oportunidades y también riesgos de soledad, manipulación y violencia.")
C_PRESENCIA = ("Hacia una plena presencia (Dicasterio para la Comunicación, 2023)", PRESENCIA,
               "Reflexión pastoral sobre las redes sociales que, a partir de la parábola del buen samaritano, invita a ser prójimos también en lo digital, a ser reflexivos y no reactivos, y a preguntarnos si buscamos seguidores para nosotros o para Cristo.")
C_LEON = ("León XIV, Mensaje para la LX Jornada Mundial de las Comunicaciones Sociales (2026)", LEON_2026,
          "«Custodiar voces y rostros humanos»: advierte que los algoritmos premian las emociones rápidas y castigan la reflexión, alerta sobre los riesgos de la inteligencia artificial y pide no renunciar al propio pensamiento.")
C_INTER = ("Inter mirifica (Concilio Vaticano II, 1963)", INTER_MIRIFICA,
           "El Concilio reconoce los medios de comunicación como dones de Dios que deben usarse según la verdad y para el bien de las personas.")
C_ISE = ("Integridad en el Servicio Eclesial (Conferencia Episcopal de Chile)", ISE,
         "Normas de conducta para quienes sirven en la Iglesia, incluidas las comunicaciones con niños, niñas y adolescentes, que deben ser transparentes y por canales institucionales.")

AVISO_PLATAFORMAS = ("*Las plataformas cambian sus funciones, nombres de menú y límites con frecuencia. Los datos de esta sesión están revisados "
                     "a noviembre de 2026: si algo no aparece donde se indica, busca la opción con un nombre parecido o revisa la ayuda oficial.*")


def u(title, objective, intro, comenzar, logros, sections, caso, claves, bible, lectio, church, questions, activity, practica, prayer, idea, profundizar, resources):
    return {"title": title, "objective": objective, "intro": intro, "comenzar": comenzar, "logros": logros,
            "sections": [{"title": t, "body": b} for t, b in sections],
            "caso": {"titulo": caso[0], "texto": caso[1], "preguntas": caso[2]},
            "claves": claves, "bible": {"ref": bible[0], "comment": bible[1]},
            "lectio": {"meditar": lectio[0], "orar": lectio[1], "vivir": lectio[2]},
            "church": [{"source": s, "url": url, "text": t} for s, url, t in church],
            "questions": questions, "activity": activity, "practica": practica, "prayer": prayer, "idea": idea,
            "profundizar": {"titulo": profundizar[0], "texto": profundizar[1]},
            "resources": [{"title": t, "url": url, "note": n} for t, url, n in resources]}


def q(pregunta, opciones, correcta, explicacion):
    return {"q": pregunta, "options": opciones, "correct": correcta, "feedback": explicacion}


def taller(pasos, ejemplo, problemas, desafio, aviso=False):
    p = ["### Taller guiado", "Toma tu teléfono o tu computador y sigue los pasos con las cuentas reales de tu grupo (o con una cuenta de práctica)."]
    p.append("#### Paso a paso\n\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(pasos, 1)))
    if ejemplo:
        p.append(f"#### {ejemplo[0]}\n\n{ejemplo[1]}")
    p.append("#### Problemas frecuentes\n\n" + "\n".join(f"- **{a}** {b}" for a, b in problemas))
    p.append(f"#### Desafío\n\n{desafio}")
    if aviso:
        p.append(AVISO_PLATAFORMAS)
    return "\n\n".join(p)
