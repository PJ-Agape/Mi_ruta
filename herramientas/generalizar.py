"""Quita de las formaciones las referencias a una comunidad concreta.

Las formaciones de origen se escribieron para un grupo determinado: nombran al
grupo, su aplicación, sus reuniones y su diócesis. En el aula deben servir a
cualquier grupo de pastoral juvenil, así que cada referencia se reescribe según
su contexto. El orden importa: primero las frases completas y al final los
reemplazos de respaldo.

generalizar(texto) devuelve el texto limpio y falla si queda algún rastro.
"""
import re

REEMPLAZOS = [
    # El Arte de Encontrarnos
    ("Comprender la identidad del dirigente de Ágape como", "Comprender la identidad del dirigente de pastoral juvenil como"),
    ("qué es un dirigente de Ágape y qué no es", "qué es un dirigente de pastoral juvenil y qué no es"),
    ("Tu servicio en Ágape", "Tu servicio en el grupo"),
    ("jóvenes que llegan a Ágape", "jóvenes que llegan al grupo"),
    ("Un grupo de Ágape no se define", "Un grupo juvenil no se define"),
    ("comprendiendo los roles de Ágape", "comprendiendo los roles del equipo"),
    ("Conocer los roles de Ágape y su sentido.", "Conocer los roles del equipo y su sentido."),
    ("cómo se organiza Ágape y", "cómo se organiza un equipo pastoral y"),
    ("#### Los roles en Ágape", "#### Los roles en el equipo"),
    ("Para que el caminar juntos sea posible, Ágape se organiza con roles claros. Revisa la **Guía de servicio** en la sección Comunidad para conocer los detalles:",
     "Para que el caminar juntos sea posible, el equipo necesita roles claros. Cada grupo los nombra a su manera; esta es una organización frecuente (revisa cómo funciona en el tuyo):"),
    ("Los espacios de reunión (mensual, quincenal y semanal) existen", "Las reuniones periódicas del equipo existen"),
    ("en el equipo de Ágape,", "en el equipo,"),
    ("el método que usamos en Ágape, heredero", "un método muy usado en la pastoral juvenil, heredero"),
    ("En Ágape lo aplicamos en cuatro pasos sencillos:", "Se puede aplicar en cuatro pasos sencillos:"),
    ("Las reuniones quincenales de Ágape existen", "Las reuniones de equipo existen"),
    ("El método que usa Ágape tiene", "Este método tiene"),
    ("En Ágape lo decimos con palabras más cercanas a los jóvenes:", "Con palabras más cercanas a los jóvenes, se puede decir así:"),
    ("«Me salgo de Ágape, esto no es para mí»", "«Me salgo del grupo, esto no es para mí»"),
    ("y cómo vivirlas en Ágape.", "y cómo vivirlas en tu grupo."),
    ("como dirigente de Ágape.", "como dirigente."),
    ("En Ágape hay dirigentes desde muy jóvenes.", "En muchos grupos hay dirigentes desde muy jóvenes."),
    ("en Ágape y en toda la Iglesia en Chile,", "en la pastoral juvenil y en toda la Iglesia en Chile,"),
    ("En Ágape no se hacen:", "En un grupo pastoral no se hacen:"),
    ("que en Ágape hay lugar para todos", "que en el grupo hay lugar para todos"),
    ("En Ágape, la estructura de roles, las duplas de coordinación y las reuniones periódicas",
     "En un grupo pastoral, la estructura de roles, la coordinación compartida y las reuniones periódicas"),
    ("Todo lo que vivimos en Ágape nace", "Todo lo que vivimos en la pastoral juvenil nace"),
    ("La Capilla de la app tiene una guía «Ante el Santísimo» que puede servir para una primera visita personal.",
     "Un subsidio sencillo de adoración, que puedes pedir en tu parroquia o a un asesor, sirve para una primera visita personal."),
    ("- **La guía «Un rato con Jesús»** de la Capilla de la app, en casa o ante el Santísimo.",
     "- **Un rato con Jesús**, en casa o ante el Santísimo, con un subsidio sencillo de oración."),
    # Evaluaciones de El Arte de Encontrarnos
    ("un encuentro de Ágape", "un encuentro juvenil"),
    ("método formativo de Ágape", "método formativo que propone el curso"),
    ("en un grupo de Ágape", "en un grupo juvenil"),
    ("del dirigente Ágape", "del dirigente"),
    # Coordinar es servir
    ("Esta es la regla de oro de la coordinación en Ágape.", "Esta es la regla de oro de la coordinación."),
    ("En Ágape la coordinación es una dupla. No es casualidad:", "Conviene que la coordinación sea una dupla. No es casualidad:"),
    ("el año pastoral de Ágape a partir", "el año pastoral del grupo a partir"),
    ("cómo se arma el año de Ágape", "cómo se arma el año pastoral"),
    ("El año de Ágape va de marzo a la solemnidad de Cristo Rey, con unos 34 encuentros que siguen",
     "En Chile, el año pastoral suele ir de marzo a la solemnidad de Cristo Rey, con encuentros semanales que siguen"),
    ("- Las reuniones del equipo: la mensual con asesores y la quincenal.",
     "- Las reuniones del equipo: por ejemplo, una mensual con asesores y otra de programación."),
    ("En la app, ese calendario vive en la Agenda: la coordinación lo carga y todos lo ven.",
     "Ese calendario debe estar a la vista de todos en una agenda compartida (en papel, en el teléfono o en una aplicación): la coordinación lo carga y todos lo ven."),
    ("a Agenda de la app", "a agenda compartida del grupo"),
    ("En la app, la Agenda reúne las fechas: compártela con ellos.", "Comparte con ellos la agenda del grupo, con todas las fechas."),
    ("la evaluación del año en la Agenda.", "la evaluación del año en la agenda del grupo."),
    ("(en Ágape, normalmente un asesor)", "(normalmente un asesor)"),
    ("Ágape es parte de la parroquia, no un grupo aparte.", "El grupo es parte de la parroquia, no algo aparte."),
    ("hacer de Ágape un lugar seguro", "hacer del grupo un lugar seguro"),
    ("hagan de Ágape un lugar sano", "hagan del grupo un lugar sano"),
    ("más tiempo en Ágape", "más tiempo en el grupo"),
    ("(mensual y quincenal)", "(de asesores y de programación)"),
    ("#### Las dos reuniones del equipo", "#### Dos reuniones con propósitos distintos"),
    ("- **Reunión quincenal** (coordinadores, animadores y dirigentes):",
     "- **Reunión de programación** (coordinadores, animadores y dirigentes; por ejemplo, cada quince días):"),
    ("tratar en la quincenal temas", "tratar en la de programación temas"),
    ("Una estructura que funciona para la quincenal:", "Una estructura que funciona para la reunión de programación:"),
    ("En la Diócesis de San Bartolomé de Chillán, las denuncias se reciben en la Oficina de Recepción de Denuncias (escucharchillan@gmail.com) o en el Obispado (Av. Libertad 640, Chillán). Confirma que estos datos sigan vigentes.",
     "Cada diócesis tiene una oficina o un encargado que recibe las denuncias. Pregunta a tu párroco cuál es el contacto en tu diócesis, anótalo en el protocolo del grupo y confirma cada año que siga vigente."),
    ("- [Diócesis de Chillán: Recepción de Denuncias](https://diocesisdechillan.cl/recepcion-de-denuncias/): Contacto de la oficina diocesana.\n", ""),
    ("En la quincenal, con todo el equipo.", "En la de programación, con todo el equipo."),
    # Camino de Discernimiento y Oración
    ("en aplicaciones católicas, en la página de tu diócesis o en la sección de Evangelio de agAPPe.",
     "en aplicaciones católicas o en la página de tu diócesis."),
    # Respaldo
    ("la Pastoral Juvenil Ágape", "la pastoral juvenil"),
    ("Pastoral Juvenil Ágape", "pastoral juvenil"),
    ("dirigente de Ágape", "dirigente de pastoral juvenil"),
    ("reuniones quincenales", "reuniones de equipo"),
    ("reunión quincenal", "reunión de equipo"),
    ("Reunión quincenal", "Reunión de equipo"),
]

RASTROS = re.compile(r"Ágape|Agape|AGAPE|agAPPe|quincenal|Chillán|de la app\b|la Agenda\b")


def generalizar(texto, origen=""):
    for viejo, nuevo in REEMPLAZOS:
        texto = texto.replace(viejo, nuevo)
    resto = RASTROS.search(texto)
    if resto:
        i = resto.start()
        raise ValueError(f"Queda una referencia a la comunidad de origen en {origen}: …{texto[max(0, i - 60):i + 60]}…")
    return texto
