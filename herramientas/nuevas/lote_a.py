"""Quinta unidad de las formaciones complementarias (lote A: liturgia, fe y catequesis)."""
VAT = "https://www.vatican.va/"
SC = VAT + "archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19631204_sacrosanctum-concilium_sp.html"
OGMR = VAT + "roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_sp.html"
CEC_LIT = VAT + "archive/catechism_sp/p2s1c2a1_sp.html"
VD = VAT + "content/benedict-xvi/es/apost_exhortations/documents/hf_ben-xvi_exh_20100930_verbum-domini.html"
DV = VAT + "archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19651118_dei-verbum_sp.html"
CV = VAT + "content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20190325_christus-vivit.html"
GE = VAT + "content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20180319_gaudete-et-exsultate.html"
CEC_FAM = VAT + "archive/catechism_sp/p3s2c2a4_sp.html"

UNIDADES = {}

UNIDADES["servidores-del-altar"] = (3, {
 "title": "Un equipo de servidores",
 "objective": "Organizar el servicio del altar como un equipo: roles, turnos, preparación previa y acogida de nuevos servidores.",
 "intro": "Servir en el altar no es tarea de una persona sola. Detrás de cada celebración bien servida hay un equipo que se organiza, se prepara y se cuida. En esta unidad vas a pensar cómo funciona tu grupo de servidores y cómo hacer que cualquiera, nuevo o antiguo, sepa qué hacer.",
 "sections": [
  {"title": "Muchos servicios, un solo altar",
   "body": "En una misa con varios servidores, cada uno tiene una tarea clara. Algunos roles frecuentes:\n\n- **Cruz y ciriales:** encabezan la procesión de entrada y salida.\n- **Misal:** sostiene o acerca el misal al sacerdote en la sede y en el altar.\n- **Credencia:** prepara y acerca vinajeras, lavabo, corporal y vasos sagrados.\n- **Turiferario y naveta:** se encargan del incienso, cuando se usa.\n- **Campanilla:** marca los momentos de la consagración, si es costumbre en la parroquia.\n\nCuando cada uno sabe su tarea, el servicio es sereno y nadie corre ni improvisa."},
  {"title": "Antes de la misa",
   "body": "El servicio empieza antes de que suene la campana:\n\n- **Llegar con tiempo,** al menos 15 o 20 minutos antes.\n- **Revisar la credencia** con el sacristán o el coordinador: cáliz, patena, corporal, purificador, vinajeras, lavabo.\n- **Repartir los roles** del día y confirmar quién hace qué.\n- **Revestirse con calma** y en silencio.\n- **Orar juntos** un momento breve antes de salir en procesión."},
  {"title": "Turnos y coordinación",
   "body": "Un grupo que funciona bien suele tener:\n\n- **Un coordinador o coordinadora** que arma los turnos y es el contacto con el párroco y el sacristán.\n- **Un calendario de turnos** conocido por todos, con reemplazos acordados.\n- **Un canal de aviso** para cuando alguien no puede asistir, con tiempo.\n- **Reuniones breves** para revisar cómo va el servicio y preparar fechas especiales.\n\nCuidar los turnos es cuidar a la comunidad: que nunca falte servicio y que nadie cargue con todo."},
  {"title": "Recibir y formar a los nuevos",
   "body": "Los servidores con más experiencia tienen una tarea hermosa: acompañar a los que llegan.\n\n- **Asignar un padrino o madrina** a cada nuevo servidor durante sus primeras misas.\n- **Empezar por roles sencillos** y avanzar poco a poco.\n- **Explicar el sentido,** no solo los movimientos.\n- **Corregir con cariño,** después de la misa y en privado.\n- **Celebrar los pasos:** la primera vez que alguien sirve, el envío anual, el cambio de rol.\n\nCuando hay niños menores de 13 años sirviendo, siempre debe haber un adulto responsable presente."}
 ],
 "bible": {"ref": "Romanos 12,4-8 · Muchos miembros, un solo cuerpo",
  "comment": "Pablo compara a la comunidad con un cuerpo: cada miembro tiene una función distinta y todos son necesarios. Un equipo de servidores vive esto en pequeño: el que lleva la cruz no vale más que el que prepara las vinajeras. Cada servicio, hecho con amor, es parte del mismo cuerpo."},
 "church": [
  {"source": "Sacrosanctum concilium 29", "text": "Los acólitos y los demás ministros desempeñan un auténtico ministerio litúrgico, y deben cumplirlo con piedad sincera y orden.", "url": SC},
  {"source": "Catecismo de la Iglesia Católica 1140-1144", "text": "Toda la asamblea celebra la liturgia, y dentro de ella cada uno sirve según su función.", "url": CEC_LIT}
 ],
 "questions": [
  "¿Qué roles existen en tu grupo de servidores? ¿Están claros para todos?",
  "¿Qué pasa en tu parroquia cuando alguien falta a su turno?",
  "¿Cómo te recibieron cuando empezaste a servir? ¿Qué te habría ayudado?",
  "¿Qué podrías enseñarle tú a un servidor nuevo?"
 ],
 "activity": "Armen juntos el tablero de su grupo de servidores: lista de roles con su descripción breve, calendario de turnos del próximo mes y una lista de revisión de la credencia. Pónganlo en la sacristía.",
 "prayer": "Señor, que nos llamas a servir juntos en tu altar: haznos un equipo unido, puntual y alegre. Que nadie se sienta solo en el servicio y que cada uno descubra que su tarea, por pequeña que parezca, es parte de tu obra. Amén.",
 "resources": [{"title": "Sacrosanctum concilium", "url": SC, "note": "Número 29, sobre los ministerios litúrgicos."}],
 "comenzar": "Piensa en la última misa que serviste. Anota qué salió bien y qué se pudo haber preparado mejor antes de empezar.",
 "logros": ["Reconocer los roles del servicio del altar.", "Organizar turnos y la preparación previa.", "Acompañar a los servidores nuevos."],
 "profundizar": {"titulo": "La lista de revisión de la credencia",
  "texto": "Una lista simple evita olvidos:\n\n- Cáliz, patena y purificador.\n- Corporal y palia.\n- Vinajeras con vino y agua.\n- Lavabo, jarro y manutergio.\n- Copones con hostias suficientes.\n- Misal con las cintas puestas en las páginas del día.\n- Incensario, carbón y naveta, si corresponde."},
 "caso": {"titulo": "El domingo sin servidores",
  "texto": "Un domingo, tres de los cuatro servidores avisan a última hora que no pueden ir. El único que llega tiene 12 años y es su segunda vez. El sacerdote empieza la misa sin saber qué pasará.",
  "preguntas": ["¿Qué falló en la organización del grupo?", "¿Qué acuerdos podrían tomar para que no se repita?"]},
 "claves": [["Credencia", "Mesa lateral donde se preparan los objetos para la celebración."], ["Turno", "Fecha y rol asignados a cada servidor."], ["Padrino de servicio", "Servidor con experiencia que acompaña a uno nuevo."]],
 "lectio": {"meditar": "Muchos miembros, un solo cuerpo. ¿Qué lugar ocupas tú en el cuerpo de tu grupo?",
  "orar": "Agradece a quienes te enseñaron a servir.",
  "vivir": "Ofrécete esta semana para acompañar a un servidor nuevo o para cubrir un turno."},
 "practica": ["Hagan la lista de roles.", "Armen el calendario de turnos.", "Preparen la lista de revisión de la credencia.", "Asignen padrinos a los nuevos."],
 "idea": "En el altar nadie sirve solo: servimos como un cuerpo."
}, [
 {"q": "¿Por qué conviene repartir los roles antes de la misa?", "options": ["Para que los servidores con más experiencia tengan los roles más importantes", "Para que cada uno sepa su tarea y el servicio sea sereno", "Porque así lo exige el sacerdote"], "correct": 1, "feedback": "Cuando cada uno sabe qué hacer, no hay carreras ni improvisación."},
 {"q": "¿Qué es lo más importante al recibir a un servidor nuevo?", "options": ["Que aprenda todos los roles en su primera misa", "Acompañarlo con un padrino, empezar por roles sencillos y explicar el sentido", "Que observe durante un año antes de servir"], "correct": 1, "feedback": "Se aprende acompañado, paso a paso y entendiendo el porqué."}
])

