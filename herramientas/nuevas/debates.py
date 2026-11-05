"""Pregunta de debate específica para cada sesión, tomada de su propio contenido.

Orden de preferencia:
  1. «Un caso para pensar»: el caso y sus preguntas.
  2. «Ejemplo» del apunte (diplomado de liderazgo): el ejemplo y qué harías tú.
  3. «Preguntas de estudio» (diplomado en Sagrada Escritura): las dos primeras.
  4. Si no hay nada de eso (cierres), una pregunta con el título de la sesión.
"""
import re

CIERRA = "Comparte tu respuesta y luego comenta el aporte de algún compañero."


def _limpio(t):
    t = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def _seccion(md, cabecera):
    m = re.search(r"^#{3,4} " + cabecera + r".*?$\n(.*?)(?=^#{2,4} |\Z)", md, re.M | re.S)
    return m


def debate_de(md, titulo_sesion):
    m = _seccion(md, r"Un caso para pensar")
    if m:
        nombre = re.match(r"^#{3,4} Un caso para pensar:?\s*(.*)$", m.group(0).splitlines()[0]).group(1).strip()
        cuerpo = m.group(1)
        parrafos = [_limpio(p) for p in re.split(r"\n\s*\n", cuerpo) if p.strip() and not p.strip().startswith(("-", "*", "1."))]
        preguntas = [_limpio(x) for x in re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", cuerpo, re.M)]
        if parrafos and preguntas:
            return {"titulo": "Caso: " + nombre if nombre else "Un caso para pensar", "caso": " ".join(parrafos), "preguntas": preguntas}
    m = re.search(r"^\*\*Ejemplo\.\*\*\s*(.+?)$", md, re.M)
    if m:
        return {"titulo": "Un caso para pensar", "caso": _limpio(m.group(1)),
                "preguntas": ["¿Qué aprendes de este ejemplo para tu propio servicio?", "¿Has visto algo parecido en tu grupo? ¿Cómo se vivió?"]}
    m = re.search(r"^\*\*Comunidad ficticia sugerida:\*\*\s*(.+?)$", md, re.M)
    if m:
        return {"titulo": "Una comunidad para analizar", "caso": (lambda t: t[:1].upper() + t[1:])(_limpio(m.group(1)).rstrip(".")) + ".",
                "preguntas": ["Si coordinaras este grupo, ¿cuál sería el principal problema y qué decidirías?", "¿Qué criterio pesó más en tu decisión y por qué?"]}
    m = _seccion(md, r"Preguntas de estudio")
    if m:
        preguntas = [_limpio(x) for x in re.findall(r"^\s*\d+\.\s+(.+)$", m.group(1), re.M)][:2]
        if preguntas:
            return {"titulo": "Preguntas de estudio", "caso": "", "preguntas": preguntas}
    return {"titulo": "", "caso": "",
            "preguntas": [f"De lo trabajado en «{titulo_sesion}», ¿qué te llevas para tu servicio y qué paso concreto vas a dar?"]}


def texto_debate(d):
    """Markdown que se muestra (y el relator puede editar) en el debate de la sesión."""
    partes = []
    if d.get("caso"):
        partes.append(f"**{d['titulo']}.** {d['caso']}")
    partes.append("\n".join("- " + q for q in d["preguntas"]))
    partes.append(CIERRA)
    return "\n\n".join(partes)


def debate_md(md, titulo_sesion):
    return texto_debate(debate_de(md, titulo_sesion))
