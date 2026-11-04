"""Utilidades para escribir los módulos del Diplomado en Sagrada Escritura."""
DV = "https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19651118_dei-verbum_sp.html"
VD = "https://www.vatican.va/content/benedict-xvi/es/apost_exhortations/documents/hf_ben-xvi_exh_20100930_verbum-domini.html"
CEC = "https://www.vatican.va/archive/catechism_sp/index_sp.html"
EG = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20131124_evangelii-gaudium.html"
URLS = {"Dei Verbum": DV, "Verbum Domini": VD, "Catecismo": CEC, "Evangelii gaudium": EG}


def iglesia(fuente, texto):
    d = {"source": fuente, "text": texto}
    for k, u in URLS.items():
        if fuente.startswith(k):
            d["url"] = u
    return d


def unidad(titulo, objetivo, intro, secciones, biblia, iglesia_, preguntas, actividad, oracion, comenzar, logros,
           profundizar, caso, claves, lectio, practica, idea):
    rec = [{"title": i["source"], "url": i["url"], "note": "Documento citado en esta unidad."} for i in iglesia_ if "url" in i][:1]
    return {
        "title": titulo, "objective": objetivo, "intro": intro,
        "sections": [{"title": t, "body": b} for t, b in secciones],
        "bible": {"ref": biblia[0], "comment": biblia[1]}, "church": iglesia_,
        "questions": preguntas, "activity": actividad, "prayer": oracion, "resources": rec,
        "comenzar": comenzar, "logros": logros,
        "profundizar": {"titulo": profundizar[0], "texto": profundizar[1]},
        "caso": {"titulo": caso[0], "texto": caso[1], "preguntas": caso[2]},
        "claves": claves, "lectio": {"meditar": lectio[0], "orar": lectio[1], "vivir": lectio[2]},
        "practica": practica, "idea": idea,
    }


def pregunta(q, opciones, correcta, retro):
    return {"q": q, "options": opciones, "correct": correcta, "feedback": retro}


def modulo(id_, titulo, subtitulo, descripcion, intro, taller, unidades, evaluacion):
    assert len(unidades) == 5, id_
    return {"id": id_, "titulo": titulo, "subtitulo": subtitulo, "categoria": "Sagrada Escritura",
            "publico": "Desde 17 años; agentes de pastoral", "descripcion": descripcion, "modulo": titulo,
            "intro": intro, "taller": taller, "unidades": unidades, "evaluacion": evaluacion}