UNIDADES["lectores-y-salmistas"] = (4, {
 "title": "La vida del lector",
 "objective": "Cultivar la espiritualidad del lector: dejar que la Palabra que proclama transforme primero su propia vida.",
 "intro": "Un buen lector no es solo alguien que lee bien en voz alta. Es alguien que conoce, reza y vive la Palabra que proclama. En esta unidad vas a mirar el ministerio del lector desde dentro: cómo prepararte espiritualmente y cómo dejar que la Escritura te cambie.",
 "sections": [
  {"title": "Primero oyente, después lector",
   "body": "Antes de prestar tu voz a la Palabra, necesitas escucharla tú. Algunas costumbres que ayudan:\n\n- **Leer el texto durante la semana,** no solo el día de la misa.\n- **Leerlo completo,** con lo que viene antes y después, para entender de qué se trata.\n- **Preguntarte:** ¿qué dice el texto?, ¿qué me dice a mí?, ¿qué le digo yo a Dios?\n- **Quedarte con una frase** que te acompañe durante el día.\n\nQuien ha rezado el texto lo proclama distinto: se nota."},
  {"title": "Coherencia sin perfección",
   "body": "La comunidad ve a quien sube al ambón. Eso no exige ser perfecto, pero sí intentar vivir lo que se proclama:\n\n- **Participar en la misa entera,** no solo en tu momento.\n- **Cuidar el trato** con los demás antes y después de la celebración.\n- **Confesarte y rezar** con regularidad.\n- **Servir también fuera del templo.**\n\nTodos somos pecadores que anuncian una Palabra más grande que nosotros. La coherencia es un camino, no un requisito de entrada."},
  {"title": "Formarse siempre",
   "body": "El lector crece cuando conoce mejor la Biblia y la liturgia:\n\n- **Conocer el leccionario:** el ciclo A, B o C de los domingos y el ciclo par o impar de los días de semana.\n- **Usar un buen comentario** o la introducción de tu Biblia para entender el contexto.\n- **Participar en las formaciones** de la parroquia o del decanato.\n- **Pedir retroalimentación** a alguien de confianza sobre tu forma de proclamar."},
  {"title": "Un ministerio para toda la comunidad",
   "body": "Desde 2021, el ministerio instituido de lector puede ser conferido también a mujeres. Pero más allá de la institución formal, todo laico que lee en la misa ejerce un servicio verdadero.\n\nEse servicio no termina en la celebración: el lector puede animar grupos de lectura de la Biblia, ayudar a preparar las lecturas con niños o acompañar a nuevos lectores."}
 ],
 "bible": {"ref": "Lucas 4,16-21 · Jesús lee en la sinagoga de Nazaret",
  "comment": "Jesús se pone de pie, recibe el rollo, lee el pasaje de Isaías y dice: «Hoy se ha cumplido esta Escritura que acaban de oír». La Palabra que proclama se hace realidad en Él. Todo lector está llamado a algo parecido: que lo que lee se vaya cumpliendo, poco a poco, en su propia vida."},
 "church": [
  {"source": "Verbum Domini 58", "text": "Los lectores deben estar realmente preparados: con formación bíblica y litúrgica, y también con preparación técnica para proclamar.", "url": VD},
  {"source": "Dei Verbum 25", "text": "Se invita a todos los fieles a la lectura asidua de la Escritura, acompañada de la oración, para que se establezca un diálogo entre Dios y el ser humano.", "url": DV}
 ],
 "questions": [
  "¿Cuándo preparas normalmente la lectura que vas a proclamar?",
  "¿Alguna lectura que proclamaste te tocó personalmente? ¿Cuál?",
  "¿Qué te ayudaría a formarte más como lector?",
  "¿Cómo podrías servir con la Palabra fuera de la misa?"
 ],
 "activity": "Cada participante elige la lectura del próximo domingo, la reza con las tres preguntas (qué dice, qué me dice, qué le digo) y comparte en el grupo la frase que lo acompañó durante la semana.",
 "prayer": "Señor, que te hiciste Palabra para nosotros: antes de prestarte mi voz, quiero prestarte mi oído y mi corazón. Que lo que proclamo se vaya cumpliendo en mi vida, y que mi comunidad escuche en mi voz tu voz. Amén.",
 "resources": [{"title": "Verbum Domini (Benedicto XVI, 2010)", "url": VD, "note": "Número 58, sobre la preparación de los lectores."}],
 "comenzar": "Recuerda la última vez que leíste en misa. ¿Cuánto tiempo antes leíste el texto por primera vez?",
 "logros": ["Preparar la lectura también con la oración.", "Vivir el ministerio con coherencia, sin exigir perfección.", "Buscar formación permanente como lector."],
 "profundizar": {"titulo": "Las lecturas de la semana",
  "texto": "Una práctica sencilla para el grupo de lectores: reunirse 30 minutos durante la semana, leer en voz alta las lecturas del domingo, compartir una frase cada uno y ensayar la proclamación. Así la preparación técnica y la espiritual van juntas."},
 "caso": {"titulo": "El lector de siempre",
  "texto": "En la parroquia, el mismo joven lee todos los domingos desde hace tres años. Lo hace bien, pero llega justo a la hora, lee y se va antes del final. Algunos jóvenes quieren leer y no se atreven a pedirlo.",
  "preguntas": ["¿Qué le dirías a ese lector?", "¿Cómo podría el grupo abrir espacio a nuevos lectores?"]},
 "claves": [["Lector instituido", "Laico que recibe de manera estable el ministerio de lector."], ["Leccionario", "Libro que ordena las lecturas de la misa por ciclos."], ["Ambón", "Lugar desde donde se proclama la Palabra."]],
 "lectio": {"meditar": "«Hoy se ha cumplido esta Escritura». ¿Qué Palabra está esperando cumplirse en tu vida?",
  "orar": "Pide a Dios un corazón que escuche antes de hablar.",
  "vivir": "Lee esta semana las lecturas del domingo tres veces: lunes, miércoles y sábado."},
 "practica": ["Elijan la lectura del domingo.", "Récenla con las tres preguntas.", "Compartan una frase.", "Ensayen la proclamación."],
 "idea": "Se proclama bien lo que primero se ha escuchado."
}, [
 {"q": "¿Qué distingue al lector que reza el texto antes de proclamarlo?", "options": ["Que lo lee más rápido", "Que lo proclama con sentido, porque primero lo escuchó", "Que no necesita ensayar"], "correct": 1, "feedback": "La preparación espiritual se nota en la proclamación."},
 {"q": "¿Qué pide la Iglesia sobre la coherencia del lector?", "options": ["Ser perfecto antes de leer", "Intentar vivir lo que proclama, como un camino", "Solo leer bien"], "correct": 1, "feedback": "La coherencia es un camino, no un requisito de perfección."}
])

