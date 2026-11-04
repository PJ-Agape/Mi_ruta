"""Quinta unidad de las formaciones complementarias (lote B: misión, cuidado y herramientas)."""
VAT = "https://www.vatican.va/"
CV = VAT + "content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20190325_christus-vivit.html"
EG = VAT + "content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20131124_evangelii-gaudium.html"
GE = VAT + "content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20180319_gaudete-et-exsultate.html"
LS = VAT + "content/francesco/es/encyclicals/documents/papa-francesco_20150524_enciclica-laudato-si.html"
DCE = VAT + "content/benedict-xvi/es/encyclicals/documents/hf_ben-xvi_enc_20051225_deus-caritas-est.html"
IM = VAT + "archive/hist_councils/ii_vatican_council/documents/vat-ii_decree_19631204_inter-mirifica_sp.html"
GS = VAT + "archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19651207_gaudium-et-spes_sp.html"
CEC_5 = VAT + "archive/catechism_sp/p3s2c2a5_sp.html"
ISE = "https://www.iglesia.cl/prevenirabusos/ise/"

UNIDADES = {}

UNIDADES["misiones-juveniles"] = (2, {
 "title": "Anunciar a Jesús",
 "objective": "Aprender a compartir la fe de forma sencilla y respetuosa: el primer anuncio, el testimonio personal y la oración con otros.",
 "intro": "En la misión vas a golpear puertas y conversar con personas muy distintas. Muchas veces te preguntarán por qué estás ahí. En esta unidad vas a preparar lo más importante: cómo contar, con tus palabras, quién es Jesús para ti.",
 "sections": [
  {"title": "El primer anuncio",
   "body": "El corazón del Evangelio cabe en pocas frases. El papa Francisco lo resume para los jóvenes en tres verdades:\n\n- **Dios te ama.** Nunca lo dudes, pase lo que pase en tu vida.\n- **Cristo te salva.** Dio su vida por ti y te ofrece su perdón.\n- **Él vive.** No es un recuerdo del pasado: está presente y camina contigo.\n\nTodo lo demás (la doctrina, la moral, los sacramentos) se entiende a partir de este anuncio."},
  {"title": "Tu testimonio",
   "body": "Un testimonio no es un discurso. Es contar, en dos o tres minutos, cómo Jesús ha tocado tu vida. Una estructura simple:\n\n1. **Cómo era mi vida** antes, o en un momento difícil.\n2. **Cómo me encontré con Jesús** o cómo lo descubrí más cerca.\n3. **Qué ha cambiado** desde entonces.\n\nHabla con palabras sencillas, sin exagerar y sin dar lecciones. Lo que convence es la verdad de lo que cuentas."},
  {"title": "Con mansedumbre y respeto",
   "body": "- **Escucha primero.** Interésate por la vida de la persona antes de hablar de la tuya.\n- **No discutas** ni intentes ganar un debate.\n- **Respeta** a quien no cree, cree distinto o no quiere conversar.\n- **No prometas** cosas que no dependen de ti.\n- **Si no sabes algo,** dilo con honestidad y ofrece averiguarlo con alguien que sepa."},
  {"title": "Orar con otros",
   "body": "Muchas personas agradecen que alguien rece con ellas. Para hacerlo:\n\n- **Pregunta siempre** si quieren rezar.\n- **Reza con palabras simples,** nombrando lo que te contaron (si te dan permiso).\n- **Puedes terminar con el Padre Nuestro** o un Ave María, que muchos conocen.\n- **Deja algo:** una estampa, una oración escrita o la invitación a la capilla."}
 ],
 "bible": {"ref": "1 Pedro 3,15-16 · Dar razón de la esperanza",
  "comment": "«Estén siempre dispuestos a dar razón de su esperanza a todo el que les pida explicaciones, pero háganlo con mansedumbre y respeto». La misión no consiste en convencer a la fuerza, sino en estar preparados para contar, con sencillez, por qué Jesús es nuestra esperanza."},
 "church": [
  {"source": "Christus vivit 111-133", "text": "El gran anuncio para todos los jóvenes: Dios te ama, Cristo te salva y Él vive.", "url": CV},
  {"source": "Evangelii gaudium 164-165", "text": "El primer anuncio o kerigma debe ocupar el centro de la evangelización: el amor de Dios manifestado en Jesucristo muerto y resucitado.", "url": EG}
 ],
 "questions": [
  "¿Cómo explicarías en una frase quién es Jesús para ti?",
  "¿Qué momento de tu vida podrías contar como testimonio?",
  "¿Qué te da más miedo de hablar de tu fe con desconocidos?",
  "¿Has rezado alguna vez con alguien que no conocías? ¿Cómo fue?"
 ],
 "activity": "Cada participante escribe su testimonio en tres partes y lo cuenta en parejas en tres minutos. Después, practican cómo ofrecer una oración a alguien que les comparte una preocupación.",
 "prayer": "Señor Jesús, que me amas, me salvas y vives: dame palabras sencillas para contar lo que has hecho en mi vida. Que sepa escuchar antes de hablar y anunciarte siempre con mansedumbre y respeto. Amén.",
 "resources": [{"title": "Christus vivit (Francisco, 2019)", "url": CV, "note": "Capítulo 4: el gran anuncio para todos los jóvenes."}],
 "comenzar": "Completa esta frase sin pensarlo mucho: «Para mí, Jesús es…».",
 "logros": ["Expresar el primer anuncio con palabras propias.", "Preparar un testimonio personal breve.", "Ofrecer la oración con respeto."],
 "profundizar": {"titulo": "Preguntas que te pueden hacer",
  "texto": "En la misión aparecen preguntas como «¿por qué Dios permite el sufrimiento?» o «¿por qué debería ir a la Iglesia?». No necesitas tener todas las respuestas. Escucha, comparte lo que tú vives y, si la conversación lo pide, ofrece seguir hablando con el asesor o el sacerdote de la misión."},
 "caso": {"titulo": "La puerta que se cierra",
  "texto": "En la primera casa, un señor les dice molesto que no cree en nada y que la Iglesia le ha hecho daño. Uno de los misioneros quiere responderle con argumentos; la otra se queda callada.",
  "preguntas": ["¿Qué harías tú?", "¿Cómo se puede respetar a esa persona y, aun así, dejar una puerta abierta?"]},
 "claves": [["Kerigma", "Primer anuncio del amor de Dios en Jesucristo."], ["Testimonio", "Relato breve de lo que Dios ha hecho en la propia vida."], ["Mansedumbre", "Firmeza amable, sin agresividad."]],
 "lectio": {"meditar": "Dar razón de tu esperanza. ¿Cuál es tu esperanza hoy?",
  "orar": "Pide por las personas que encontrarás en la misión.",
  "vivir": "Comparte esta semana tu testimonio con alguien de confianza."},
 "practica": ["Escriban su testimonio.", "Cuéntenlo en parejas.", "Practiquen ofrecer una oración.", "Comenten qué les costó."],
 "idea": "Anunciar es contar con sencillez lo que Jesús ha hecho en ti."
}, [
 {"q": "¿Cuáles son las tres verdades del primer anuncio según Christus vivit?", "options": ["Dios te ama, Cristo te salva, Él vive", "Reza, ayuna, da limosna", "Ve a misa, confiésate, comulga"], "correct": 0, "feedback": "Es el corazón del Evangelio, del que se desprende todo lo demás."},
 {"q": "¿Cómo se comparte la fe en la misión?", "options": ["Ganando los debates", "Escuchando primero y hablando con mansedumbre y respeto", "Insistiendo hasta que la persona acepte"], "correct": 1, "feedback": "La misión propone, no impone."}
])

