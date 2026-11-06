"""Genera fuentes/complementarias/gestion-del-tiempo.json y su contenido.

Uso (desde la raíz del repositorio):
    python3 herramientas/nuevas/gestion_tiempo.py
    python3 herramientas/malla.py
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "herramientas"))

EG = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20131124_evangelii-gaudium.html"
CV = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20190325_christus-vivit.html"
LS = "https://www.vatican.va/content/francesco/es/encyclicals/documents/papa-francesco_20150524_enciclica-laudato-si.html"
GE = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20180319_gaudete-et-exsultate.html"


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


UNIDADES = [
    u("El tiempo del otro es un don",
      "Descubrir que el tiempo es un regalo de Dios y que respetar el tiempo de los demás es una forma concreta de caridad.",
      "Solemos pensar la gestión del tiempo como una técnica para rendir más. En la pastoral la mirada es otra: el tiempo es un don, y el tiempo de cada persona que viene a un encuentro, a una reunión o a una actividad es un regalo que nos confía. Llegar tarde, alargar sin aviso o hacer esperar no es un detalle: es disponer de algo que no es nuestro.",
      "Recuerda la última vez que esperaste a alguien más de veinte minutos sin aviso. ¿Qué sentiste? ¿Qué dejaste de hacer por esperar? Escríbelo en dos líneas.",
      ["Explicar por qué el tiempo es un don y no solo un recurso.", "Calcular el costo real de la impuntualidad en un grupo.", "Reconocer la puntualidad como una forma de caridad y de acogida."],
      [("Cronos y kairós",
        "Los griegos tenían dos palabras para el tiempo. **Cronos** es el tiempo del reloj, que se mide y se agota. **Kairós** es el tiempo oportuno, el momento de gracia en que algo importante puede suceder. La Biblia usa las dos.\n\n"
        "Gestionar bien el *cronos* (horarios, plazos, duraciones) no es frialdad: es lo que permite que haya espacio para el *kairós*, para el encuentro, la oración y la conversación profunda. Un encuentro que empieza cuarenta minutos tarde suele terminar apurado justo en la parte más importante."),
       ("El costo de llegar tarde",
        "La impuntualidad parece pequeña cuando se mira desde uno mismo, pero se multiplica por todas las personas que esperan.\n\n"
        "**Haz la cuenta:** si un encuentro de 30 personas empieza 20 minutos tarde, se perdieron **600 minutos**: diez horas de vida de la comunidad. Si pasa cada semana durante un año, son más de 500 horas.\n\n"
        "Además, la impuntualidad enseña: quienes llegaron a la hora aprenden que no vale la pena hacerlo, y la próxima vez llegarán más tarde. Así nace la famosa «hora chilena», que en realidad no es una costumbre inevitable, sino un acuerdo que nadie eligió."),
       ("La puntualidad como acogida",
        "Ser puntual no es rigidez: es decirle al otro **«me importas, tu tiempo vale»**. Para quien sirve en la pastoral, tiene un sentido especial:\n\n"
        "- **Llegar antes:** el dirigente llega antes que los jóvenes, prepara el lugar y recibe a cada uno por su nombre.\n"
        "- **Empezar a la hora:** se empieza con los que están, aunque sean pocos. Eso honra a quienes llegaron y educa a los demás.\n"
        "- **Terminar a la hora:** las familias organizan su día en torno a la hora de salida que les diste.\n"
        "- **Avisar siempre:** si vas a llegar tarde o no vas a poder ir, avisa apenas lo sepas, no cuando ya te están esperando."),
       ("El tiempo de los que no pueden reclamar",
        "Hay personas cuyo tiempo se suele atropellar porque no se quejan: el sacristán que espera para cerrar el templo, la señora que prepara la once, el chofer del bus, los papás que esperan afuera en el auto, los voluntarios que limpian después.\n\n"
        "Respetar el tiempo de los que sirven en silencio es una prueba de que entendimos el Evangelio. Una actividad pastoral no termina cuando se acaba la dinámica, sino cuando el último que ayudó puede irse a su casa.")],
      ("La hora chilena",
       "El encuentro del grupo juvenil está citado a las 17:00. Los dirigentes llegan a las 17:15 y empiezan a las 17:40, «porque nunca llega nadie a la hora». Tres jóvenes nuevos que llegaron puntuales esperaron casi una hora sentados en la escalera. Uno de ellos no volvió.",
       ["¿Qué mensaje recibieron los jóvenes que llegaron a la hora?", "¿Cómo podría el equipo romper este círculo desde el próximo sábado?"]),
      [["Cronos", "El tiempo del reloj, que se mide y se agota."], ["Kairós", "El tiempo oportuno, el momento de gracia en que algo importante puede suceder."], ["Puntualidad", "Llegar, empezar y terminar a la hora acordada; una forma de respeto y de acogida."]],
      ("Eclesiastés 3,1-8 · Todo tiene su tiempo",
       "El sabio enumera los tiempos de la vida: tiempo de nacer y de morir, de plantar y de cosechar, de callar y de hablar. Cada cosa tiene su momento bajo el cielo. Reconocer el momento oportuno es parte de la sabiduría."),
      ("¿Qué «tiempo» estás viviendo hoy en tu servicio? ¿Respetas el tiempo de los demás?", "Pide perdón por el tiempo que has hecho perder a otros y agradece a quienes te regalan el suyo.", "Esta semana, llega diez minutos antes a tu compromiso pastoral y recibe a cada persona por su nombre."),
      [("Evangelii gaudium 222-225", EG, "«El tiempo es superior al espacio»: Francisco invita a privilegiar los procesos que maduran con paciencia por sobre el afán de ocupar espacios y obtener resultados inmediatos."),
       ("Laudato si' 237", LS, "El domingo y el descanso recuerdan que el tiempo no es solo para producir: tiene una dimensión receptiva y gratuita que abre a la contemplación y al encuentro.")],
      ["¿Cuánto tiempo pierde tu grupo, cada mes, por empezar tarde?", "¿A quién de tu comunidad le has hecho esperar sin avisar?", "¿Qué personas sirven en silencio y suelen esperar a que terminen las actividades?", "¿Qué te cuesta más: llegar a la hora, empezar a la hora o terminar a la hora?"],
      "Calculen en grupo cuántas horas de vida se pierden al año en su comunidad por empezar tarde (minutos de atraso promedio × personas × encuentros al año). Luego escriban tres acuerdos concretos de puntualidad para el próximo mes y decidan cómo los van a comunicar a los jóvenes y las familias.",
      ["Estimen el atraso promedio de sus encuentros.", "Calculen las horas perdidas al año.", "Escriban tres acuerdos de puntualidad.", "Decidan cómo comunicarlos."],
      "Señor del tiempo, Tú nos regalas cada día como un don. Perdona las veces que hemos hecho esperar a otros y hemos dispuesto de su tiempo como si fuera nuestro. Enséñanos a llegar antes para acoger, a empezar con los que están y a terminar cuando prometimos, para que nuestra puntualidad también anuncie tu amor. Amén.",
      "El tiempo del otro no es mío: cuidarlo es una forma de amar.",
      ("La puntualidad educa",
       "Los jóvenes aprenden más de lo que ven que de lo que escuchan. Un equipo que empieza siempre a la hora, aunque haya pocos, forma en pocas semanas una comunidad puntual. Un equipo que espera a los atrasados, en cambio, enseña que llegar a la hora es perder el tiempo. Cambiar la cultura de un grupo toma tiempo, pero empieza con una decisión del equipo."),
      [("Evangelii gaudium (Francisco, 2013)", EG, "Números 222-225, «El tiempo es superior al espacio»."),
       ("Laudato si' (Francisco, 2015)", LS, "Número 237, sobre el descanso y el sentido del tiempo.")]),

    u("Ordenar mi tiempo para servir mejor",
      "Organizar el propio tiempo con prioridades claras, para servir sin descuidar el estudio, el trabajo, la familia, el descanso y la oración.",
      "Nadie puede respetar el tiempo de los demás si su propia agenda es un caos. Muchos dirigentes llegan tarde, olvidan compromisos o se agotan no por falta de voluntad, sino porque dicen que sí a todo y no tienen un orden. Esta sesión te ayuda a poner primero lo importante.",
      "Escribe todo lo que hiciste ayer, hora por hora, aproximadamente. Marca con un color lo que fue importante y con otro lo que solo fue urgente o simplemente se te fue.",
      ["Distinguir lo urgente de lo importante.", "Planificar la semana con bloques y prioridades.", "Aprender a decir que no con respeto y a tiempo."],
      [("Urgente e importante",
        "Una herramienta sencilla es dividir las tareas en cuatro grupos:\n\n"
        "| | Urgente | No urgente |\n|---|---|---|\n"
        "| **Importante** | **Hacer ya:** la prueba de mañana, el aviso del retiro de este sábado. | **Planificar:** preparar con tiempo el encuentro, estudiar, rezar, descansar, estar con la familia. |\n"
        "| **No importante** | **Delegar o simplificar:** muchos mensajes, algunas llamadas. | **Eliminar:** horas en redes sin darte cuenta. |\n\n"
        "El secreto está en el cuadro **importante y no urgente**: si le das tiempo, las urgencias disminuyen. Un encuentro preparado el martes no se convierte en una urgencia el sábado a las 16:00."),
       ("Primero las piedras grandes",
        "Imagina un frasco que hay que llenar con piedras grandes, piedrecillas y arena. Si pones primero la arena, las piedras grandes no caben. Si pones primero las piedras grandes, el resto se acomoda entre ellas.\n\n"
        "Las **piedras grandes** son lo que no puede faltar en tu semana: tu deber de estado (estudio o trabajo), tu familia, tu descanso, tu oración y tu servicio. Agéndalas **primero**, como bloques fijos en tu calendario. Después acomoda lo demás."),
       ("La semana en bloques",
        "Una vez a la semana, por ejemplo el domingo en la tarde, toma diez minutos para planificar:\n\n"
        "1. **Revisa** lo que viene: clases, trabajo, reuniones, encuentros, plazos.\n"
        "2. **Bloquea** las piedras grandes en tu calendario, incluido el tiempo para preparar tu servicio.\n"
        "3. **Considera los traslados:** si el encuentro es a las 17:00 y tardas 30 minutos en llegar, tu compromiso empieza a las 16:30.\n"
        "4. **Deja márgenes:** entre una actividad y otra, al menos 15 minutos libres. Las agendas sin margen son las que producen atrasos en cadena.\n"
        "5. **Revisa al final de la semana** qué funcionó y qué no."),
       ("Decir que no a tiempo",
        "Decir que sí a todo parece generosidad, pero termina en compromisos a medias, atrasos y cansancio. Quien no sabe decir que no, termina fallándole a alguien.\n\n"
        "- **Antes de aceptar,** revisa tu agenda: ¿tienes realmente el tiempo?\n"
        "- **Di que no a tiempo,** apenas sepas que no puedes, no el día anterior.\n"
        "- **Propón alternativas:** «este mes no puedo coordinar el retiro, pero puedo ayudar con las compras».\n"
        "- **Un no honesto** respeta más el tiempo del equipo que un sí que no se cumple.")],
      ("El dirigente que dice que sí a todo",
       "Tomás es dirigente, está en cuarto medio, juega fútbol y canta en el coro. Cuando le piden algo, siempre dice que sí. Este mes llegó tarde a tres encuentros, olvidó comprar los materiales del retiro y avisó a última hora que no podía ir a la reunión de equipo. Él siente que no le alcanza el tiempo; el equipo siente que no pueden contar con él.",
       ["¿Qué le está pasando a Tomás?", "¿Cómo podría ordenar sus prioridades sin dejar de servir?"]),
      [["Prioridad", "Lo que se pone primero porque es más importante, aunque no sea lo más urgente."], ["Bloque de tiempo", "Espacio reservado en la agenda para una actividad concreta."], ["Margen", "Tiempo libre entre actividades que absorbe imprevistos y evita atrasos en cadena."]],
      ("Lucas 10,38-42 · Marta y María",
       "Marta se afana sirviendo y se queja de que su hermana María, sentada a los pies de Jesús, no la ayuda. Jesús le dice que se inquieta por muchas cosas, pero que una sola es necesaria, y que María eligió la mejor parte. Servir mucho no reemplaza estar con el Señor."),
      ("¿Te pareces más a Marta o a María? ¿Qué te inquieta y agita?", "Presenta al Señor tu agenda de la semana y pregúntale qué es lo único necesario.", "Esta semana, bloquea en tu calendario un tiempo fijo de oración antes de cualquier otra cosa."),
      [("Laudato si' 225-226", LS, "La paz interior y la capacidad de vivir el momento presente sin la ansiedad de pasar a lo siguiente son parte de una espiritualidad sana.")],
      ["¿Qué tareas importantes y no urgentes estás postergando?", "¿Cuáles son las piedras grandes de tu semana?", "¿A qué deberías decir que no este mes?", "¿Cuánto margen dejas entre tus compromisos?"],
      "Cada participante planifica su próxima semana: primero bloquea sus piedras grandes (estudio o trabajo, familia, descanso, oración y servicio), luego agrega los demás compromisos con sus tiempos de traslado y márgenes. En parejas, revisen la agenda del otro: ¿es realista? ¿dónde se va a producir un atraso?",
      ["Lista tus piedras grandes.", "Bloquéalas en tu calendario.", "Agrega traslados y márgenes.", "Revisa tu agenda con un compañero."],
      "Señor, como a Marta, a veces me inquieto y me agito por muchas cosas. Ayúdame a poner primero lo único necesario, a ordenar mi tiempo con sabiduría y a decir que no cuando hace falta, para servir con alegría y no a medias. Amén.",
      "Pon primero las piedras grandes: lo demás se acomoda.",
      ("El cansancio también es un tema pastoral",
       "Un dirigente agotado no sirve mejor, sirve peor: se irrita, olvida, llega tarde. Cuidar el propio descanso y los tiempos de la familia no es egoísmo: es responsabilidad con la comunidad que confía en ti. Si sientes que no te alcanza el tiempo, conversa con tu coordinación para redistribuir las tareas."),
      [("Christus vivit (Francisco, 2019)", CV, "Capítulo 2, «Jesucristo siempre joven»."),
       ("Laudato si' (Francisco, 2015)", LS, "Números 222-227, sobre la sobriedad, la paz interior y el tiempo presente.")]),

    u("Encuentros y reuniones que respetan el tiempo",
      "Preparar y conducir encuentros y reuniones que empiecen y terminen a la hora, con horarios realistas.",
      "Las reuniones eternas y los encuentros que se alargan sin aviso son de las formas más comunes de faltar el respeto al tiempo de otros en la pastoral. La buena noticia es que se pueden corregir con unos pocos hábitos del equipo.",
      "Piensa en la última reunión o encuentro que se alargó. ¿Cuánto se alargó? ¿Por qué? ¿Quién pagó el costo?",
      ["Preparar una reunión con objetivo, tabla y tiempos.", "Conducir un encuentro respetando el horario.", "Diseñar programas de actividades con tiempos realistas."],
      [("¿Hace falta reunirse?",
        "Antes de convocar, pregúntate: ¿lo que hay que tratar necesita conversación, o basta un mensaje claro? Muchas reuniones existen solo para informar algo que podía escribirse en cinco líneas.\n\n"
        "Reúnanse para **discernir, decidir, planificar y rezar juntos**. Para informar, usen un mensaje o un documento compartido."),
       ("Convocar bien",
        "Una convocatoria que respeta el tiempo de los demás incluye:\n\n"
        "- **Objetivo:** qué queremos lograr al terminar.\n"
        "- **Tabla con tiempos:** cada tema con sus minutos.\n"
        "- **Hora de inicio y de término.**\n"
        "- **Qué leer o traer antes,** para no ocupar la reunión en eso.\n"
        "- **Anticipación:** al menos tres o cuatro días antes, para que cada uno se organice."),
       ("Conducir con el reloj a la vista",
        "- **Empieza a la hora** con quienes están. No resumas lo tratado para los que llegan tarde: que lo pregunten al final.\n"
        "- **Nombra a alguien que cuide el tiempo,** que avise cuando quedan cinco minutos de cada tema.\n"
        "- **Si un tema se alarga,** decide en grupo: se acorta otro tema, se deja para la próxima o se forma una comisión. Pero no se alarga la hora de término sin consultar.\n"
        "- **Termina con los acuerdos:** qué, quién y para cuándo.\n"
        "- **Termina a la hora,** aunque falte algo. Quien quiera seguir conversando, puede quedarse; quien tiene que irse, se va tranquilo."),
       ("Programas con tiempos realistas",
        "En los encuentros y actividades, los atrasos casi siempre se producen por programas imposibles:\n\n"
        "- **Las dinámicas duran más de lo que crees:** explicar, formar grupos y volver toma tiempo. Calcula un 30 % más.\n"
        "- **Considera los tiempos muertos:** traslados entre lugares, ir al baño, servir la comida, ordenar la sala.\n"
        "- **En actividades de más de un día,** las comidas marcan el ritmo: arma primero la grilla de comidas y luego ubica las actividades (lo verás en la formación de Logística).\n"
        "- **Respeta la hora de salida** comunicada a las familias: si un encuentro termina a las 20:00, a las 20:00 los jóvenes están saliendo, no empezando la oración final.")],
      ("Los papás en el estacionamiento",
       "El encuentro de confirmación debía terminar a las 20:00. A las 20:00 recién empezó la oración final, y a las 20:25 terminó el compartir. Afuera, una decena de papás esperaba en los autos; algunos tenían que trabajar temprano al día siguiente. La catequista no entendía por qué varias familias se quejaron, si «la oración estuvo tan bonita».",
       ["¿Qué faltó en la planificación del encuentro?", "¿Cómo se podría haber cuidado la oración final sin pasarse del horario?"]),
      [["Tabla", "Lista ordenada de los temas de una reunión, con el tiempo asignado a cada uno."], ["Guardián del tiempo", "Persona que en una reunión avisa cuánto tiempo queda en cada tema."], ["Tiempo muerto", "Tiempo que se va en traslados, esperas y transiciones, y que hay que considerar al programar."]],
      ("1 Corintios 14,26-33.40 · Todo con orden",
       "Pablo orienta a la comunidad de Corinto para que sus reuniones no sean un desorden: que hablen por turno, que cada uno aporte para edificar a los demás, porque Dios no es un Dios de confusión sino de paz. Y concluye: que todo se haga con decoro y orden."),
      ("¿Tus reuniones y encuentros edifican, o cansan y desordenan?", "Ofrece al Señor las reuniones de tu equipo y pídele un espíritu de paz y orden.", "En tu próxima reunión, propón una tabla con tiempos y nombra a un guardián del tiempo."),
      [("Evangelii gaudium 222-225", EG, "Los procesos importan más que ocupar espacios; una buena organización está al servicio de que los procesos maduren."),
       ("Christus vivit 202-208", CV, "Francisco propone una pastoral juvenil sinodal, en la que se escucha y se participa; las buenas reuniones son una forma de vivir esa sinodalidad.")],
      ["¿Qué reuniones de tu grupo podrían ser un mensaje?", "¿Quién cuida hoy el tiempo en tus reuniones?", "¿Qué actividad de tu programa suele alargarse? ¿Por qué?", "¿Qué hora de salida comunican a las familias y cuántas veces la cumplen?"],
      "En grupos, tomen el programa de su próximo encuentro y revísenlo con lupa: agreguen un 30 % al tiempo de cada dinámica, sumen los tiempos muertos y comparen con la hora de término. Si no cabe, decidan qué sacar. Luego preparen la convocatoria de su próxima reunión de equipo con objetivo, tabla con tiempos y hora de término.",
      ["Revisen el programa del próximo encuentro.", "Ajusten tiempos de dinámicas y tiempos muertos.", "Decidan qué sacar si no cabe.", "Preparen la convocatoria de la próxima reunión."],
      "Dios de la paz, que no eres un Dios de confusión: haz que nuestras reuniones y encuentros sean espacios de orden, escucha y fraternidad. Que sepamos empezar a la hora, cuidar la palabra de cada uno y terminar cuando prometimos, para que nadie salga cansado de encontrarse con nosotros. Amén.",
      "Una reunión bien preparada cuida el tiempo de todos; una mal preparada lo consume.",
      ("Menos, pero mejor",
       "La tentación de muchos equipos es llenar los encuentros de actividades. Un encuentro con una dinámica, un momento de Palabra bien preparado y un compartir sin apuro suele dejar más que uno con cinco actividades corriendo. Programar menos es una forma de respetar el tiempo y la profundidad."),
      [("Evangelii gaudium (Francisco, 2013)", EG, "Números 222-225."),
       ("Christus vivit (Francisco, 2019)", CV, "Capítulo 7, «La pastoral de los jóvenes».")]),

    u("Mensajes que cuidan el tiempo del otro",
      "Comunicarse por chat, correo y redes de manera clara, oportuna y respetuosa del tiempo y el descanso de los demás.",
      "Hoy gran parte de la coordinación pastoral pasa por WhatsApp y otras aplicaciones. Un mensaje confuso, un grupo con cien notificaciones al día o un audio de diez minutos a medianoche también consumen el tiempo y la paz de los demás. Comunicar bien es respetar.",
      "Revisa el grupo de WhatsApp de tu comunidad o equipo. ¿Cuántos mensajes hubo ayer? ¿Cuántos eran realmente necesarios?",
      ["Escribir mensajes completos y claros a la primera.", "Establecer normas de uso para los grupos de la pastoral.", "Avisar a tiempo y confirmar compromisos."],
      [("Un mensaje completo a la primera",
        "Cada mensaje incompleto genera preguntas, respuestas y más mensajes. Un buen aviso responde de una vez:\n\n"
        "- **Qué:** la actividad o el pedido.\n"
        "- **Cuándo:** fecha, hora de inicio **y de término**.\n"
        "- **Dónde:** el lugar, con referencia o ubicación.\n"
        "- **Qué llevar o preparar.**\n"
        "- **Hasta cuándo responder,** si se necesita confirmación.\n\n"
        "Si el mensaje es importante, **escríbelo** en vez de mandar un audio: se lee en segundos y se puede volver a consultar."),
       ("Normas para los grupos",
        "Un grupo sin normas termina siendo un ruido que nadie lee. Acuerden con el grupo:\n\n"
        "- **Para qué es el grupo:** avisos, coordinación o conversación (pueden ser grupos distintos).\n"
        "- **Horario:** no escribir de noche ni muy temprano, salvo emergencias. Si escribes tarde, programa el mensaje o espera al día siguiente.\n"
        "- **Respuestas al privado:** «gracias», «ok» y conversaciones de dos personas, por mensaje privado.\n"
        "- **Sin cadenas** ni contenido ajeno al propósito del grupo.\n"
        "- **Los mensajes importantes, fijados** para que no se pierdan.\n\n"
        "Si hay menores en los grupos, recuerda además las orientaciones de buen trato y prevención de tu comunidad."),
       ("Avisar y confirmar a tiempo",
        "Muchos problemas de tiempo vienen de lo que **no** se dijo:\n\n"
        "- **Confirma** si vas o no vas, en el plazo pedido. El «visto» sin respuesta obliga a otro a perseguirte.\n"
        "- **Avisa apenas sepas** que vas a llegar tarde o no vas a poder cumplir algo. Un aviso a tiempo permite reorganizarse; uno de último minuto deja a otros en problemas.\n"
        "- **Responde en un plazo razonable** los mensajes que esperan una respuesta tuya, aunque sea para decir «lo reviso y te contesto el jueves»."),
       ("El derecho al descanso",
        "Que podamos escribir a cualquier hora no significa que debamos hacerlo. Los dirigentes, los coordinadores y los asesores también necesitan desconectarse: estudiar, trabajar, estar con su familia, descansar y rezar.\n\n"
        "Una comunidad que respeta el tiempo de sus servidores **no espera respuestas inmediatas** fuera de horario y **no premia** al que contesta a medianoche. Cuidar el descanso del otro es también una forma de caridad.")],
      ("El grupo de las 200 notificaciones",
       "El grupo de WhatsApp de la pastoral juvenil tiene 60 personas. Un viernes, un aviso del encuentro del sábado queda enterrado entre stickers, felicitaciones de cumpleaños y una discusión sobre fútbol. Al día siguiente, la mitad no sabía que el lugar había cambiado y llegó a la parroquia equivocada.",
       ["¿Qué falló en el uso del grupo?", "¿Qué normas propondrías para que no vuelva a pasar?"]),
      [["Mensaje completo", "Aviso que responde de una vez qué, cuándo (con hora de término), dónde, qué llevar y hasta cuándo responder."], ["Normas del grupo", "Acuerdos sobre el propósito, el horario y el uso de un grupo de mensajería."], ["Desconexión", "Tiempo en que una persona no está disponible para mensajes, para descansar y estar con los suyos."]],
      ("Mateo 5,37 · Que tu sí sea sí",
       "Jesús enseña a hablar con sencillez y verdad: que tu sí sea sí y tu no sea no. Una palabra clara y cumplida ahorra confusiones, explicaciones y tiempo a todos."),
      ("¿Tus mensajes son claros? ¿Cumples lo que confirmas?", "Pide al Señor una palabra sencilla, verdadera y oportuna.", "Esta semana, responde todos los mensajes que esperan algo de ti y no escribas al grupo después de las 22:00."),
      [("Christus vivit 86-90", CV, "El ambiente digital ofrece oportunidades y riesgos; requiere discernimiento para que la comunicación construya comunidad y no la desgaste."),
       ("Mensaje para la Jornada Mundial de las Comunicaciones Sociales 2019, «Somos miembros unos de otros»", None, "Francisco invita a que las redes sean un lugar de encuentro verdadero y no de aislamiento ni de ruido.")],
      ["¿Qué tipo de mensajes te hacen perder más tiempo?", "¿Tu grupo tiene normas? ¿Se respetan?", "¿Respondes a tiempo cuando alguien espera tu confirmación?", "¿Cómo cuidas el descanso de quienes coordinan?"],
      "En grupos, reescriban tres mensajes reales (o inventados) que hayan generado confusión, para que sean completos a la primera. Luego redacten las normas del grupo de WhatsApp de su comunidad (máximo seis) y el mensaje con que las propondrían al grupo.",
      ["Reescriban tres mensajes confusos.", "Redacten las normas del grupo.", "Preparen el mensaje para proponerlas.", "Acuerden un horario de mensajes."],
      "Señor, que nuestras palabras sean claras y verdaderas, que nuestro sí sea sí y nuestro no sea no. Que sepamos avisar a tiempo, responder con responsabilidad y respetar el descanso de los demás, para que nuestra comunicación construya comunidad. Amén.",
      "Un mensaje completo a la primera ahorra diez mensajes después.",
      ("Audio, texto o llamada",
       "Cada formato tiene su lugar. El **texto** es para avisos e información que se va a consultar después. El **audio** sirve para algo personal y breve, nunca para datos como horas o direcciones. La **llamada** es para lo urgente o lo delicado. Y lo importante, cuando se puede, se conversa **en persona**."),
      [("Christus vivit (Francisco, 2019)", CV, "Números 86-90, sobre el ambiente digital.")]),

    u("Compromisos, plazos y el tiempo de Dios",
      "Cumplir plazos y compromisos en equipo, y aprender a respetar también los tiempos de los procesos de las personas.",
      "Respetar el tiempo del otro incluye cumplir lo que prometimos, en el plazo prometido, para que otros puedan hacer su parte. Pero también incluye algo más profundo: respetar los tiempos de crecimiento de cada persona, que no siempre coinciden con nuestros calendarios.",
      "Haz una lista de los compromisos que tienes pendientes con tu equipo o comunidad. ¿Alguno está atrasado? ¿Avisaste?",
      ["Cumplir plazos pensando en quienes dependen de nuestro trabajo.", "Vencer la postergación con pasos pequeños.", "Respetar los tiempos de los procesos de las personas."],
      [("Cada plazo tiene a alguien detrás",
        "En un equipo, cada tarea está conectada con otras. Si quien debía reservar el bus lo hace tarde, quien hace el presupuesto no puede cerrar la cuota, y las familias reciben la información encima.\n\n"
        "Por eso, antes de aceptar un plazo pregúntate **quién depende de que yo cumpla**, y si no vas a llegar, **avisa antes de que venza**, no después. Un plazo renegociado a tiempo es responsabilidad; un plazo incumplido en silencio es descuido."),
       ("Vencer la postergación",
        "Todos postergamos lo que se nos hace difícil, largo o aburrido. Algunas claves:\n\n"
        "- **Divide la tarea** en pasos pequeños: «organizar el retiro» no se puede empezar; «llamar a la casa de retiro para preguntar fechas» sí.\n"
        "- **Regla de los dos minutos:** si algo toma menos de dos minutos, hazlo ahora.\n"
        "- **Ponle fecha a cada paso** en tu calendario, no solo a la tarea completa.\n"
        "- **Pide a alguien que te pregunte** cómo vas: el acompañamiento también sirve para esto.\n"
        "- **Empieza por lo más difícil** cuando tienes más energía."),
       ("No sobrecargar a los demás",
        "Respetar el tiempo del otro también es no pedir a último minuto lo que podía pedirse con anticipación. Antes de encargar algo, pregúntate: ¿le estoy dando tiempo suficiente? ¿Sabe exactamente qué se espera y para cuándo? ¿Le estoy pidiendo demasiado a la misma persona?\n\n"
        "Los equipos sanos reparten las tareas, piden con anticipación y agradecen el tiempo que cada uno regala."),
       ("El tiempo de los procesos",
        "En la pastoral trabajamos con personas, y las personas no crecen al ritmo de nuestro calendario. Un joven puede tardar meses en abrirse, en volver a confesarse o en decidirse a servir. Una familia puede necesitar tiempo para confiar.\n\n"
        "Respetar el tiempo del otro es también **no apurar sus procesos**: acompañar con paciencia, sembrar sin exigir resultados inmediatos y confiar en que Dios trabaja a su ritmo. El papa Francisco lo dice así: **el tiempo es superior al espacio**; importa más iniciar procesos que dominar resultados.")],
      ("El bus que nadie reservó",
       "Faltando tres semanas para las misiones, Camila se comprometió a cotizar y reservar el bus. Lo fue dejando para después y no avisó. Una semana antes, ya no había buses disponibles a un precio razonable, la cuota tuvo que subir y dos familias dijeron que no podían pagar.",
       ["¿Quiénes pagaron el costo del plazo incumplido?", "¿Qué podría haber hecho Camila, y qué podría haber hecho el equipo, para evitarlo?"]),
      [["Plazo", "Fecha límite acordada para cumplir una tarea, de la que suelen depender otras personas."], ["Postergación", "Tendencia a dejar para después lo que conviene hacer ahora."], ["Proceso", "Camino de crecimiento de una persona o comunidad, que tiene sus propios tiempos."]],
      ("2 Pedro 3,8-9 · La paciencia de Dios",
       "Para el Señor, un día es como mil años y mil años como un día. El Señor no se retrasa en cumplir su promesa, como algunos piensan: tiene paciencia, porque quiere que todos lleguen a la conversión. Dios cumple, y a la vez espera con paciencia a cada uno."),
      ("¿Qué compromisos estás postergando? ¿Con quién necesitas más paciencia?", "Agradece la paciencia que Dios ha tenido con tu propio proceso.", "Esta semana, cumple o renegocia a tiempo un compromiso atrasado, y ten un gesto de paciencia con alguien de tu grupo."),
      [("Evangelii gaudium 169-173", EG, "El acompañamiento personal de los procesos de crecimiento requiere paciencia, escucha y respeto por los tiempos de cada persona."),
       ("Gaudete et exsultate 166-169", GE, "El discernimiento ayuda a reconocer los tiempos de Dios en la propia vida y a responder con prontitud y libertad.")],
      ["¿Qué plazo tuyo está afectando hoy a otra persona?", "¿Qué tarea postergada podrías dividir en pasos pequeños?", "¿A quién le pides cosas a último minuto?", "¿Qué proceso de una persona de tu grupo necesitas respetar con más paciencia?"],
      "Cada participante revisa sus compromisos pendientes y los divide en pasos con fecha. Luego, en grupo, redacten el «pacto del tiempo» de su equipo: acuerdos sobre puntualidad, reuniones, mensajes, plazos y descanso, que presentarán a su comunidad en el taller de cierre.",
      ["Revisa tus compromisos pendientes.", "Divídelos en pasos con fecha.", "Avisa si alguno no lo vas a poder cumplir.", "Redacten el borrador del pacto del tiempo."],
      "Señor, Tú cumples siempre tus promesas y esperas con paciencia a cada uno. Ayúdame a ser fiel a mis compromisos, a cumplir mis plazos pensando en quienes dependen de mí y a respetar los tiempos de las personas que acompaño, como Tú respetas los míos. Amén.",
      "Cumplir a tiempo cuida a los demás; esperar con paciencia, también.",
      ("Tiempo para lo que no se mide",
       "Al final, respetar el tiempo de los demás es lo que permite que sobre tiempo para lo esencial: la conversación sin apuro con un joven que lo necesita, la oración tranquila, la celebración, el descanso compartido. Ordenamos el tiempo para que haya espacio para el encuentro."),
      [("Evangelii gaudium (Francisco, 2013)", EG, "Números 169-173, sobre el acompañamiento personal."),
       ("Gaudete et exsultate (Francisco, 2018)", GE, "Capítulo 5, sobre el discernimiento.")]),
]

EVALUACION = [
    q("¿Qué diferencia hay entre cronos y kairós?", ["Cronos es el tiempo del reloj; kairós, el tiempo oportuno o de gracia.", "Son dos nombres del mismo tiempo.", "Kairós es el tiempo libre y cronos el de trabajo."], 0, "Gestionar bien el cronos deja espacio para el kairós."),
    q("Si un encuentro de 30 personas empieza 20 minutos tarde, ¿cuánto tiempo de la comunidad se perdió?", ["20 minutos.", "Unas 10 horas (600 minutos).", "Una hora."], 1, "La impuntualidad se multiplica por todas las personas que esperan."),
    q("Cuando un encuentro está citado a una hora y aún hay pocos, ¿qué conviene hacer?", ["Esperar a que lleguen todos.", "Empezar a la hora con quienes están.", "Suspender el encuentro."], 1, "Empezar a la hora honra a quienes llegaron y educa a los demás."),
    q("En la matriz de urgente e importante, ¿qué cuadro conviene cuidar más?", ["Urgente y no importante.", "Importante y no urgente.", "Ni urgente ni importante."], 1, "Si se le da tiempo a lo importante no urgente, disminuyen las urgencias."),
    q("¿Qué significa «primero las piedras grandes»?", ["Hacer primero las tareas más pesadas físicamente.", "Agendar primero lo que no puede faltar: estudio o trabajo, familia, descanso, oración y servicio.", "Dejar lo importante para el final de la semana."], 1, "Lo demás se acomoda entre las prioridades."),
    q("¿Cuál es una buena práctica al conducir una reunión?", ["Alargarla hasta terminar todos los temas.", "Nombrar a alguien que cuide el tiempo y terminar a la hora.", "Resumir todo cada vez que alguien llega tarde."], 1, "Si un tema se alarga, se decide qué acortar, sin pasar la hora de término sin consultar."),
    q("Al programar las dinámicas de un encuentro, ¿qué conviene hacer?", ["Calcular justo lo que dura la actividad.", "Sumar alrededor de un 30 % más y considerar los tiempos muertos.", "No poner horarios."], 1, "Explicar, formar grupos y volver siempre toma más tiempo."),
    q("¿Qué debe incluir un aviso completo?", ["Solo el día.", "Qué, cuándo (con hora de término), dónde, qué llevar y hasta cuándo responder.", "Un audio explicativo."], 1, "Un mensaje completo a la primera ahorra muchos mensajes después."),
    q("Si sabes que no vas a cumplir un plazo, ¿qué haces?", ["Esperar a ver si alguien se da cuenta.", "Avisar antes de que venza y proponer una alternativa.", "Avisar después de la fecha."], 1, "Renegociar a tiempo es responsabilidad; incumplir en silencio es descuido."),
    q("¿Qué significa respetar el tiempo de los procesos de las personas?", ["Exigir resultados rápidos.", "Acompañar con paciencia, sin apurar su crecimiento.", "Dejar de acompañar a quien avanza lento."], 1, "El tiempo es superior al espacio: importa más iniciar procesos que dominar resultados."),
]

TALLER = ("El pacto del tiempo: cada participante presenta su auditoría de una semana (cuánto tiempo dedicó a sus piedras grandes, dónde se le fue el tiempo "
          "y qué cambiará). Luego, el equipo completo acuerda y firma el pacto del tiempo de su comunidad, con acuerdos concretos sobre puntualidad (llegar, empezar "
          "y terminar a la hora), reuniones (convocatoria, tabla y guardián del tiempo), mensajes (aviso completo, horario y normas del grupo), plazos (avisar antes "
          "de que venzan) y descanso. Definen cómo lo comunicarán a los jóvenes y a las familias, y cuándo lo evaluarán.")

FORMACION = {
    "id": "gestion-del-tiempo",
    "titulo": "El tiempo del otro: gestión del tiempo en la pastoral",
    "subtitulo": "Puntualidad, prioridades, reuniones, mensajes y plazos que respetan a los demás",
    "categoria": "Misión y servicio",
    "publico": "Desde 14 años",
    "descripcion": "Una formación para aprender a gestionar el tiempo desde el respeto por el tiempo de los demás: la puntualidad como acogida, las prioridades personales, encuentros y reuniones que empiezan y terminan a la hora, mensajes que cuidan el tiempo y el descanso del otro, y compromisos cumplidos a tiempo sin apurar los procesos de las personas. 5 unidades de 90 minutos y una evaluación final.",
    "modulo": "El tiempo del otro",
    "intro": "El tiempo es un don de Dios, y el tiempo de cada persona que viene a un encuentro, a una reunión o a una actividad es un regalo que nos confía. En esta formación aprenderás a ordenar tu propio tiempo para servir mejor, y sobre todo a cuidar el tiempo de los demás: llegar, empezar y terminar a la hora, preparar reuniones que no desgasten, comunicar con claridad, cumplir los plazos y respetar los tiempos de crecimiento de cada persona.",
    "unidades": UNIDADES,
    "evaluacion": EVALUACION,
    "taller": TALLER,
}

if __name__ == "__main__":
    destino = R / "fuentes" / "complementarias" / "gestion-del-tiempo.json"
    destino.write_text(json.dumps(FORMACION, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    import complementarias
    complementarias.generar(destino)
    print("escrito", destino)
