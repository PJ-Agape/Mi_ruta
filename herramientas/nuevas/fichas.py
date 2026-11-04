"""Ejes temáticos y competencias de cada formación (se muestran al tocar una tarjeta de la portada)."""

FICHAS = {
    # ---------------- Cursos y diplomados
    "dirigente-juvenil": {
        "ejes": ["Vocación y espiritualidad del dirigente", "Vida de grupo y acompañamiento", "Metodología y animación", "Liturgia y vida sacramental del grupo", "Organización, cuidado y relevo"],
        "competencias": ["Discernir y sostener su vocación de servicio con una vida de oración.",
                         "Acoger, escuchar y acompañar a los jóvenes de su grupo.",
                         "Preparar y animar encuentros con metodología participativa.",
                         "Planificar, coordinar y evaluar las actividades del grupo con su equipo.",
                         "Crear ambientes seguros y actuar según los protocolos de buen trato."],
    },
    "diplomado": {
        "ejes": ["Liderazgo personal y autoridad", "Equipos, delegación y acompañamiento", "Comunicación y conflictos", "Planificación y proyectos", "Proyecto integrador"],
        "competencias": ["Ejercer un liderazgo de servicio basado en la confianza y el ejemplo.",
                         "Formar equipos, delegar y acompañar el crecimiento de otros dirigentes.",
                         "Comunicar con claridad y mediar en conflictos.",
                         "Diseñar, presupuestar y evaluar proyectos pastorales.",
                         "Llevar a cabo un proyecto real en su comunidad con asesoría."],
    },
    "servicio-liturgico": {
        "ejes": ["Sentido de la liturgia", "Servicio del altar", "Proclamación de la Palabra", "Música y canto", "Buen trato en el servicio"],
        "competencias": ["Comprender la estructura y el sentido de la misa.",
                         "Servir en el altar, proclamar las lecturas o animar el canto con dignidad.",
                         "Preparar con su equipo las celebraciones del año litúrgico.",
                         "Vivir el servicio litúrgico como camino de fe."],
    },
    "fe-y-catequesis": {
        "ejes": ["La Biblia", "Modelos de santidad", "Catequesis de niños y jóvenes", "Animación y comunicación"],
        "competencias": ["Manejar la Biblia y leerla con sentido.",
                         "Presentar la fe con testimonios de vida cercanos.",
                         "Apoyar al catequista en la preparación y animación de encuentros.",
                         "Cuidar a niños y adolescentes con criterios de buen trato."],
    },
    "mision-y-servicio": {
        "ejes": ["Caridad y doctrina social", "Cuidado de la casa común", "Misión juvenil", "Organización y logística", "Seguridad y cuidado"],
        "competencias": ["Fundamentar el servicio en el Evangelio y la doctrina social de la Iglesia.",
                         "Diseñar y llevar a cabo proyectos solidarios o ecológicos.",
                         "Preparar, vivir y evaluar una misión juvenil.",
                         "Organizar la logística de una actividad con seguridad."],
    },
    "diplomado-escritura": {
        "ejes": ["Introducción al Antiguo y al Nuevo Testamento", "Pentateuco, Profetas y Sapienciales", "Evangelios, Hechos y San Pablo", "Escritos joánicos, Hebreos y Apocalipsis", "Interpretación de la Biblia en la Iglesia"],
        "competencias": ["Situar cada libro bíblico en su contexto histórico y literario.",
                         "Interpretar un texto según los criterios de *Dei Verbum* y de la Pontificia Comisión Bíblica.",
                         "Realizar el análisis exegético de una perícopa por escrito.",
                         "Usar la Biblia con fundamento en la catequesis, la predicación y los grupos bíblicos."],
    },
    "catequista": {
        "ejes": ["Identidad del agente pastoral", "Contenidos de la fe: Biblia, Credo y sacramentos", "Pedagogía de la catequesis", "Acompañamiento y animación de grupos", "Organización y cuidado"],
        "competencias": ["Explicar con sencillez y fidelidad los contenidos de la fe.",
                         "Preparar y animar encuentros de catequesis según la edad.",
                         "Acompañar a catequizandos y familias en el camino de iniciación cristiana.",
                         "Coordinarse con la comunidad y cuidar ambientes seguros."],
    },
    # ---------------- Módulos sueltos
    "servidores-del-altar": {
        "ejes": ["Vocación de servicio", "El templo y los objetos litúrgicos", "La misa paso a paso", "Celebraciones especiales"],
        "competencias": ["Reconocer los objetos y lugares de la celebración.", "Servir en cada momento de la misa.", "Trabajar en equipo con otros servidores."],
    },
    "lectores-y-salmistas": {
        "ejes": ["La Palabra en la liturgia", "Preparación de la lectura", "Voz y micrófono", "El salmo responsorial"],
        "competencias": ["Preparar y proclamar una lectura con claridad.", "Cantar o recitar el salmo responsorial.", "Redactar y leer la oración universal."],
    },
    "musica-liturgica": {
        "ejes": ["La música en la liturgia", "Elección de cantos", "Tiempos litúrgicos", "Animación de la asamblea"],
        "competencias": ["Elegir cantos adecuados para cada momento y tiempo litúrgico.", "Preparar ensayos y animar el canto de la asamblea.", "Vivir el coro como comunidad de servicio."],
    },
    "conocer-la-biblia": {
        "ejes": ["Organización de la Biblia", "Palabra de Dios en palabras humanas", "Géneros y contexto", "La Biblia en la vida y en el grupo"],
        "competencias": ["Buscar y citar textos bíblicos.", "Distinguir géneros literarios y leer en contexto.", "Animar una lectura orante en grupo."],
    },
    "santos-jovenes": {
        "ejes": ["Llamado a la santidad", "Santos de Chile", "Testigos de nuestro tiempo", "El propio camino"],
        "competencias": ["Presentar la vida de santos jóvenes como modelos cercanos.", "Relacionar sus testimonios con la vida de los jóvenes de hoy.", "Proponer un camino personal de santidad."],
    },
    "el-credo": {
        "ejes": ["La fe como respuesta", "Dios Padre creador", "Jesucristo", "El Espíritu Santo y la Iglesia", "La esperanza cristiana"],
        "competencias": ["Explicar los artículos del Credo con lenguaje sencillo.", "Fundamentar la fe en la Escritura y el Catecismo.", "Responder preguntas frecuentes sobre la fe."],
    },
    "sacramentos": {
        "ejes": ["Qué es un sacramento", "Bautismo y Confirmación", "Eucaristía y primera comunión", "Reconciliación e iniciación cristiana"],
        "competencias": ["Explicar el sentido y los signos de cada sacramento de iniciación.", "Acompañar a familias y catequizandos en la preparación sacramental.", "Integrar la vida sacramental en la catequesis."],
    },
    "misiones-juveniles": {
        "ejes": ["Sentido de la misión", "Preparación responsable", "Anuncio y vida en terreno", "Evaluación y continuidad"],
        "competencias": ["Organizar una misión de verano o invierno.", "Anunciar a Jesús con respeto en visitas y actividades.", "Evaluar la misión y darle continuidad."],
    },
    "ayudante-de-catequesis": {
        "ejes": ["Qué es la catequesis", "Etapas de niños y adolescentes", "Preparar y animar encuentros", "Familias y comunidad"],
        "competencias": ["Colaborar con el catequista en la preparación de encuentros.", "Adaptar actividades a la edad de los catequizandos.", "Cuidar a los niños con criterios de buen trato."],
    },
    "voluntariado-y-doctrina-social": {
        "ejes": ["Fe y caridad", "Principios de la doctrina social", "Servir con criterio", "Proyecto solidario"],
        "competencias": ["Aplicar los principios de la doctrina social al servicio.", "Servir con dignidad y respeto a las personas.", "Diseñar un proyecto solidario."],
    },
    "ecologia-integral": {
        "ejes": ["La creación como don", "Crisis ambiental y pobreza", "Hábitos cotidianos", "Conversión ecológica"],
        "competencias": ["Explicar la ecología integral según *Laudato si'*.", "Proponer cambios de hábitos en el grupo.", "Diseñar un proyecto por la casa común."],
    },
    "buen-trato-y-prevencion": {
        "ejes": ["Cultura del buen trato", "Ambientes seguros", "Escucha y actuación ante una revelación", "Reparación y cuidado mutuo"],
        "competencias": ["Aplicar normas de ambientes seguros en actividades pastorales.", "Saber cómo actuar y a quién informar ante una revelación.", "Promover una cultura de cuidado en el grupo."],
    },
    "primeros-auxilios": {
        "ejes": ["Evaluación de la escena y pedido de ayuda", "Emergencias vitales", "Lesiones frecuentes", "Prevención en actividades"],
        "competencias": ["Evaluar una emergencia y pedir ayuda correctamente.", "Aplicar primeros auxilios básicos en lesiones frecuentes.", "Planificar actividades con medidas de prevención."],
    },
    "primeros-auxilios-psicologicos": {
        "ejes": ["Qué es una crisis", "Protocolo ABCD", "Situaciones difíciles", "Cuidado del que cuida"],
        "competencias": ["Brindar primera ayuda psicológica con el protocolo ABCD.", "Reconocer cuándo derivar a un profesional.", "Cuidarse y cuidar al equipo después de una crisis."],
    },
    "comunicacion-y-redes": {
        "ejes": ["Comunicar con sentido", "Creación de contenidos", "Cuidado en lo digital", "Plan de comunicación"],
        "competencias": ["Crear contenidos claros para redes y afiches.", "Cuidar la imagen y los datos de las personas en lo digital.", "Elaborar un plan de comunicación para el grupo."],
    },
    "dinamicas-y-juegos": {
        "ejes": ["El juego en la pastoral", "Diseño de dinámicas", "Banco de dinámicas", "Grandes juegos y seguridad"],
        "competencias": ["Diseñar y conducir una dinámica con objetivo claro.", "Animar una jornada completa.", "Adaptar juegos para que sean seguros e inclusivos."],
    },
    "logistica": {
        "ejes": ["Planificación logística", "Alimentación", "Materiales e inventario", "Lugares y traslados", "Presupuesto y rendición"],
        "competencias": ["Planificar la logística de jornadas, retiros y campamentos.", "Calcular menús, cantidades e insumos.", "Gestionar presupuesto, compras y rendición de cuentas."],
    },
}