UNIDADES["voluntariado-y-doctrina-social"] = (3, {
 "title": "Dónde y cómo servir",
 "objective": "Conocer los distintos espacios de voluntariado, elegir uno con criterio y comprometerse de manera responsable y sostenida.",
 "intro": "Hay muchas formas de servir: en la parroquia, en una fundación, en el barrio o en una emergencia. Elegir bien dónde poner tus energías ayuda a que tu servicio dure y haga bien. En esta unidad vas a conocer los espacios posibles y a pensar cuál es el tuyo.",
 "sections": [
  {"title": "Espacios para servir",
   "body": "- **En la parroquia:** comedores, ollas comunes, visitas a enfermos y adultos mayores, ropero, apoyo escolar.\n- **En la Iglesia más amplia:** Cáritas, el Hogar de Cristo (fundado por san Alberto Hurtado) y muchas obras de congregaciones religiosas.\n- **En organizaciones de la sociedad civil:** fundaciones de vivienda, educación, discapacidad, migrantes o medio ambiente.\n- **En emergencias:** incendios, inundaciones o terremotos, siempre coordinados con quienes organizan la ayuda.\n- **En el barrio:** junta de vecinos, clubes deportivos, iniciativas de cuidado del entorno."},
  {"title": "Elegir con criterio",
   "body": "Algunas preguntas para discernir:\n\n- **¿Qué necesidad me conmueve?** El servicio dura más cuando nace del corazón.\n- **¿Qué sé hacer o puedo aprender?**\n- **¿Cuánto tiempo real tengo?** Mejor poco y constante que mucho al principio y nada después.\n- **¿La organización es seria?** Que tenga responsables claros, capacitación y normas de cuidado, sobre todo si trabaja con niños o personas vulnerables.\n- **¿Puedo ir con otros?** Servir en grupo sostiene el compromiso."},
  {"title": "Un compromiso responsable",
   "body": "- **Cumple lo que prometes:** horarios, turnos y avisos.\n- **Capacítate** antes de empezar.\n- **Respeta las normas** de la organización, aunque te parezcan lentas.\n- **Cuida la confidencialidad** de las personas que atiendes: no publiques fotos ni historias sin autorización.\n- **Si eres menor de edad,** conversa con tus padres y respeta las tareas que corresponden a tu edad."},
  {"title": "Servir también transforma al que sirve",
   "body": "El voluntariado no es solo dar. Quien sirve recibe: amigos nuevos, una mirada más amplia de la realidad, preguntas sobre su vocación. Muchos jóvenes descubren su profesión o su camino de vida en un voluntariado.\n\nPor eso conviene darse tiempos para **reflexionar y rezar** lo que se vive: ¿qué me está enseñando esta experiencia?, ¿dónde estoy encontrando a Dios?"}
 ],
 "bible": {"ref": "Isaías 6,8 · «Aquí estoy, envíame»",
  "comment": "Dios pregunta: «¿A quién enviaré?». E Isaías responde: «Aquí estoy, envíame». Ante las necesidades del mundo, Dios sigue haciendo la misma pregunta. Elegir dónde servir es una forma concreta de responderle."},
 "church": [
  {"source": "Deus caritas est 30", "text": "Benedicto XVI destaca el voluntariado como escuela de vida que educa a la solidaridad y a la disponibilidad para dar.", "url": DCE},
  {"source": "Christus vivit 168-174", "text": "Francisco invita a los jóvenes a ser protagonistas del cambio, comprometidos con el servicio a los demás.", "url": CV}
 ],
 "questions": [
  "¿Qué necesidad de tu barrio o ciudad te conmueve más?",
  "¿Cuánto tiempo real puedes dedicar cada semana o cada mes?",
  "¿Conoces organizaciones serias donde podrías servir?",
  "¿Qué te ha enseñado alguna experiencia de servicio?"
 ],
 "activity": "Hagan un mapa de espacios de voluntariado cercanos: parroquia, fundaciones, barrio. Para cada uno anoten qué hace, qué necesita, qué edad mínima pide y a quién contactar. Luego, cada uno elige uno para conocer en el próximo mes.",
 "prayer": "Señor, que preguntas «¿a quién enviaré?»: aquí estoy. Ayúdame a elegir bien dónde servir, a ser fiel en lo pequeño y a dejarme transformar por quienes encuentro. Que mi servicio sea constante, humilde y alegre. Amén.",
 "resources": [{"title": "Deus caritas est (Benedicto XVI, 2005)", "url": DCE, "note": "Número 30, sobre el voluntariado."}],
 "comenzar": "Escribe tres causas o necesidades que te importan. Marca la que más te mueve.",
 "logros": ["Conocer distintos espacios de voluntariado.", "Elegir un servicio con criterios claros.", "Asumir un compromiso responsable y reflexionado."],
 "profundizar": {"titulo": "Señales de una organización confiable",
  "texto": "Antes de comprometerte, revisa que la organización: tenga responsables identificados, ofrezca inducción o capacitación, cuente con normas de cuidado y prevención, sea transparente con el uso de los recursos y no te pida tareas para las que no estás preparado."},
 "caso": {"titulo": "El entusiasmo de marzo",
  "texto": "Un grupo de jóvenes se inscribe en marzo en un apoyo escolar para niños del barrio. En mayo ya van la mitad, y en julio quedan dos. Los niños preguntan por qué los demás no volvieron.",
  "preguntas": ["¿Qué pudo haber fallado?", "¿Cómo podrían haber elegido y organizado mejor su compromiso?"]},
 "claves": [["Voluntariado", "Servicio libre y gratuito a otros, de manera organizada."], ["Discernimiento", "Elegir con oración y criterio."], ["Constancia", "Mantener el compromiso en el tiempo."]],
 "lectio": {"meditar": "«Aquí estoy, envíame». ¿Estás disponible para lo que Dios te pida?",
  "orar": "Reza por las personas a las que servirás.",
  "vivir": "Contacta esta semana a una organización del mapa para conocerla."},
 "practica": ["Hagan el mapa de voluntariados.", "Completen los datos de cada uno.", "Elijan uno para conocer.", "Compartan la experiencia en el próximo encuentro."],
 "idea": "Mejor un servicio pequeño y constante que uno grande que no dura."
}, [
 {"q": "¿Qué conviene al elegir un voluntariado?", "options": ["Comprometerse con todo lo posible al principio", "Ser realista con el tiempo disponible y preferir la constancia", "Elegir lo que eligen los amigos"], "correct": 1, "feedback": "Un compromiso pequeño y constante hace más bien que uno grande que se abandona."},
 {"q": "¿Qué señal indica que una organización es confiable?", "options": ["Que no pide capacitación", "Que tiene responsables claros y normas de cuidado", "Que acepta a cualquiera para cualquier tarea"], "correct": 1, "feedback": "La seriedad protege a las personas atendidas y a los voluntarios."}
])

