"""Taller práctico de la sesión de cierre de cada módulo (antes de la evaluación)."""
TALLERES = {
 # Formaciones complementarias
 "servidores-del-altar": "Ensayo general en el templo: el grupo prepara y sirve una misa completa de práctica (o una celebración de la Palabra), con todos los roles repartidos. Antes, revisan juntos la credencia con la lista de chequeo; después, cada servidor dice qué hizo bien y qué mejorará, y el coordinador da una retroalimentación breve.",
 "lectores-y-salmistas": "Cada participante proclama una lectura y un salmo del próximo domingo ante el grupo, con micrófono si es posible. Antes de proclamar comparte en una frase lo que el texto le dijo en la oración. Los demás dan retroalimentación sobre tres aspectos: comprensión del texto, voz y ritmo, y presencia.",
 "musica-liturgica": "El coro prepara la música completa de una misa del tiempo litúrgico actual: elige los cantos con los criterios del módulo, arma la hoja de cantos, hace un ensayo de 30 minutos y anima a la asamblea (el resto del grupo) en los momentos principales. Al final evalúan juntos qué ayudó a rezar.",
 "conocer-la-biblia": "Por parejas, cada uno guía un momento de Palabra compartida de 20 minutos con un texto elegido por el grupo, usando los siete pasos. Antes deben explicar en dos minutos el género y el contexto del texto. El resto del grupo participa y luego comenta qué funcionó.",
 "santos-jovenes": "Cada participante presenta en tres minutos a un santo o testigo de la fe que lo haya marcado (puede ser de los estudiados o uno nuevo), con un dato de su vida, una frase y lo que le enseña. Al final, cada uno escribe en una tarjeta su propio «camino de santidad» para el próximo mes.",
 "ayudante-de-catequesis": "En parejas, preparan y animan un encuentro breve de catequesis (20 minutos) para un grupo de la edad que acompañan, con acogida, un momento de Palabra, una actividad y una oración. El grupo hace de catequizandos. Después, el catequista responsable da retroalimentación sobre preparación, trato y cuidado.",
 "misiones-juveniles": "Simulación de una jornada de misión: en parejas, cada equipo visita una «casa» (otro par de participantes que interpreta una familia con una situación preparada por el relator), escucha, comparte su testimonio y ofrece una oración. Luego se evalúa la visita con la pauta del módulo y se revisa la planificación logística de la próxima misión.",
 "voluntariado-y-doctrina-social": "Cada equipo presenta su proyecto solidario completo: diagnóstico, objetivo, plan, responsables, presupuesto y cómo se cuidará la dignidad de las personas atendidas. Los demás lo revisan con preguntas desde los principios de la doctrina social: ¿promueve o solo asiste?, ¿participan los destinatarios?, ¿es sostenible?",
 "ecologia-integral": "Cada equipo presenta su proyecto por la casa común (en la parroquia, el barrio o el colegio) con objetivo, acciones, responsables y fecha. Además, cada participante comparte un cambio concreto de su estilo de vida que mantuvo durante el módulo y cómo le fue.",
 "buen-trato-y-prevencion": "Análisis de casos en grupos: cada grupo recibe una situación (una salida, un mensaje privado, un rumor, una revelación de daño) y debe decidir qué hacer, a quién avisar y qué no hacer, según el protocolo de la parroquia. Al final, cada participante completa su tarjeta con los nombres y contactos del encargado de prevención y los números de ayuda.",
 "primeros-auxilios": "Estaciones prácticas: en grupos rotan por cuatro estaciones (evaluación inicial y llamada al 131, reanimación cardiopulmonar en maniquí si hay, maniobra ante atragantamiento y vendaje de una herida). Si es posible, el taller lo guía un profesional de la salud o un instructor certificado.",
 "primeros-auxilios-psicologicos": "Juego de roles en tríos: una persona vive una crisis (caso preparado por el relator), otra la acompaña aplicando el protocolo ABCD y la tercera observa con una pauta. Rotan los roles. Al cierre, cada participante revisa su tarjeta con los números de ayuda y el nombre del adulto responsable a quien derivar.",
 "comunicacion-y-redes": "Cada equipo presenta el plan de comunicación de su grupo para los próximos tres meses (objetivos, públicos, canales, calendario y roles) y una pieza de muestra: una publicación, una historia o un afiche. Los demás revisan que cuide la imagen y los datos de las personas.",
 "dinamicas-y-juegos": "Cada participante conduce una dinámica de 10 minutos con el grupo, usando la ficha de dinámica: objetivo, explicación, conducción y reflexión final. Los demás evalúan con una pauta breve: ¿se entendió?, ¿todos participaron?, ¿la reflexión ayudó a pensar?",
 "el-credo": None, "sacramentos": None, "logistica": None,
 # Dirigente juvenil
 "dj-discernimiento": "Retiro breve de discernimiento (90 minutos): un tiempo de silencio, una lectio divina personal con Samuel (1 Samuel 3,1-10) y una conversación de 15 minutos con el asesor o un acompañante. Cada participante escribe una carta a Dios con su respuesta, aunque sea «todavía no».",
 "dj-identidad": "Cada participante escribe su regla de vida para los próximos tres meses: oración diaria, Eucaristía, descanso, servicio y formación. La comparte en parejas y elige a alguien que lo acompañe a cumplirla.",
 "dj-acogida": "En grupos, diseñan los primeros 20 minutos de un encuentro para un grupo nuevo: acogida en la puerta, presentación, una dinámica de confianza y un momento en que todos tengan una tarea. Lo aplican con el resto del curso y reciben retroalimentación.",
 "dj-escucha": "Práctica de escucha en tríos: una persona cuenta algo real y no demasiado íntimo, otra escucha aplicando lo aprendido (sin aconsejar, con preguntas abiertas y poniendo nombre a lo que siente) y la tercera observa. Rotan. Al final cada uno identifica su principal dificultad para escuchar.",
 "dj-metodologia": "En equipos, planifican un encuentro completo de 60 minutos con el método vivir, conversar, iluminar y actuar, que incluya un juego y un momento de oración con símbolos. Presentan la planificación y animan la parte del juego con el curso.",
 "dj-eucaristia": "El grupo prepara la animación de una misa dominical: cantos, lectores, monición de entrada, oración de los fieles, procesión de ofrendas y servidores. Revisan con el párroco que todo respete la liturgia del día.",
 "dj-coordinar": "Cada participante arma el plan del año de su grupo en una página: objetivo, calendario cruzado con las fechas de la parroquia, responsables por actividad y presupuesto básico con formato de rendición de cuentas.",
 "dj-conducir": "Simulación de una reunión de equipo: con una agenda dada, un participante conduce, otro toma el acta y los demás representan roles (alguien que no cumplió un compromiso, dos que discuten). Al final se evalúa la conducción, el seguimiento de compromisos y la comunicación asertiva.",
 "dj-proyectar": "Cada participante prepara la carpeta de traspaso de su servicio (procesos, contactos, calendario, materiales y lecciones aprendidas) y el plan de acompañamiento de un futuro dirigente. Se cierra con una celebración de envío.",
}