UNIDADES["musica-liturgica"] = (2, {
 "title": "Cantar los tiempos y las fiestas",
 "objective": "Adaptar la música al año litúrgico y a las celebraciones especiales, para que el canto ayude a vivir cada tiempo.",
 "intro": "La Iglesia no celebra siempre lo mismo: tiene tiempos de espera, de alegría, de conversión y de fiesta. La música es una de las formas más claras de hacer sentir ese ritmo. En esta unidad vas a aprender a elegir y preparar el canto según el tiempo litúrgico y según la celebración.",
 "sections": [
  {"title": "El año litúrgico en música",
   "body": "- **Adviento:** espera sobria y alegre. Cantos de esperanza, instrumentos más sencillos.\n- **Navidad:** fiesta. Villancicos litúrgicos, canto más pleno.\n- **Cuaresma:** conversión y austeridad. No se canta el Aleluya ni el Gloria (salvo en solemnidades y fiestas); el acompañamiento instrumental se modera.\n- **Semana Santa:** el corazón del año. Cada día tiene su carácter: la entrada en Jerusalén, la Cena, la Pasión, el silencio y la Vigilia.\n- **Pascua:** cincuenta días de alegría. Vuelve el Aleluya con fuerza.\n- **Tiempo ordinario:** crecer en la vida cristiana. Variedad, pero sin perder el sentido de cada momento."},
  {"title": "Sacramentos y celebraciones especiales",
   "body": "- **Bautismos:** cantos sencillos que la familia pueda cantar; aclamaciones breves.\n- **Primeras comuniones y confirmaciones:** cantos que los niños o jóvenes conozcan y hayan ensayado.\n- **Matrimonios:** acompañar la celebración, no convertirla en un concierto. Las canciones románticas no litúrgicas no reemplazan los cantos de la misa.\n- **Funerales:** cantos de esperanza en la resurrección, con delicadeza y sobriedad."},
  {"title": "Fiestas de la comunidad",
   "body": "Cada comunidad tiene sus fiestas: el patrono, el Mes de María, las fiestas religiosas populares. Ahí la música tradicional tiene un lugar especial.\n\n- **Rescatar los cantos de la tradición** que la gente conoce y quiere.\n- **Integrar la religiosidad popular** sin desplazar las partes propias de la misa.\n- **Preguntar a los mayores** qué se cantaba antes: es una forma de cuidar la memoria de la comunidad."},
  {"title": "Planificar con tiempo",
   "body": "Un coro que planifica sirve mejor:\n\n- **Calendario anual** con los tiempos y las fiestas marcadas.\n- **Repertorio base por tiempo:** unos pocos cantos por tiempo, bien aprendidos.\n- **Ensayos especiales** para Semana Santa, Navidad y la fiesta patronal, con varias semanas de anticipación.\n- **Coordinación con el párroco** para las celebraciones de sacramentos."}
 ],
 "bible": {"ref": "Eclesiastés 3,1-8 · Hay un tiempo para cada cosa",
  "comment": "«Un tiempo para llorar y un tiempo para reír, un tiempo para lamentarse y un tiempo para bailar». La Escritura reconoce que la vida tiene ritmos. La liturgia también, y la música ayuda a la comunidad a entrar en cada uno de ellos."},
 "church": [
  {"source": "Sacrosanctum concilium 102", "text": "La Iglesia celebra a lo largo del año todo el misterio de Cristo, desde la Encarnación hasta Pentecostés y la espera de su venida.", "url": SC},
  {"source": "Ordenación General del Misal Romano 39-41", "text": "Se debe dar gran importancia al canto en la celebración, según la índole de cada pueblo y de cada asamblea.", "url": OGMR}
 ],
 "questions": [
  "¿Tu comunidad nota la diferencia entre la música de Cuaresma y la de Pascua?",
  "¿Qué cantos de la tradición de tu parroquia te gustaría rescatar?",
  "¿Cómo se prepara hoy la música de Semana Santa en tu comunidad?",
  "¿Qué celebración especial te ha costado más acompañar con la música?"
 ],
 "activity": "Armen el calendario musical del próximo trimestre: tiempos litúrgicos, fiestas y sacramentos previstos, con dos o tres cantos posibles para cada uno y las fechas de ensayo.",
 "prayer": "Señor del tiempo y de la historia: enséñanos a cantar contigo la espera, la alegría, la conversión y la fiesta. Que nuestra música ayude a tu pueblo a vivir cada tiempo con el corazón abierto. Amén.",
 "resources": [{"title": "Sacrosanctum concilium", "url": SC, "note": "Capítulo V, sobre el año litúrgico."}],
 "comenzar": "Escribe un canto que asocias a Navidad, uno a Cuaresma y uno a Pascua. ¿Qué tiene cada uno que lo hace propio de ese tiempo?",
 "logros": ["Distinguir el carácter musical de cada tiempo litúrgico.", "Acompañar sacramentos y fiestas con criterio.", "Planificar el repertorio del año."],
 "profundizar": {"titulo": "Cuaresma: el valor de quitar",
  "texto": "En Cuaresma la liturgia «quita» cosas: el Aleluya, el Gloria, las flores, parte del acompañamiento instrumental. Ese despojo prepara la explosión de la Vigilia Pascual, cuando todo vuelve. Si en Cuaresma se canta igual que siempre, la Pascua pierde fuerza."},
 "caso": {"titulo": "La canción de los novios",
  "texto": "Una pareja pide que en su matrimonio, durante la comunión, se cante la canción romántica de moda. El coro no sabe qué responder.",
  "preguntas": ["¿Qué criterios ayudan a responder?", "¿Qué alternativa podrían ofrecer a los novios?"]},
 "claves": [["Año litúrgico", "Ciclo anual en que la Iglesia celebra el misterio de Cristo."], ["Tiempo fuerte", "Adviento, Navidad, Cuaresma y Pascua."], ["Repertorio base", "Conjunto de cantos bien aprendidos para cada tiempo."]],
 "lectio": {"meditar": "Hay un tiempo para cada cosa. ¿En qué tiempo está hoy tu vida?",
  "orar": "Agradece por las fiestas de tu comunidad.",
  "vivir": "Escucha esta semana un canto propio del tiempo litúrgico actual y reza con él."},
 "practica": ["Marquen los tiempos y fiestas del trimestre.", "Elijan dos o tres cantos por fecha.", "Fijen los ensayos.", "Compártanlo con el párroco."],
 "idea": "La música ayuda a la comunidad a vivir cada tiempo."
}, [
 {"q": "¿Qué cambia en la música durante la Cuaresma?", "options": ["Nada, se canta igual", "No se canta el Aleluya y el acompañamiento se modera", "Se canta solo en latín"], "correct": 1, "feedback": "La austeridad de la Cuaresma prepara la alegría de la Pascua."},
 {"q": "¿Cuál es un buen criterio para la música de un matrimonio?", "options": ["Cantar las canciones favoritas de los novios", "Acompañar la celebración con cantos litúrgicos, sin convertirla en un concierto", "No cantar nada"], "correct": 1, "feedback": "El canto sirve a la celebración, también en los sacramentos."}
])