UNIDADES["ecologia-integral"] = (2, {
 "title": "Ecología de la vida cotidiana",
 "objective": "Descubrir que la ecología integral empieza en los espacios de cada día: el cuerpo, la casa, el barrio y las relaciones.",
 "intro": "Cuando pensamos en ecología, pensamos en bosques, glaciares y océanos. Pero el papa Francisco también habla de una «ecología de la vida cotidiana»: cómo cuidamos nuestro cuerpo, nuestra casa, nuestro barrio y la forma en que convivimos. En esta unidad vas a mirar tu entorno más cercano.",
 "sections": [
  {"title": "El lugar donde vivimos",
   "body": "Los espacios influyen en cómo vivimos y nos relacionamos. Un barrio con plazas, árboles, luz y lugares de encuentro ayuda a convivir mejor. Uno con basura, abandono o inseguridad hace todo más difícil.\n\nPreguntas para mirar tu entorno:\n\n- **¿Hay lugares de encuentro** para niños, jóvenes y adultos mayores?\n- **¿Cómo está el aseo** de las calles y plazas?\n- **¿Qué espacios están abandonados** y podrían recuperarse?\n- **¿Quiénes están más solos** en tu barrio?"},
  {"title": "Ecología humana",
   "body": "Cuidar la creación incluye cuidar el propio cuerpo y aceptarlo como un regalo. También incluye respetar el cuerpo de los demás.\n\n- **Descanso, alimentación y movimiento:** el cuerpo también es casa común.\n- **Aceptar el propio cuerpo,** sin compararse con modelos imposibles de las redes.\n- **Cuidar el cuerpo de otros:** no burlarse, no exponer, no dañar."},
  {"title": "Relaciones que cuidan",
   "body": "La ecología integral también es social. Un barrio sano es uno donde:\n\n- **Los vecinos se conocen** y se saludan.\n- **Se cuida a los más frágiles:** adultos mayores solos, personas con discapacidad, familias migrantes.\n- **Los conflictos se conversan** antes de que crezcan.\n- **Hay lugar para los jóvenes,** que no son vistos como un problema sino como una fuerza."},
  {"title": "Pequeñas acciones en tu entorno",
   "body": "- **Adoptar un espacio:** una plaza, una jardinera, el patio de la parroquia.\n- **Organizar una jornada de limpieza** con los vecinos.\n- **Visitar a un adulto mayor** que vive solo.\n- **Crear un punto de reciclaje** en la parroquia o el colegio.\n- **Recuperar un lugar de encuentro:** pintar, plantar, iluminar."}
 ],
 "bible": {"ref": "Jeremías 29,5-7 · Busquen el bien de la ciudad",
  "comment": "A los israelitas desterrados en Babilonia, Dios les dice: «Construyan casas, planten huertos… busquen el bien de la ciudad adonde los desterré y rueguen por ella al Señor, porque de su bien dependerá el de ustedes». Cuidar el lugar donde vivimos es parte de nuestra fe."},
 "church": [
  {"source": "Laudato si' 147-148", "text": "Los espacios donde vivimos influyen en nuestra manera de ver la vida, sentir y actuar; hace falta cuidar los lugares comunes y los vínculos que los hacen habitables.", "url": LS},
  {"source": "Laudato si' 155", "text": "La ecología humana implica aceptar el propio cuerpo como don de Dios y cuidarlo, reconociendo también al otro en su diferencia.", "url": LS}
 ],
 "questions": [
  "¿Qué lugar de tu barrio te gusta más? ¿Por qué?",
  "¿Qué espacio cercano está descuidado y podría recuperarse?",
  "¿Cómo te relacionas con tu propio cuerpo? ¿Lo cuidas?",
  "¿Quién en tu barrio podría necesitar compañía?"
 ],
 "activity": "Hagan un recorrido por el entorno de la parroquia o del lugar de encuentro. Anoten lo que encuentran: espacios descuidados, lugares de encuentro, personas que podrían necesitar algo. Elijan una acción pequeña para hacer en el próximo mes.",
 "prayer": "Señor, que nos pides buscar el bien de la ciudad: abre nuestros ojos para ver el barrio donde vivimos. Ayúdanos a cuidar los espacios comunes, nuestro cuerpo y a las personas que están más solas. Que nuestra fe se note en el lugar donde vivimos. Amén.",
 "resources": [{"title": "Laudato si' (Francisco, 2015)", "url": LS, "note": "Números 147-155, sobre la ecología de la vida cotidiana."}],
 "comenzar": "Dibuja un mapa simple de tu barrio con tres lugares que usas cada semana.",
 "logros": ["Mirar el entorno cercano desde la ecología integral.", "Reconocer el cuidado del cuerpo como parte de la ecología humana.", "Proponer acciones concretas en el barrio."],
 "profundizar": {"titulo": "Pedir permiso y sumar a otros",
  "texto": "Antes de intervenir un espacio público, conversen con la junta de vecinos o la municipalidad. Muchas municipalidades apoyan con herramientas, plantas o retiro de basura. Sumar a los vecinos hace que el cuidado dure más que una jornada."},
 "caso": {"titulo": "La plaza de los columpios rotos",
  "texto": "Frente a la capilla hay una plaza con columpios rotos y basura. Los niños ya no van y los adultos dicen que es peligrosa. El grupo juvenil se pregunta si es su problema.",
  "preguntas": ["¿Es tarea del grupo hacer algo?", "¿Qué primer paso podrían dar?"]},
 "claves": [["Ecología de la vida cotidiana", "Cuidado de los espacios y relaciones de cada día."], ["Ecología humana", "Cuidado del propio cuerpo y respeto por el de los demás."], ["Bien común", "Condiciones que permiten a todos vivir mejor."]],
 "lectio": {"meditar": "Busquen el bien de la ciudad. ¿Qué bien necesita tu barrio?",
  "orar": "Reza por tus vecinos, uno por uno si puedes.",
  "vivir": "Saluda esta semana a un vecino con el que nunca has hablado."},
 "practica": ["Hagan el recorrido.", "Anoten lo que encuentran.", "Elijan una acción.", "Planifiquen el primer paso."],
 "idea": "La casa común empieza en la puerta de tu casa."
}, [
 {"q": "¿Qué es la ecología de la vida cotidiana?", "options": ["Solo reciclar", "El cuidado de los espacios, el cuerpo y las relaciones de cada día", "Algo que solo hacen los expertos"], "correct": 1, "feedback": "La ecología integral empieza en lo cercano."},
 {"q": "Según Laudato si', la ecología humana incluye:", "options": ["Aceptar y cuidar el propio cuerpo como un don", "Solo cuidar a los animales", "Vivir lejos de las ciudades"], "correct": 0, "feedback": "Cuidar la creación incluye cuidar nuestro cuerpo y el de los demás."}
])