# Preguntas de la evaluación de cada módulo de Dirigente juvenil, tomadas de las evaluaciones originales.
# (curso de origen, id de la evaluación, índices de las preguntas)
EVAL_DJ = {
 "dj-discernimiento": [("discernimiento-y-oracion", "m1-eval", list(range(9)))],
 "dj-identidad": [("arte-de-encontrarnos", "m1-eval", [0, 1, 3, 5, 7]), ("arte-de-encontrarnos", "m5-eval", [2, 5, 8]), ("arte-de-encontrarnos", "m4-eval", [7])],
 "dj-acogida": [("arte-de-encontrarnos", "m2-eval", [0, 2, 3, 4, 5, 6, 7]), ("arte-de-encontrarnos", "m1-eval", [4])],
 "dj-escucha": [("arte-de-encontrarnos", "m1-eval", [2, 6]), ("arte-de-encontrarnos", "m2-eval", [1]), ("arte-de-encontrarnos", "m3-eval", [0, 1, 4, 7]), ("arte-de-encontrarnos", "m5-eval", [0, 6])],
 "dj-metodologia": [("arte-de-encontrarnos", "m4-eval", [0, 1, 2, 3, 4, 5, 6]), ("arte-de-encontrarnos", "m3-eval", [2])],
 "dj-eucaristia": [("arte-de-encontrarnos", "m6-eval", list(range(8)))],
 "dj-coordinar": [("coordinar-es-servir", "m1-eval", [0, 1, 2, 4, 5]), ("coordinar-es-servir", "m2-eval", [0, 1, 4, 5]), ("coordinar-es-servir", "m3-eval", [2])],
 "dj-conducir": [("coordinar-es-servir", "m2-eval", [2, 6]), ("coordinar-es-servir", "m3-eval", [0, 1, 3]), ("coordinar-es-servir", "m4-eval", [0, 1, 3, 4, 5])],
 "dj-proyectar": [("arte-de-encontrarnos", "m5-eval", [3, 7]), ("coordinar-es-servir", "m4-eval", [2, 6]), ("coordinar-es-servir", "m5-eval", [2, 3, 4, 5, 6])],
}