UNIDADES["conocer-la-biblia"] = (4, {
 "title": "Compartir la Palabra en grupo",
 "objective": "Aprender un método sencillo para leer y compartir la Biblia en grupo, de modo que la Palabra ilumine la vida de todos.",
 "intro": "La Biblia se puede leer a solas, pero nació para ser escuchada en comunidad. Cuando un grupo comparte la Palabra, cada uno descubre cosas que solo no habría visto. En esta unidad vas a aprender a guiar un momento de Palabra compartida en tu grupo.",
 "sections": [
  {"title": "Por qué leer juntos",
   "body": "- **La Biblia es el libro de una comunidad:** el pueblo de Israel y la Iglesia la escucharon, la rezaron y la transmitieron juntos.\n- **Cada uno aporta su mirada:** lo que a ti te pasa inadvertido, a otro le toca el corazón.\n- **Nos protege de interpretaciones raras:** el grupo, la tradición y los pastores ayudan a leer bien.\n- **Crea comunidad:** compartir la Palabra es compartir la vida."},
  {"title": "Un método en siete pasos",
   "body": "Un esquema sencillo, inspirado en las comunidades cristianas de muchos lugares:\n\n1. **Invocar al Espíritu Santo** con una oración o un canto breve.\n2. **Leer el texto** en voz alta, despacio.\n3. **Repetir en voz alta** una palabra o frase que llamó la atención, sin comentarla.\n4. **Silencio** de unos minutos para dejar resonar el texto.\n5. **Compartir** qué me dice el texto a mí, hoy.\n6. **Comprometerse:** ¿qué nos pide Dios esta semana?\n7. **Orar juntos** con lo que surgió."},
  {"title": "El rol de quien anima",
   "body": "Quien guía el momento no da una charla. Su tarea es:\n\n- **Elegir un texto breve,** de preferencia el evangelio del domingo.\n- **Cuidar los tiempos** para que todos puedan hablar.\n- **Hablar en primera persona** y ayudar a que los demás también lo hagan: «a mí me dice…».\n- **No corregir ni discutir** lo que otro comparte de su vida.\n- **Aclarar con humildad** si alguien interpreta algo de forma muy alejada del texto, y buscar ayuda si no sabe responder."},
  {"title": "Errores frecuentes",
   "body": "- **Convertirlo en debate** sobre temas polémicos.\n- **Que hable siempre el mismo.**\n- **Saltarse el silencio** por miedo a que sea incómodo.\n- **Quedarse en ideas** sin llegar a la vida concreta.\n- **Usar textos muy largos o difíciles** para empezar."}
 ],
 "bible": {"ref": "Lucas 24,13-35 · Los discípulos de Emaús",
  "comment": "Dos discípulos caminan tristes y conversan. Jesús se acerca, les explica las Escrituras y, al partir el pan, lo reconocen. Después dicen: «¿No ardía nuestro corazón mientras nos hablaba en el camino?». Compartir la Palabra en grupo es caminar juntos dejando que Jesús nos explique la vida."},
 "church": [
  {"source": "Verbum Domini 86-87", "text": "La lectura orante de la Escritura, personal y comunitaria, es un camino privilegiado para el encuentro con Cristo.", "url": VD},
  {"source": "Dei Verbum 25", "text": "La lectura de la Escritura debe ir acompañada de la oración, para que se establezca un diálogo entre Dios y el ser humano.", "url": DV}
 ],
 "questions": [
  "¿Has compartido alguna vez la Palabra en grupo? ¿Cómo fue?",
  "¿Qué te cuesta más: hablar de lo que te dice el texto o escuchar a otros?",
  "¿Qué texto del evangelio te gustaría compartir con tu grupo?",
  "¿Qué compromiso concreto podría surgir de un momento de Palabra compartida?"
 ],
 "activity": "Por parejas o tríos, preparen y guíen un momento de Palabra compartida de 20 minutos con el evangelio del próximo domingo, usando los siete pasos. Al final, el grupo comenta qué funcionó.",
 "prayer": "Señor Jesús, que caminaste con los discípulos de Emaús y les explicaste las Escrituras: camina también con nosotros. Que al compartir tu Palabra arda nuestro corazón y te reconozcamos en medio del grupo. Amén.",
 "resources": [{"title": "Verbum Domini (Benedicto XVI, 2010)", "url": VD, "note": "Números 86-87, sobre la lectura orante."}],
 "comenzar": "Piensa en una frase de la Biblia que alguien te compartió alguna vez y que te quedó dando vueltas. ¿Quién te la compartió?",
 "logros": ["Valorar la lectura comunitaria de la Biblia.", "Guiar un momento de Palabra compartida en siete pasos.", "Evitar los errores frecuentes al animar."],
 "profundizar": {"titulo": "Textos para empezar",
  "texto": "Algunos textos breves y buenos para grupos que recién comienzan:\n\n- Marcos 10,46-52: el ciego Bartimeo.\n- Lucas 19,1-10: Zaqueo.\n- Juan 4,5-15: la samaritana.\n- Lucas 15,11-24: el hijo pródigo.\n- Mateo 14,22-33: Jesús camina sobre el agua."},
 "caso": {"titulo": "La discusión",
  "texto": "En el momento de compartir, dos jóvenes empiezan a discutir si el milagro del texto «ocurrió de verdad». El resto se queda callado y el tiempo se acaba sin que nadie haya hablado de su vida.",
  "preguntas": ["¿Qué podría haber hecho quien animaba?", "¿Dónde se puede conversar esa pregunta en otro momento?"]},
 "claves": [["Palabra compartida", "Lectura de la Biblia en grupo que lleva a la vida y a la oración."], ["Resonancia", "Palabra o frase del texto que toca a cada uno."], ["Compromiso", "Paso concreto que surge de la Palabra."]],
 "lectio": {"meditar": "¿No ardía nuestro corazón? ¿Cuándo ha ardido el tuyo al escuchar la Palabra?",
  "orar": "Pide a Jesús que camine con tu grupo.",
  "vivir": "Comparte esta semana con alguien una frase del evangelio del domingo."},
 "practica": ["Elijan el texto.", "Preparen los siete pasos.", "Guíen el momento.", "Evalúen juntos."],
 "idea": "La Palabra se entiende mejor cuando se comparte."
}, [
 {"q": "¿Cuál es la tarea de quien anima un momento de Palabra compartida?", "options": ["Dar una charla sobre el texto", "Cuidar los tiempos, invitar a hablar en primera persona y no discutir lo que otros comparten", "Corregir a quienes se equivocan"], "correct": 1, "feedback": "Quien anima facilita; no reemplaza la voz del grupo."},
 {"q": "¿Por qué es importante el silencio después de leer?", "options": ["Para descansar", "Para dejar que el texto resuene antes de compartir", "Porque no hay nada que decir"], "correct": 1, "feedback": "El silencio deja que la Palabra llegue al corazón."}
])