UNIDADES["buen-trato-y-prevencion"] = (3, {
 "title": "Reparar y acompañar",
 "objective": "Comprender cómo una comunidad acompaña después de una situación de daño: a quienes fueron dañados, al grupo y a quienes sirven.",
 "intro": "Prevenir es lo primero. Pero cuando ocurre un daño, la manera en que la comunidad responde puede sanar o volver a herir. En esta unidad vas a conocer qué significa acompañar y reparar, y cuál es tu lugar como joven que sirve, sin asumir tareas que corresponden a adultos y especialistas.",
 "sections": [
  {"title": "Lo que vive una persona dañada",
   "body": "Quien ha sufrido un daño puede sentir vergüenza, culpa, miedo, rabia o confusión. A veces tarda años en hablar. Por eso:\n\n- **Creerle y no juzgar** es el primer paso.\n- **Nunca culparla** ni preguntar por qué no habló antes.\n- **Respetar sus tiempos** y su privacidad.\n- **No exponerla:** su historia no se comenta en el grupo ni en redes."},
  {"title": "La respuesta de la comunidad",
   "body": "Cuando hay una denuncia o una situación de daño, las orientaciones de la Iglesia en Chile piden:\n\n- **Activar los procedimientos** establecidos con el encargado de prevención y las autoridades que correspondan.\n- **Proteger a la persona afectada** antes que a la institución o a la imagen del grupo.\n- **Colaborar con la justicia** cuando hay un posible delito.\n- **Informar con prudencia** a la comunidad, sin ocultar ni difundir detalles.\n\nEstas decisiones las toman los adultos responsables. Tu tarea es avisar, acompañar y respetar."},
  {"title": "Acompañar al grupo",
   "body": "Un hecho grave afecta a todo el grupo. Puede aparecer tristeza, rabia, divisiones o deseos de abandonar. Ayuda:\n\n- **Abrir espacios para conversar** lo que sienten, guiados por adultos preparados.\n- **No alimentar rumores** ni tomar partido públicamente.\n- **Rezar juntos** por todos los afectados.\n- **Pedir apoyo profesional** cuando el grupo lo necesita."},
  {"title": "Reparar",
   "body": "Reparar no es olvidar ni dar vuelta la página rápido. Significa reconocer el daño, pedir perdón cuando corresponde, acompañar a las personas afectadas en lo que necesitan y cambiar lo que permitió que ocurriera.\n\nUna comunidad que aprende de sus heridas se vuelve más segura para todos. Esa es también una forma de anunciar el Evangelio."}
 ],
 "bible": {"ref": "Isaías 61,1-3 · Vendar los corazones heridos",
  "comment": "El profeta es enviado «a vendar los corazones heridos… a consolar a los que están de duelo». Jesús hizo suyas estas palabras. La comunidad cristiana está llamada a ser lugar de consuelo y reparación, especialmente para quienes fueron heridos dentro de ella."},
 "church": [
  {"source": "Carta al Pueblo de Dios (Francisco, 2018)", "text": "El papa pide a toda la Iglesia reconocer con vergüenza y arrepentimiento el daño causado a las víctimas y comprometerse en una cultura del cuidado."},
  {"source": "Integridad en el Servicio Eclesial (Conferencia Episcopal de Chile, 2020)", "text": "Establece los criterios de acogida a las víctimas, los procedimientos ante denuncias y el deber de colaborar con la justicia.", "url": ISE}
 ],
 "questions": [
  "¿Por qué crees que a muchas personas les cuesta contar un daño que sufrieron?",
  "¿Qué actitudes de una comunidad pueden volver a herir a una víctima?",
  "¿Qué le corresponde a un joven dirigente y qué a los adultos responsables?",
  "¿Qué significa para ti que una comunidad «aprenda de sus heridas»?"
 ],
 "activity": "Con la guía del asesor, revisen juntos qué dice el protocolo de su parroquia o diócesis sobre la acogida de víctimas y el acompañamiento de la comunidad. Anoten quién es el encargado de prevención y cómo contactarlo.",
 "prayer": "Señor, que viniste a vendar los corazones heridos: te pedimos por todas las personas que han sido dañadas, especialmente dentro de la Iglesia. Danos un corazón que crea, que acompañe y que no vuelva a herir. Haz de nuestra comunidad un lugar seguro y reparador. Amén.",
 "resources": [{"title": "Prevenir abusos: Iglesia en Chile", "url": ISE, "note": "Documento ISE y orientaciones de acogida."}],
 "comenzar": "Piensa en alguna vez que alguien te creyó cuando contaste algo difícil. ¿Qué hizo esa persona que te ayudó?",
 "logros": ["Comprender lo que vive una persona que sufrió un daño.", "Conocer cómo responde la comunidad ante una denuncia.", "Reconocer el propio rol y sus límites."],
 "profundizar": {"titulo": "Lo que no se dice",
  "texto": "Frases que vuelven a herir y que nunca deben decirse: «¿por qué no lo contaste antes?», «seguro lo malinterpretaste», «piensa en el daño que le haces al grupo», «hay que perdonar y olvidar». Ante la duda, es mejor escuchar en silencio y buscar ayuda."},
 "caso": {"titulo": "El rumor",
  "texto": "En la parroquia se comienza a comentar que hubo una denuncia contra un adulto que trabajaba con jóvenes. En el grupo de WhatsApp aparecen nombres, opiniones y defensas apasionadas.",
  "preguntas": ["¿Qué daño puede causar esta conversación?", "¿Qué deberían hacer los dirigentes del grupo?"]},
 "claves": [["Acogida", "Recibir a la persona afectada creyéndole y sin juzgar."], ["Reparación", "Reconocer el daño, acompañar y cambiar lo que lo permitió."], ["Revictimización", "Volver a dañar a una víctima con actitudes o palabras."]],
 "lectio": {"meditar": "Vendar los corazones heridos. ¿A quién podrías acompañar hoy?",
  "orar": "Reza por las víctimas de abusos y por sus familias.",
  "vivir": "Evita esta semana participar de rumores o comentarios sobre otros."},
 "practica": ["Revisen el protocolo con el asesor.", "Identifiquen al encargado de prevención.", "Anoten los canales de contacto.", "Conversen qué les corresponde como jóvenes."],
 "idea": "Una comunidad que cree, acompaña y repara se vuelve más segura para todos."
}, [
 {"q": "Si alguien te cuenta que sufrió un daño, ¿cuál es la primera actitud?", "options": ["Preguntarle por qué no habló antes", "Creerle, no juzgar y avisar a un adulto responsable", "Contarlo al grupo para que lo apoyen"], "correct": 1, "feedback": "Creer, no juzgar y activar a los adultos responsables."},
 {"q": "¿A quién protege primero la comunidad ante una denuncia?", "options": ["A la imagen del grupo", "A la persona afectada", "Al acusado"], "correct": 1, "feedback": "La persona afectada es la prioridad."}
])

UNIDADES["primeros-auxilios-psicologicos"] = (3, {
 "title": "Cuando todo el grupo vive una crisis",
 "objective": "Saber acompañar a un grupo que enfrenta una pérdida o un evento traumático colectivo, cuidando a cada persona y derivando cuando corresponde.",
 "intro": "A veces la crisis no la vive una persona sola, sino todo el grupo: la muerte de un compañero, un accidente en una actividad, un incendio o un terremoto. En esta unidad vas a aprender cómo acompañar a un grupo en esos momentos, siempre junto a los adultos responsables.",
 "sections": [
  {"title": "Crisis colectivas",
   "body": "Algunas situaciones que afectan a todo un grupo:\n\n- **La muerte** de un integrante, un dirigente o un familiar cercano.\n- **Un accidente** durante una actividad o un campamento.\n- **Desastres** como incendios forestales, inundaciones o terremotos.\n- **Hechos de violencia** en el barrio o el colegio.\n\nCada persona reacciona distinto: algunos lloran, otros se ríen nerviosos, otros se callan o se enojan. Todas son reacciones posibles ante algo que sobrepasa."},
  {"title": "Las primeras horas",
   "body": "- **Seguridad primero:** que todos estén a salvo y atendidos.\n- **Avisar a los adultos responsables** y a las familias.\n- **Mantener al grupo junto,** en un lugar tranquilo.\n- **Dar información clara y verdadera,** sin rumores ni detalles innecesarios.\n- **Atender necesidades básicas:** agua, abrigo, comida, contacto con la familia.\n- **Identificar a quienes están más afectados** para acompañarlos de cerca."},
  {"title": "Un espacio para hablar",
   "body": "En los días siguientes, puede ayudar un encuentro guiado por un adulto preparado:\n\n- **Abrir con un momento de silencio** u oración.\n- **Invitar a compartir** sin obligar a nadie.\n- **Normalizar las reacciones:** sentir pena, rabia o miedo es esperable.\n- **Hacer algo juntos:** escribir cartas, plantar algo, preparar una misa.\n- **Explicar dónde pedir ayuda** si alguien sigue mal.\n\nNo se trata de hacer terapia: se trata de que nadie quede solo con lo que siente."},
  {"title": "Señales para derivar",
   "body": "Después de algunas semanas, la mayoría de las personas se va recuperando. Hay que buscar ayuda profesional si alguien:\n\n- **No puede dormir, comer o funcionar** en su vida diaria.\n- **Se aísla** de forma persistente.\n- **Habla de no querer vivir** o de hacerse daño: en ese caso, avisa de inmediato a un adulto y llama al **\\*4141**.\n- **Revive el hecho** constantemente con mucha angustia.\n\nSalud Responde (**600 360 7777**) orienta sobre dónde consultar."}
 ],
 "bible": {"ref": "Juan 20,19-21 · Paz a ustedes",
  "comment": "Después de la muerte de Jesús, los discípulos están encerrados, con miedo. Jesús resucitado entra, se pone en medio y les dice: «La paz esté con ustedes». No borra lo que vivieron: les muestra sus heridas. Acompañar a un grupo en crisis es estar en medio, con paz, sin negar el dolor."},
 "church": [
  {"source": "Gaudium et spes 1", "text": "Los gozos y las esperanzas, las tristezas y las angustias de las personas de nuestro tiempo, sobre todo de los pobres y de los que sufren, son también los de los discípulos de Cristo.", "url": GS},
  {"source": "Christus vivit 291-298", "text": "Acompañar a los jóvenes implica escucharlos con paciencia y caminar junto a ellos en sus momentos difíciles.", "url": CV}
 ],
 "questions": [
  "¿Has vivido alguna vez una situación difícil como grupo? ¿Qué ayudó?",
  "¿Por qué es importante dar información clara y no dejar que corran rumores?",
  "¿Qué gestos simbólicos ayudan a un grupo a vivir un duelo?",
  "¿Quiénes son los adultos y profesionales a los que podrías acudir?"
 ],
 "activity": "Con el asesor, armen un plan breve de respuesta para una crisis en el grupo: a quién se avisa, quién habla con las familias, dónde se reúnen, quién guía el encuentro posterior y qué números de ayuda se usan.",
 "prayer": "Jesús resucitado, que entraste en medio de tus discípulos llenos de miedo: entra también en nuestros grupos cuando el dolor nos golpea. Danos tu paz, ayúdanos a no dejar a nadie solo y a buscar ayuda cuando la necesitemos. Amén.",
 "resources": [{"title": "Gaudium et spes (Concilio Vaticano II, 1965)", "url": GS, "note": "Número 1, sobre la cercanía de la Iglesia al dolor humano."}],
 "comenzar": "Piensa en un momento difícil que viviste junto a otros. ¿Qué hizo alguien que te ayudó a sentirte acompañado?",
 "logros": ["Reconocer las reacciones ante una crisis colectiva.", "Saber qué hacer en las primeras horas.", "Identificar cuándo derivar a ayuda profesional."],
 "profundizar": {"titulo": "Cuidar a quienes acompañan",
  "texto": "Los dirigentes que acompañan una crisis también quedan afectados. Después de la emergencia, necesitan un espacio propio para conversar con el asesor, descansar y, si lo necesitan, pedir ayuda profesional."},
 "caso": {"titulo": "El campamento",
  "texto": "En un campamento de verano, un joven sufre un accidente grave y es trasladado al hospital. El resto del grupo queda en el lugar, asustado, mientras corren versiones distintas por WhatsApp.",
  "preguntas": ["¿Qué harías en las primeras horas?", "¿Cómo acompañarías al grupo en los días siguientes?"]},
 "claves": [["Crisis colectiva", "Evento que afecta a todo un grupo."], ["Normalizar", "Explicar que las reacciones ante algo grave son esperables."], ["Derivar", "Conectar a la persona con ayuda profesional."]],
 "lectio": {"meditar": "Jesús se pone en medio. ¿Dónde necesita tu grupo esa presencia?",
  "orar": "Reza por algún grupo o comunidad que esté viviendo un dolor.",
  "vivir": "Guarda en tu teléfono los números de ayuda."},
 "practica": ["Definan a quién avisar.", "Asignen roles.", "Elijan el lugar de encuentro.", "Anoten los números de ayuda."],
 "idea": "En una crisis, nadie debe quedar solo con lo que siente."
}, [
 {"q": "¿Qué es lo primero en una crisis colectiva?", "options": ["Hacer un encuentro de oración", "Asegurar que todos estén a salvo y avisar a los adultos responsables", "Publicar lo ocurrido en redes"], "correct": 1, "feedback": "Seguridad primero, luego aviso y acompañamiento."},
 {"q": "Si alguien habla de no querer vivir, ¿qué haces?", "options": ["Esperas a ver si se le pasa", "Avisas de inmediato a un adulto y llaman al *4141", "Lo comentas con el grupo"], "correct": 1, "feedback": "Es una urgencia: se avisa y se busca ayuda de inmediato."}
])