UNIDADES["santos-jovenes"] = (3, {
 "title": "Santos de nuestra tierra y de la vida cotidiana",
 "objective": "Conocer a tres jóvenes que vivieron la santidad en contextos distintos y descubrir qué tienen que decir a tu propia vida.",
 "intro": "La santidad no tiene un solo molde. Un joven mapuche de la Patagonia, un estudiante del oratorio de Don Bosco y una universitaria italiana de los años ochenta vivieron el Evangelio de maneras muy diferentes. En esta unidad vas a conocer sus historias y a preguntarte qué camino te muestran.",
 "sections": [
  {"title": "Beato Ceferino Namuncurá (1886-1905)",
   "body": "Hijo del cacique mapuche Manuel Namuncurá, nació en Chimpay, en la Patagonia argentina. Pidió estudiar para ayudar a su pueblo y fue acogido por los salesianos en Buenos Aires. Allí descubrió la fe con profundidad y sintió el llamado a ser sacerdote para servir a su gente.\n\nViajó a Italia para continuar sus estudios, pero enfermó de tuberculosis y murió en Roma a los 18 años. Fue beatificado en 2007. Su vida une la identidad de un pueblo originario con el Evangelio, sin renunciar a ninguno de los dos."},
  {"title": "Santo Domingo Savio (1842-1857)",
   "body": "Alumno de san Juan Bosco en el oratorio de Turín. Era un adolescente alegre, buen compañero y muy atento a los demás: separaba peleas, acompañaba a los que estaban solos y cuidaba a los enfermos. Junto a otros compañeros formó un grupo para ayudarse a vivir la fe y servir en el oratorio.\n\nSu lema fue «antes morir que pecar». Murió a los 14 años y fue canonizado en 1954. Muestra que la santidad se juega en lo cotidiano: el patio, la sala de clases y los amigos."},
  {"title": "Beata Sandra Sabattini (1961-1984)",
   "body": "Joven italiana, estudiante de medicina y miembro de la Comunidad Papa Juan XXIII, que acoge a personas con discapacidad, adicciones y en situación de calle. Desde adolescente escribió un diario espiritual y pasaba tiempo en oración cada día.\n\nEstaba de novia y soñaba con ser médica misionera en África. A los 22 años fue atropellada cuando iba a una reunión de la comunidad y murió pocos días después. Fue beatificada en 2021: es la primera joven novia declarada beata, un ejemplo de santidad en el amor de pareja y en el servicio."},
  {"title": "Tres caminos, un mismo amor",
   "body": "- **Ceferino** vivió la santidad desde su identidad y su deseo de servir a su pueblo.\n- **Domingo** la vivió en la alegría del grupo de amigos y el servicio sencillo.\n- **Sandra** la vivió en el estudio, el noviazgo y la entrega a los más pobres.\n\nNinguno hizo cosas espectaculares. Los tres vivieron su vida ordinaria con un amor extraordinario."}
 ],
 "bible": {"ref": "1 Timoteo 4,12 · Que nadie te desprecie por ser joven",
  "comment": "Pablo le dice al joven Timoteo: «Que nadie te menosprecie por ser joven; sé ejemplo para los creyentes en la palabra, la conducta, el amor, la fe y la pureza». Ceferino, Domingo y Sandra fueron ejemplo siendo muy jóvenes. La edad no es obstáculo para la santidad."},
 "church": [
  {"source": "Christus vivit 49-63", "text": "El papa Francisco presenta a varios santos jóvenes, entre ellos Domingo Savio y Ceferino Namuncurá, como ejemplos para los jóvenes de hoy.", "url": CV},
  {"source": "Gaudete et exsultate 14", "text": "Todos estamos llamados a ser santos viviendo con amor y ofreciendo el propio testimonio en las ocupaciones de cada día.", "url": GE}
 ],
 "questions": [
  "¿Con cuál de los tres te identificas más? ¿Por qué?",
  "¿Qué tiene que ver la identidad de tu pueblo o tu familia con tu fe?",
  "¿Cómo se podría vivir la santidad en tu colegio, tu universidad o tu trabajo?",
  "¿Qué significa para ti vivir el pololeo o el noviazgo como camino de santidad?"
 ],
 "activity": "En grupos, cada uno toma a uno de los tres santos y prepara una presentación de tres minutos como si fuera una publicación para redes sociales: una frase, un dato de su vida y una pregunta para quien la lea.",
 "prayer": "Señor, que llamaste a Ceferino, a Domingo y a Sandra a ser santos en su vida de cada día: ayúdame a descubrir que mi vida ordinaria también puede ser camino hacia ti. Que nadie me desprecie por ser joven, y que yo no me desprecie tampoco. Amén.",
 "resources": [{"title": "Christus vivit (Francisco, 2019)", "url": CV, "note": "Números 49-63, sobre jóvenes santos."}],
 "comenzar": "Escribe tres lugares donde pasas la mayor parte de tu semana. Esos son tus lugares de santidad.",
 "logros": ["Conocer la vida de tres jóvenes santos de contextos distintos.", "Reconocer la santidad en la vida cotidiana.", "Relacionar su ejemplo con la propia vida."],
 "profundizar": {"titulo": "El diario de Sandra",
  "texto": "Sandra escribió desde los diez años un diario espiritual. Allí anotaba sus oraciones, dudas y propósitos. Escribir lo que vivimos con Dios ayuda a reconocer su paso por nuestra vida. Tu bitácora en esta plataforma puede ser algo parecido."},
 "caso": {"titulo": "«Eso era antes»",
  "texto": "En el grupo, un joven dice: «Los santos eran de otra época. Hoy nadie puede vivir así». Otra joven le responde que Sandra Sabattini murió en 1984, cuando sus papás eran adolescentes.",
  "preguntas": ["¿Qué responderías tú?", "¿Conoces a alguien hoy que viva el Evangelio de forma admirable?"]},
 "claves": [["Beato", "Persona declarada por la Iglesia como modelo de vida cristiana, con culto en lugares determinados."], ["Santo", "Persona canonizada, propuesta como modelo para toda la Iglesia."], ["Santidad cotidiana", "Vivir con amor las tareas de cada día."]],
 "lectio": {"meditar": "Sé ejemplo siendo joven. ¿En qué podrías ser ejemplo hoy?",
  "orar": "Pide la intercesión del santo que más te tocó.",
  "vivir": "Haz esta semana un gesto concreto de servicio en uno de tus tres lugares."},
 "practica": ["Elijan un santo por grupo.", "Preparen la publicación.", "Preséntenla.", "Compartan qué les enseñó."],
 "idea": "La santidad se vive en lo ordinario, con un amor extraordinario."
}, [
 {"q": "¿Qué tienen en común Ceferino, Domingo y Sandra?", "options": ["Hicieron milagros espectaculares", "Vivieron su vida ordinaria con un amor extraordinario", "Fueron todos sacerdotes"], "correct": 1, "feedback": "La santidad se juega en lo cotidiano."},
 {"q": "¿Qué muestra la vida de Ceferino Namuncurá?", "options": ["Que hay que renunciar a la propia cultura para ser santo", "Que se puede unir la identidad de un pueblo con el Evangelio", "Que solo los europeos llegan a ser santos"], "correct": 1, "feedback": "Ceferino vivió la fe sin renunciar a su identidad mapuche."}
])