UNIDADES["primeros-auxilios"] = (4, {
 "title": "Prevenir: actividades seguras",
 "objective": "Planificar una salida, jornada o campamento reduciendo riesgos y preparando la respuesta ante emergencias.",
 "intro": "La mejor emergencia es la que no ocurre. Muchos accidentes en actividades juveniles se pueden prevenir con una buena planificación. En esta unidad vas a aprender a preparar una actividad segura: antes, durante y después.",
 "sections": [
  {"title": "Antes de la actividad",
   "body": "- **Conocer el lugar:** visitarlo antes si es posible, identificar riesgos (agua, altura, tránsito, clima).\n- **Fichas de salud** de cada participante: alergias, enfermedades, medicamentos y contacto de emergencia.\n- **Autorizaciones firmadas** por los padres o tutores para menores de edad.\n- **Número de adultos responsables** adecuado al grupo y a la actividad.\n- **Plan de emergencia:** centro de salud más cercano, cómo llegar, quién maneja, cobertura de teléfono."},
  {"title": "El botiquín",
   "body": "Un botiquín básico para actividades:\n\n- Guantes desechables.\n- Gasas, apósitos y vendas.\n- Tela adhesiva y parches curitas.\n- Suero fisiológico para lavar heridas.\n- Tijeras y pinzas.\n- Manta térmica.\n- Bolsas de frío instantáneo.\n- Protector solar.\n\nLos medicamentos de cada participante los administra solo un adulto responsable, según la indicación de la familia. No se dan medicamentos por cuenta propia."},
  {"title": "Durante la actividad",
   "body": "- **Contar al grupo** en cada traslado o cambio de lugar.\n- **Sistema de parejas:** nadie anda solo.\n- **Hidratación y protección del sol** en verano.\n- **Reglas claras** sobre el agua, los fuegos y las zonas prohibidas.\n- **Atención al clima:** suspender o adaptar si cambia.\n- **Un adulto siempre ubicable** con el botiquín y las fichas de salud."},
  {"title": "Después",
   "body": "- **Avisar a las familias** de cualquier incidente, aunque sea menor.\n- **Registrar lo ocurrido:** qué pasó, cómo se atendió, quién estuvo presente.\n- **Evaluar con el equipo** qué funcionó y qué mejorar para la próxima vez.\n- **Reponer el botiquín.**"}
 ],
 "bible": {"ref": "Proverbios 22,3 · El prudente ve el peligro",
  "comment": "«El prudente ve el peligro y se pone a salvo; los inexpertos siguen adelante y sufren las consecuencias». La prudencia es una virtud cristiana: cuidar la vida de otros incluye pensar antes en lo que podría salir mal."},
 "church": [
  {"source": "Catecismo de la Iglesia Católica 2288", "text": "La vida y la salud física son bienes confiados por Dios; debemos cuidarlos razonablemente, teniendo en cuenta las necesidades de los demás.", "url": CEC_5},
  {"source": "Integridad en el Servicio Eclesial (Conferencia Episcopal de Chile, 2020)", "text": "Las actividades con menores de edad requieren autorización de los padres, adultos responsables suficientes y normas claras de cuidado.", "url": ISE}
 ],
 "questions": [
  "¿Qué riesgos has visto en actividades de tu grupo?",
  "¿Tu grupo usa fichas de salud y autorizaciones?",
  "¿Sabes dónde está el centro de salud más cercano al lugar de tu próxima actividad?",
  "¿Qué incidente pasado se pudo haber evitado?"
 ],
 "activity": "Planifiquen la seguridad de la próxima salida o jornada del grupo: lista de riesgos del lugar, plan de emergencia, revisión del botiquín y formato de ficha de salud y autorización.",
 "prayer": "Señor de la vida, que nos confías a nuestros hermanos: danos prudencia para prevenir, serenidad para actuar y un corazón atento al cuidado de cada uno. Que nuestras actividades sean lugares seguros donde todos puedan crecer. Amén.",
 "resources": [{"title": "Prevenir abusos: Iglesia en Chile", "url": ISE, "note": "Orientaciones para actividades con menores de edad."}],
 "comenzar": "Piensa en la última actividad fuera de la parroquia en la que participaste. ¿Había botiquín? ¿Sabías quién era el adulto responsable?",
 "logros": ["Identificar riesgos antes de una actividad.", "Preparar botiquín, fichas y autorizaciones.", "Aplicar normas de cuidado durante y después."],
 "profundizar": {"titulo": "Los campamentos de verano",
  "texto": "En verano aumentan los riesgos por calor, sol y agua. Nunca se debe permitir el baño sin un adulto responsable mirando y sin conocer el lugar. Los ríos, lagos y el mar en Chile pueden tener corrientes peligrosas incluso cuando parecen tranquilos."},
 "caso": {"titulo": "La salida improvisada",
  "texto": "Un sábado soleado, el grupo decide ir de improviso a un río cercano. Nadie lleva botiquín, no hay autorizaciones y solo un dirigente de 18 años acompaña a quince jóvenes.",
  "preguntas": ["¿Qué riesgos ves?", "¿Qué habría que preparar para hacer esa salida de forma segura?"]},
 "claves": [["Plan de emergencia", "Qué hacer, a quién llamar y dónde ir si algo pasa."], ["Ficha de salud", "Información médica y de contacto de cada participante."], ["Sistema de parejas", "Cada participante tiene un compañero del que se preocupa."]],
 "lectio": {"meditar": "El prudente ve el peligro. ¿Qué peligros no estás viendo?",
  "orar": "Reza por quienes organizan actividades con jóvenes.",
  "vivir": "Revisa esta semana el botiquín de tu grupo o parroquia."},
 "practica": ["Hagan la lista de riesgos.", "Preparen el plan de emergencia.", "Revisen el botiquín.", "Preparen fichas y autorizaciones."],
 "idea": "Cuidar la vida empieza antes de que ocurra la emergencia."
}, [
 {"q": "¿Qué documentos se necesitan para una salida con menores de edad?", "options": ["Ninguno", "Autorización de los padres y ficha de salud", "Solo la lista de asistencia"], "correct": 1, "feedback": "Autorización y ficha de salud son básicas."},
 {"q": "¿Quién puede dar medicamentos a un participante?", "options": ["Cualquier dirigente", "Solo un adulto responsable, según la indicación de la familia", "El mismo participante a otros"], "correct": 1, "feedback": "Los medicamentos no se dan por cuenta propia."}
])

UNIDADES["comunicacion-y-redes"] = (3, {
 "title": "Contar un evento",
 "objective": "Planificar y realizar la cobertura comunicacional de una actividad: antes, durante y después, cuidando a las personas.",
 "intro": "Una jornada, una misión o una fiesta patronal son oportunidades para contar lo que vive la comunidad. Pero una buena cobertura no se improvisa. En esta unidad vas a aprender a organizar un equipo de comunicación para un evento.",
 "sections": [
  {"title": "Antes: planificar",
   "body": "- **Definir qué se quiere contar:** ¿qué es lo más importante de este evento?\n- **Elegir los canales:** historias, publicaciones, mensaje a las familias, nota en el boletín parroquial.\n- **Repartir roles:** quién toma fotos, quién graba, quién escribe, quién publica.\n- **Revisar autorizaciones de imagen,** sobre todo de menores de edad.\n- **Anunciar el evento** con la información clave: qué, cuándo, dónde, para quién."},
  {"title": "Durante: registrar",
   "body": "- **Fotos de momentos, no solo de poses:** manos trabajando, rostros atentos, el lugar.\n- **Videos breves** de 10 a 20 segundos.\n- **Frases de los participantes,** con su permiso.\n- **Respetar los momentos sagrados:** no fotografiar con flash durante la consagración ni interrumpir la oración.\n- **No publicar en tiempo real** lo que no se ha revisado."},
  {"title": "Después: contar",
   "body": "- **Elegir pocas imágenes buenas** en vez de muchas regulares.\n- **Escribir un texto breve** que cuente qué se vivió y por qué importa.\n- **Agradecer** a quienes hicieron posible el evento.\n- **Publicar dentro de las 48 horas,** mientras el evento está fresco.\n- **Guardar el material ordenado** para el archivo del grupo."},
  {"title": "Cuidar a las personas",
   "body": "- **No publicar imágenes de menores** sin autorización escrita de sus padres o tutores.\n- **Evitar fotos** que puedan avergonzar a alguien.\n- **No etiquetar** a menores ni mostrar datos que permitan ubicarlos.\n- **Retirar de inmediato** una imagen si alguien lo pide.\n- **Pensar antes de publicar:** ¿le gustaría a esta persona verse así?"}
 ],
 "bible": {"ref": "Lucas 1,1-4 · Escribir todo ordenadamente",
  "comment": "Lucas dice que investigó todo cuidadosamente desde el principio para escribirlo ordenadamente, para que Teófilo conozca la solidez de lo que le enseñaron. Contar bien lo que vive la comunidad, con verdad y orden, es una forma de evangelizar."},
 "church": [
  {"source": "Inter mirifica (Concilio Vaticano II, 1963)", "text": "Los medios de comunicación pueden servir al anuncio del Evangelio cuando se usan con verdad, respeto a las personas y sentido del bien común.", "url": IM},
  {"source": "Christus vivit 87", "text": "El ambiente digital es un lugar de encuentro y comunicación, pero también de riesgos que exigen cuidar a las personas.", "url": CV}
 ],
 "questions": [
  "¿Qué evento reciente de tu grupo valdría la pena contar?",
  "¿Qué fotos de actividades pasadas te parecen buenas? ¿Por qué?",
  "¿Tu grupo pide autorización para publicar imágenes de menores?",
  "¿Qué momentos de una celebración no deberían fotografiarse?"
 ],
 "activity": "Planifiquen la cobertura del próximo evento del grupo: objetivo, canales, roles, autorizaciones y una pauta de fotos. Después del evento, publiquen y evalúen juntos el resultado.",
 "prayer": "Señor, que inspiraste a Lucas a contar con cuidado tu historia: ayúdanos a contar con verdad y alegría lo que vive nuestra comunidad. Que nuestras imágenes y palabras cuiden siempre la dignidad de cada persona. Amén.",
 "resources": [{"title": "Inter mirifica", "url": IM, "note": "Decreto del Concilio sobre los medios de comunicación."}],
 "comenzar": "Busca en tus redes la publicación de un evento parroquial o juvenil que te haya gustado. ¿Qué la hace buena?",
 "logros": ["Planificar la cobertura de un evento.", "Registrar y publicar con calidad.", "Cuidar la imagen y los datos de las personas."],
 "profundizar": {"titulo": "La pauta de fotos",
  "texto": "Una lista de las fotos que no pueden faltar ayuda a no olvidar nada: el lugar y el ambiente, la acogida, un momento de oración, el trabajo en grupos, la foto grupal final, los organizadores, un detalle simbólico."},
 "caso": {"titulo": "La foto viral",
  "texto": "Durante una jornada, un joven sube una historia con un video gracioso de un niño de 9 años que se cae. El video se comparte mucho. La mamá del niño escribe molesta a la parroquia.",
  "preguntas": ["¿Qué falló?", "¿Qué hay que hacer ahora?"]},
 "claves": [["Cobertura", "Registro y difusión de un evento."], ["Autorización de imagen", "Permiso para publicar la imagen de una persona."], ["Pauta", "Lista planificada de lo que se registrará."]],
 "lectio": {"meditar": "Escribir ordenadamente. ¿Qué historia de tu comunidad merece ser contada?",
  "orar": "Reza por quienes comunican en la Iglesia.",
  "vivir": "Revisa tus publicaciones antiguas y retira alguna que pueda incomodar a otros."},
 "practica": ["Definan el objetivo.", "Repartan roles.", "Revisen autorizaciones.", "Publiquen y evalúen."],
 "idea": "Contar bien lo que vivimos también es anunciar."
}, [
 {"q": "¿Qué se necesita para publicar fotos de menores de edad?", "options": ["Nada, si es una actividad de la Iglesia", "Autorización escrita de sus padres o tutores", "Que el menor esté de acuerdo"], "correct": 1, "feedback": "La autorización de los padres o tutores es indispensable."},
 {"q": "¿Qué conviene al publicar después de un evento?", "options": ["Subir todas las fotos", "Elegir pocas imágenes buenas y un texto breve", "Esperar un mes"], "correct": 1, "feedback": "Menos y mejor comunica más."}
])