UNIDADES["ayudante-de-catequesis"] = (3, {
 "title": "Las familias y la comunidad",
 "objective": "Comprender el lugar de la familia y de la comunidad en la catequesis, y aprender a acoger a las familias con sus distintas realidades.",
 "intro": "La catequesis no ocurre solo en la sala del encuentro. Los niños y jóvenes llegan desde una familia y van hacia una comunidad. En esta unidad vas a mirar cómo involucrar a las familias, cómo acogerlas sin juzgar y cómo conectar la catequesis con la vida de la parroquia.",
 "sections": [
  {"title": "La familia, primera escuela de la fe",
   "body": "Los padres y quienes crían son los primeros educadores en la fe. La catequesis no los reemplaza: los acompaña. Por eso:\n\n- **Lo que pasa en casa pesa más** que lo que pasa en una hora de encuentro.\n- **Un niño aprende a rezar** viendo rezar a los suyos.\n- **La catequesis funciona mejor** cuando la familia sabe qué se está viviendo y puede continuarlo en casa."},
  {"title": "Familias muy distintas",
   "body": "Las familias que llegan a la catequesis son muy diversas: con ambos padres, con uno solo, con abuelos a cargo, separadas, con nuevas parejas, con mucha fe o con muy poca.\n\nComo ayudante:\n\n- **Acoge a todos sin juzgar.** No preguntes ni comentes la situación familiar de un niño.\n- **Usa un lenguaje inclusivo:** «tu familia», «quienes te cuidan», en vez de suponer siempre «tu papá y tu mamá».\n- **Cuida a los niños** cuando una actividad toque temas familiares que puedan doler.\n- **Si notas algo que te preocupa,** conversa con el catequista responsable; no lo resuelvas solo."},
  {"title": "Involucrar a las familias",
   "body": "Algunas ideas sencillas:\n\n- **Una tarea para hacer en casa** que requiera conversar con la familia.\n- **Encuentros de familias** algunas veces al año.\n- **Invitar a las familias** a la misa en que participan los niños.\n- **Un mensaje breve** después de cada encuentro, a través del catequista, contando qué se vivió.\n\nSiempre a través del catequista responsable y con los canales que la parroquia defina."},
  {"title": "Conectar con la comunidad",
   "body": "La catequesis prepara para vivir en comunidad, no solo para recibir un sacramento. Ayuda a que los niños y jóvenes:\n\n- **Conozcan la parroquia:** el templo, el párroco, los grupos.\n- **Participen en la misa** del domingo, no solo en las de su grupo.\n- **Descubran los grupos** a los que podrían integrarse después: infancia misionera, grupos juveniles, coros, servidores del altar."}
 ],
 "bible": {"ref": "Deuteronomio 6,4-9 · Enseñarás estas palabras a tus hijos",
  "comment": "«Escucha, Israel… Grábate en el corazón estas palabras que hoy te mando; repíteselas a tus hijos, háblales de ellas cuando estés en casa y cuando vayas de viaje». La fe se transmitía en la vida diaria de la familia. La catequesis ayuda a que eso siga ocurriendo hoy."},
 "church": [
  {"source": "Catecismo de la Iglesia Católica 2221-2226", "text": "Los padres tienen la primera responsabilidad en la educación de sus hijos, también en la fe; la familia es como una iglesia doméstica.", "url": CEC_FAM},
  {"source": "Directorio para la Catequesis (2020)", "text": "La familia es sujeto activo de la catequesis, y la comunidad cristiana debe acompañarla en su tarea de transmitir la fe."}
 ],
 "questions": [
  "¿Quién te enseñó a rezar a ti?",
  "¿Qué realidades familiares conoces en tu grupo de catequesis, sin dar nombres?",
  "¿Qué expresiones podrían hacer sentir excluido a un niño?",
  "¿Cómo podría tu grupo de catequesis conectarse más con la parroquia?"
 ],
 "activity": "Diseñen una tarea para la casa que invite a cada niño o joven a conversar con su familia sobre el tema del próximo encuentro. Revisen que sirva para cualquier tipo de familia.",
 "prayer": "Señor, que creciste en la familia de Nazaret: bendice a todas las familias de nuestros niños y jóvenes, con sus alegrías y sus heridas. Haznos capaces de acogerlas sin juzgar y de ayudarles a transmitir la fe en su casa. Amén.",
 "resources": [{"title": "Catecismo de la Iglesia Católica", "url": CEC_FAM, "note": "Números 2221-2226, sobre los deberes de los padres."}],
 "comenzar": "Recuerda un momento de fe que viviste con tu familia cuando eras niño. ¿Qué lo hizo especial?",
 "logros": ["Reconocer a la familia como primera educadora de la fe.", "Acoger a familias diversas sin juzgar.", "Involucrar a las familias y conectar con la comunidad."],
 "profundizar": {"titulo": "Lo que no corresponde al ayudante",
  "texto": "El ayudante no debe: pedir datos personales a las familias, comunicarse con ellas por su cuenta sin acuerdo del catequista, ni compartir información de los niños fuera del grupo. Todo contacto con las familias se hace por los canales definidos por la parroquia."},
 "caso": {"titulo": "El Día del Padre",
  "texto": "Para el Día del Padre, el catequista propone que cada niño haga una tarjeta para su papá. Una niña se queda quieta y luego dice en voz baja que su papá no vive con ella.",
  "preguntas": ["¿Cómo podrías haber evitado esta situación?", "¿Qué harías en ese momento?"]},
 "claves": [["Iglesia doméstica", "La familia como primer lugar donde se vive y transmite la fe."], ["Acogida", "Recibir a cada familia sin juicios."], ["Comunidad", "La parroquia y sus grupos, donde la fe se sigue viviendo."]],
 "lectio": {"meditar": "Repíteselas a tus hijos. ¿Qué palabras de fe te repitieron a ti?",
  "orar": "Reza por las familias de tu grupo de catequesis.",
  "vivir": "Agradece esta semana a alguien de tu familia por la fe que te transmitió."},
 "practica": ["Diseñen la tarea para la casa.", "Revisen que sirva para cualquier familia.", "Preséntenla al catequista.", "Úsenla en el próximo encuentro."],
 "idea": "La catequesis acompaña a la familia; no la reemplaza."
}, [
 {"q": "¿Quiénes son los primeros educadores en la fe?", "options": ["Los catequistas", "Los padres y quienes crían", "Los sacerdotes"], "correct": 1, "feedback": "La catequesis acompaña a la familia, no la reemplaza."},
 {"q": "Si notas algo preocupante en la situación de un niño, ¿qué haces?", "options": ["Lo resuelves tú directamente con la familia", "Lo conversas con el catequista responsable", "No haces nada"], "correct": 1, "feedback": "El ayudante no actúa solo: informa al catequista responsable."}
])