UNIDADES["dinamicas-y-juegos"] = (3, {
 "title": "Animar una jornada completa",
 "objective": "Diseñar el ritmo de una jornada o encuentro largo, combinando juego, reflexión, oración y descanso.",
 "intro": "Una dinámica bien hecha dura 15 minutos. Una jornada dura un día entero. Animarla requiere pensar en el ritmo: cuándo subir la energía, cuándo bajarla, cuándo reflexionar y cuándo descansar. En esta unidad vas a aprender a diseñar una jornada completa.",
 "sections": [
  {"title": "La curva de energía",
   "body": "La energía de un grupo sube y baja durante el día:\n\n- **Al llegar:** gente que no se conoce o viene cansada. Dinámicas de acogida y presentación.\n- **Media mañana:** buena atención. Momento para el tema central.\n- **Después de almuerzo:** energía baja. Juegos activos, no charlas largas.\n- **Tarde:** trabajo en grupos y gran juego.\n- **Cierre:** calma, oración y envío.\n\nUna buena jornada alterna momentos activos y momentos de profundidad."},
  {"title": "Las transiciones",
   "body": "Pasar de un momento a otro es donde más se pierde el grupo. Ayuda:\n\n- **Anunciar lo que viene** con claridad.\n- **Usar una señal** conocida para reunir al grupo: un canto, una palmada, una campana.\n- **Pasar de lo activo a lo reflexivo** con una dinámica de calma intermedia.\n- **Tener todo preparado** antes, para no hacer esperar."},
  {"title": "El equipo de animación",
   "body": "Nadie anima solo una jornada. Un equipo funciona mejor si:\n\n- **Cada momento tiene un responsable.**\n- **Hay alguien a cargo de los tiempos** que avisa cuando hay que avanzar.\n- **Alguien cuida a los participantes:** quién está solo, quién se siente mal.\n- **Se reúnen brevemente** durante la jornada para ajustar.\n- **Evalúan al final,** cuando todo está fresco."},
  {"title": "Imprevistos",
   "body": "Siempre pasa algo: llueve, llegan menos personas, una dinámica no resulta. Ten preparado:\n\n- **Un plan B bajo techo** para los juegos al aire libre.\n- **Dinámicas cortas de reserva** para llenar un espacio.\n- **Flexibilidad:** si el grupo está cansado, acorta; si está muy metido en una conversación, dale más tiempo.\n- **Lo esencial no se negocia:** la oración y el cierre se mantienen."}
 ],
 "bible": {"ref": "Marcos 6,30-32 · Vengan a descansar un poco",
  "comment": "Los apóstoles vuelven de la misión con mucho que contar y tan ocupados que no tienen tiempo ni para comer. Jesús les dice: «Vengan ustedes solos a un lugar apartado y descansen un poco». Jesús cuida el ritmo de los suyos: trabajo, encuentro y descanso."},
 "church": [
  {"source": "Gaudete et exsultate 122-128", "text": "La alegría y el sentido del humor son parte de la santidad: el santo vive con alegría y la contagia a los demás.", "url": GE},
  {"source": "Christus vivit 226-228", "text": "El deporte, el juego y la vida al aire libre son espacios privilegiados para el encuentro y el crecimiento de los jóvenes.", "url": CV}
 ],
 "questions": [
  "¿Cuál ha sido la mejor jornada en la que has participado? ¿Qué la hizo buena?",
  "¿En qué momento del día suele bajar más la energía de tu grupo?",
  "¿Qué imprevisto has tenido que resolver en una actividad?",
  "¿Cómo se reparten las tareas en el equipo de animación de tu grupo?"
 ],
 "activity": "En equipos, diseñen el programa completo de una jornada de seis horas para el grupo: horarios, momentos, responsables, materiales y plan B. Preséntenlo y reciban comentarios de los demás equipos.",
 "prayer": "Señor, que cuidaste el ritmo de tus discípulos: ayúdanos a animar jornadas donde haya juego, encuentro, oración y descanso. Que cada momento ayude a nuestros jóvenes a encontrarse contigo y entre ellos. Amén.",
 "resources": [{"title": "Gaudete et exsultate (Francisco, 2018)", "url": GE, "note": "Números 122-128, sobre la alegría."}],
 "comenzar": "Recuerda una jornada aburrida en la que participaste. ¿En qué momento se perdió el grupo?",
 "logros": ["Diseñar el ritmo de una jornada según la energía del grupo.", "Cuidar las transiciones entre momentos.", "Trabajar en equipo y prever imprevistos."],
 "profundizar": {"titulo": "Plantilla de jornada",
  "texto": "Una tabla con cinco columnas ayuda a planificar: hora, momento, objetivo, responsable y materiales. Revisen que no haya más de 45 minutos seguidos sentados escuchando y que exista un momento de oración y uno de evaluación."},
 "caso": {"titulo": "La charla después del almuerzo",
  "texto": "En una jornada, el equipo programa una charla de una hora justo después de almuerzo. A los diez minutos, la mitad del grupo está con el celular y varios se quedan dormidos.",
  "preguntas": ["¿Qué falló en el diseño?", "¿Cómo reorganizarías esa parte de la jornada?"]},
 "claves": [["Curva de energía", "Cómo cambia la atención del grupo durante el día."], ["Transición", "Paso de un momento de la jornada a otro."], ["Plan B", "Alternativa preparada ante imprevistos."]],
 "lectio": {"meditar": "Vengan a descansar un poco. ¿Respetas tu propio ritmo?",
  "orar": "Reza por el equipo con el que animas.",
  "vivir": "Regálate esta semana un momento real de descanso."},
 "practica": ["Definan el objetivo de la jornada.", "Diseñen el programa.", "Asignen responsables.", "Preparen el plan B."],
 "idea": "Una buena jornada alterna juego, profundidad y descanso."
}, [
 {"q": "¿Qué conviene programar después de almuerzo?", "options": ["Una charla larga", "Juegos activos", "Un momento de silencio de una hora"], "correct": 1, "feedback": "Después de almuerzo la energía baja: hay que moverse."},
 {"q": "¿Qué no se negocia ante imprevistos?", "options": ["El gran juego", "La oración y el cierre", "El horario de almuerzo"], "correct": 1, "feedback": "Lo esencial se mantiene; lo demás se adapta."}
])
