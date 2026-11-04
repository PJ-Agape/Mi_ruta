"""Programa académico del Diplomado en Sagrada Escritura.

Cada módulo: objetivos, carga horaria (30 h), lecturas obligatorias, bibliografía complementaria,
recursos en línea, trabajo escrito y evaluación final. Cada sesión: lectura bíblica, lectura del manual,
estado de la cuestión y preguntas de estudio.

Criterio bibliográfico: solo obras verificadas (autor, título, editorial y año); no se indican páginas.
Referencia académica: programa de Sagrada Escritura II de la Facultad de Teología de la UCA (Buenos Aires).
"""

V = "https://www.vatican.va"
DV = V + "/archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19651118_dei-verbum_sp.html"
VD = V + "/content/benedict-xvi/es/apost_exhortations/documents/hf_ben-xvi_exh_20100930_verbum-domini.html"
CEC = V + "/archive/catechism_sp/index_sp.html"
PD = V + "/content/leo-xiii/es/encyclicals/documents/hf_l-xiii_enc_18111893_providentissimus-deus.html"
DAS = V + "/content/pius-xii/es/encyclicals/documents/hf_p-xii_enc_30091943_divino-afflante-spiritu.html"
IBI = "https://laici.op.org/wp-content/uploads/sites/12/2025/10/Interpretacion-de-la-Biblia-en-la-Iglesia-Pontificia-Comision-Biblica.pdf"
PCB = V + "/content/romancuria/es/pontificie-commissioni/pontificia-commissione-biblica/profilo.html"
RUIZ = "https://repositorio.uca.edu.ar/handle/123456789/17629"
RODELAS = "https://dialnet.unirioja.es/descarga/articulo/9522009.pdf"
BXVI_2009 = V + "/content/benedict-xvi/es/speeches/2009/april/documents/hf_ben-xvi_spe_20090423_pcb.html"

# Lecturas comunes ---------------------------------------------------------
BIBLIA = "*La Biblia. Libro del Pueblo de Dios*, trad. A. J. Levoratti y A. B. Trusso, Verbo Divino, Estella 2015 (u otra edición católica con introducciones y notas: Biblia de Jerusalén, Biblia de la Conferencia Episcopal Española)."
DV_T = ("Concilio Vaticano II, constitución dogmática *Dei Verbum* (1965)", DV)
VD_T = ("Benedicto XVI, exhortación apostólica *Verbum Domini* (2010)", VD)
IBI_T = ("Pontificia Comisión Bíblica, *La interpretación de la Biblia en la Iglesia* (1993), PPC, Madrid 1993", IBI)
PJ_T = "Pontificia Comisión Bíblica, *El pueblo judío y sus Escrituras sagradas en la Biblia cristiana* (2001), PPC, Madrid 2002."
IV_T = "Pontificia Comisión Bíblica, *Inspiración y verdad de la Sagrada Escritura* (2014), BAC, Madrid 2014."
JER = "R. E. Brown – J. A. Fitzmyer – R. E. Murphy (eds.), *Nuevo comentario bíblico San Jerónimo*, Verbo Divino, Estella 2004 (dos tomos: AT y NT)."
BROWN_NT = "R. E. Brown, *Introducción al Nuevo Testamento*, 2 vols., Trotta, Madrid 2002."
SICRE_AT = "J. L. Sicre, *Introducción al Antiguo Testamento*, Verbo Divino, Estella (ediciones sucesivas)."

ONLINE_BASE = [
    ("*Dei Verbum*, texto completo en vatican.va", DV),
    ("*Verbum Domini*, texto completo en vatican.va", VD),
    ("*La interpretación de la Biblia en la Iglesia* (PDF)", IBI),
    ("Catecismo de la Iglesia Católica, nn. 101-141", CEC),
]


def M(objetivos, obligatoria, complementaria, online, trabajo, sesiones, contenidos_minimos):
    assert len(sesiones) == 5
    return {"objetivos": objetivos, "obligatoria": obligatoria, "complementaria": complementaria,
            "online": online, "trabajo": trabajo, "sesiones": sesiones, "contenidos": contenidos_minimos}


def S(biblia, manual, profundizacion, preguntas):
    return {"biblia": biblia, "manual": manual, "profundizacion": profundizacion, "preguntas": preguntas}


PROGRAMA = {}

# =========================================================================
PROGRAMA["se-1"] = M(
    objetivos=[
        "Describir el canon del Antiguo Testamento católico y explicar sus diferencias con la Biblia hebrea y las Biblias protestantes.",
        "Situar los libros del AT en las grandes etapas de la historia de Israel, del período patriarcal a la época helenística.",
        "Explicar, en sus líneas generales, cómo se formaron las tradiciones y los libros del AT.",
        "Fundamentar desde *Dei Verbum* 14-16 y el documento de la PCB de 2001 la lectura cristiana del AT.",
    ],
    contenidos_minimos="Canon, texto y versiones. Historia de Israel y su lectura crítica. Formación literaria del AT. Unidad de los dos Testamentos.",
    obligatoria=[
        BIBLIA,
        "J. L. Sicre, *Introducción al Antiguo Testamento*, Verbo Divino, Estella: capítulos sobre el canon, la historia de Israel y la formación de los libros.",
        "J. M. Sánchez Caro, «El canon de la Biblia», en V. M. Artola – J. M. Sánchez Caro, *Biblia y Palabra de Dios* (Introducción al estudio de la Biblia 2), Verbo Divino, Estella 1992.",
        "*Dei Verbum*, nn. 11-16 (inspiración, verdad, interpretación y Antiguo Testamento).",
    ],
    complementaria=[
        "J. González Echegaray y otros, *La Biblia en su entorno* (Introducción al estudio de la Biblia 1), Verbo Divino, Estella.",
        "M. Tábet, *Introducción al Antiguo Testamento I. Pentateuco y libros históricos*, Palabra, Madrid.",
        "J. Trebolle Barrera – M. Pérez Fernández, *Historia de la Biblia*, Trotta, Madrid 2006.",
        "G. von Rad, *Teología del Antiguo Testamento*, 2 vols., Sígueme, Salamanca.",
        "U. Mannucci, *La Biblia como Palabra de Dios*, Desclée de Brouwer, Bilbao 1997.",
        PJ_T,
        IV_T,
        JER,
    ],
    online=ONLINE_BASE + [
        ("León XIII, *Providentissimus Deus* (1893)", PD),
        ("Pío XII, *Divino afflante Spiritu* (1943)", DAS),
        ("Pontificia Comisión Bíblica: perfil y documentos (vatican.va)", PCB),
    ],
    trabajo=("Ensayo breve (1.500 a 2.000 palabras): **«¿Por qué los cristianos leemos el Antiguo Testamento?»**. "
             "Elige un texto del AT (por ejemplo, Gn 12,1-9; Ex 3,1-15; 2 Sam 7,1-17 o Is 7,10-17) y explica: a) su contexto histórico aproximado; "
             "b) qué dice en su sentido literal; c) cómo lo relee el NT; d) qué enseña *Dei Verbum* 15-16 sobre esta relación. "
             "Cita al menos dos lecturas del programa y un documento del Magisterio."),
    sesiones=[
        S("Lc 24,13-35 y 44-48; Neh 8,1-12; Prólogo del Eclesiástico (Sir, prólogo).",
          "Sánchez Caro, *Biblia y Palabra de Dios*: el canon del AT, los deuterocanónicos y las versiones antiguas (Septuaginta, Vulgata).",
          "La investigación actual distingue entre la fijación del canon hebreo, que no se resolvió en un «concilio de Jamnia» como se repetía antes, y el uso cristiano de las Escrituras griegas. "
          "La Iglesia antigua recibió una colección más amplia, cercana a la Septuaginta, y el Concilio de Trento la definió solemnemente (1546). "
          "Las Biblias de tradición protestante siguieron el canon hebreo y llaman «apócrifos» a los deuterocanónicos. Para un agente de pastoral, lo decisivo es poder explicar esta diferencia sin polémica y con datos.",
          ["¿Qué criterios usó la Iglesia antigua para reconocer un libro como canónico?",
           "¿Por qué la Septuaginta tuvo tanta importancia para los primeros cristianos?",
           "Explica con tus palabras la diferencia entre «canon», «inspiración» y «verdad» de la Escritura."]),
        S("Gn 12,1-9; Ex 1–3; Jos 24; 2 Sam 7; 1 Re 12; 2 Re 17 y 25.",
          "Sicre, *Introducción al AT*: la historia de Israel desde los orígenes hasta el exilio.",
          "El relato bíblico de la historia de Israel es teología de la historia: interpreta los hechos a la luz de la alianza. "
          "La arqueología y la historiografía han matizado muchas reconstrucciones (por ejemplo, sobre la conquista o la extensión del reino davídico), y el debate entre posturas más conservadoras y más críticas sigue abierto. "
          "*Dei Verbum* 12 pide atender a los géneros literarios y a las formas de narrar de la época: el objetivo no es «probar» cada detalle, sino comprender qué verdad quiere enseñar el texto «para nuestra salvación» (DV 11).",
          ["¿Qué diferencia hay entre una crónica moderna y la historia teológica de los libros de Reyes?",
           "Señala tres momentos de crisis en la historia de Israel y qué preguntas de fe provocaron.",
           "¿Cómo entiendes la expresión de DV 11 «la verdad que Dios quiso consignar para nuestra salvación»?"]),
        S("Esd 1; Neh 1–2; Dn 7; 1 Mac 1–2; Sal 137.",
          "Sicre, *Introducción al AT*: exilio, época persa, helenística y macabea. Complementa con *La Biblia en su entorno*.",
          "El exilio en Babilonia (587-538 a.C.) es considerado por la mayoría de los estudiosos como el gran momento de reflexión y redacción de las tradiciones de Israel. "
          "En la época persa se consolidan la Ley y el templo; en la helenística aparecen la sabiduría en diálogo con la cultura griega y la apocalíptica. "
          "Este período, a veces llamado «intertestamentario», es indispensable para entender el judaísmo plural del tiempo de Jesús (fariseos, saduceos, esenios).",
          ["¿Por qué se dice que el exilio fue una crisis fecunda?",
           "¿Qué es la apocalíptica y en qué libros del AT aparece?",
           "Describe dos grupos judíos del siglo I y su origen histórico."]),
        S("Gn 1,1–2,4a y 2,4b-25 (compara ambos relatos); Dt 26,5-10; Jr 36.",
          "Sánchez Caro, *Biblia y Palabra de Dios*: inspiración y formación de la Escritura; Sicre, *Introducción al AT*: tradiciones orales y escritas.",
          "La formación del AT fue un proceso largo: tradiciones orales, colecciones, redacciones y relecturas a lo largo de siglos. "
          "La clásica hipótesis documental (J, E, D, P) ha sido muy revisada desde fines del siglo XX y hoy conviven modelos distintos, que se estudian en el módulo IV. "
          "Para la fe, este proceso humano no es un obstáculo: la PCB (*Inspiración y verdad*, 2014) explica que la inspiración abarca a los distintos autores y redactores que intervinieron en el texto.",
          ["¿Qué indicios del propio texto bíblico muestran que hubo un proceso de redacción?",
           "¿Por qué el carácter humano de la formación de la Biblia no niega su inspiración?",
           "¿Qué significa que Dios es «autor» de la Escritura según DV 11?"]),
        S("Mt 5,17-20; 2 Cor 3,12-18; Heb 1,1-4; Rom 15,4.",
          "*Dei Verbum* 14-16 y PCB, *El pueblo judío y sus Escrituras sagradas en la Biblia cristiana*, primera parte.",
          "La lectura cristiana del AT se mueve entre dos riesgos: el marcionismo, que lo descarta, y una lectura que lo convierte solo en «anuncio» sin valor propio. "
          "La PCB (2001) afirma que el AT posee un valor permanente y que la lectura judía es una lectura posible y legítima, mientras que la cristiana lo lee a la luz de Cristo. "
          "San Agustín lo resumió así: el Nuevo está escondido en el Antiguo y el Antiguo se hace claro en el Nuevo (citado en DV 16).",
          ["¿Qué fue el marcionismo y por qué la Iglesia lo rechazó?",
           "¿Qué significa leer el AT «a la luz de Cristo» sin quitarle su sentido propio?",
           "¿Qué consecuencias pastorales tiene el documento de la PCB de 2001 para hablar del pueblo judío?"]),
    ],
)

# =========================================================================
PROGRAMA["se-2"] = M(
    objetivos=[
        "Describir el contexto político, social y religioso de Palestina en el siglo I.",
        "Explicar las tres etapas de la formación de los evangelios (Jesús, predicación apostólica, redacción) según *Sancta Mater Ecclesia* y DV 19.",
        "Presentar los 27 libros del NT, sus géneros y su proceso de canonización.",
        "Aplicar criterios básicos de interpretación católica (DV 12; *La interpretación de la Biblia en la Iglesia*).",
    ],
    contenidos_minimos="Contexto del NT. Formación de los evangelios. Literatura epistolar. Canon y texto del NT. Hermenéutica católica.",
    obligatoria=[
        BIBLIA,
        BROWN_NT + " Partes I (preliminares) y II (evangelios y obras afines, introducción general).",
        "R. Aguirre Monasterio – A. Rodríguez Carmona, *Evangelios sinópticos y Hechos de los Apóstoles* (Introducción al estudio de la Biblia 6), Verbo Divino, Estella 1994: parte introductoria.",
        "*Dei Verbum*, nn. 17-20; Pontificia Comisión Bíblica, instrucción *Sancta Mater Ecclesia* sobre la verdad histórica de los evangelios (1964).",
    ],
    complementaria=[
        "J. Jeremias, *Jerusalén en tiempos de Jesús*, Cristiandad, Madrid 1977.",
        "H. Köster, *Introducción al Nuevo Testamento*, Sígueme, Salamanca 1988.",
        "E. W. Stegemann – W. Stegemann, *Historia social del cristianismo primitivo*, Verbo Divino, Estella 2001.",
        "J. L. Sicre, *El cuadrante II. La apertura. El mundo de Jesús*, Verbo Divino, Estella 1997.",
        "C. Tassin, Cuadernos Bíblicos 136 (2007) y 144 (2009), Verbo Divino, Estella: el judaísmo en tiempos de Jesús.",
        "D. Marguerat (dir.), *Introducción al Nuevo Testamento. Su historia, su escritura, su teología*, Desclée de Brouwer, Bilbao 2008.",
        "R. Penna, *La formación del Nuevo Testamento en sus tres dimensiones*, Verbo Divino, Estella 2012.",
        "L. H. Rivas, *Los libros y la historia de la Biblia*, San Benito, Buenos Aires 2013.",
        "A. Wikenhauser – J. Schmid, *Introducción al Nuevo Testamento*, Herder, Barcelona 1978.",
        "J. Gnilka, *Teología del Nuevo Testamento*, Trotta, Madrid 1998.",
    ],
    online=ONLINE_BASE + [
        ("E. Ruiz, «A 30 años de *La interpretación de la Biblia en la Iglesia*», *Teología* 142 (2023), repositorio UCA", RUIZ),
        ("Benedicto XVI, discurso a la Pontificia Comisión Bíblica (2009)", BXVI_2009),
    ],
    trabajo=("Trabajo escrito (1.500 a 2.000 palabras): **del Jesús histórico al texto evangélico**. "
             "Elige una perícopa breve (Mc 1,14-15; Mc 2,23-28; Lc 11,1-4 o Mt 6,9-13) y describe las tres etapas de su transmisión según *Dei Verbum* 19: "
             "a) qué elementos remontan a Jesús y su contexto palestino; b) cómo la usó la predicación de la Iglesia; c) cómo la integró el evangelista en su obra. "
             "Cita al menos dos lecturas del programa."),
    sesiones=[
        S("Lc 2,1-7; Lc 3,1-2; Mc 12,13-27; Hch 23,6-10.",
          "Brown, *Introducción al NT*: el mundo político y religioso del NT. Complementa con Jeremias o Stegemann.",
          "La investigación del siglo XX amplió mucho el conocimiento del judaísmo del Segundo Templo gracias a los manuscritos de Qumrán (descubiertos desde 1947) y al estudio de la literatura rabínica. "
          "Hoy se habla de «judaísmos» en plural: un mundo diverso dentro del cual Jesús debe ser comprendido como judío. "
          "La historia social (Stegemann, Theissen) añadió preguntas sobre economía, campesinado y estructuras de poder en Galilea.",
          ["¿Qué aportaron los manuscritos de Qumrán a la comprensión del NT?",
           "Describe la situación política de Judea y Galilea en tiempos de Jesús.",
           "¿Por qué es importante comprender a Jesús dentro del judaísmo de su tiempo?"]),
        S("Lc 1,1-4; 1 Cor 15,1-11; Hch 2,14-36; Jn 20,30-31.",
          "Aguirre – Rodríguez Carmona, *Evangelios sinópticos y Hechos*: formación de los evangelios. *Dei Verbum* 18-19.",
          "La instrucción *Sancta Mater Ecclesia* (1964), recogida en DV 19, distingue tres etapas: lo que Jesús hizo y enseñó, la predicación apostólica después de Pascua y la redacción de los evangelistas. "
          "Esto permitió integrar en la exégesis católica la historia de las formas y de la redacción, rechazando a la vez sus presupuestos filosóficos escépticos. "
          "La «tercera búsqueda» del Jesús histórico (desde los años 80) y los trabajos sobre memoria y tradición oral (Guijarro, Dunn) han dado nuevos instrumentos para estudiar la primera etapa.",
          ["¿Cuáles son las tres etapas de formación de los evangelios según DV 19?",
           "¿Qué afirma la Iglesia sobre la historicidad de los evangelios y qué no afirma?",
           "¿Qué significa que los evangelistas «escogieron, sintetizaron y explicaron» el material recibido?"]),
        S("Rom 1,1-7; Flm completo; 2 Pe 3,15-16; Ap 1,1-3.",
          "Brown, *Introducción al NT*: la forma de las cartas y el panorama de los libros. Rivas, *Los libros y la historia de la Biblia*: el canon del NT.",
          "El canon del NT se fue configurando entre los siglos II y IV: hacia fines del siglo II ya había un núcleo reconocido (cuatro evangelios y cartas de Pablo), y libros como Hebreos, Santiago, 2 Pedro o el Apocalipsis tardaron más en ser aceptados en todas las Iglesias. "
          "El Fragmento Muratoriano y la carta pascual de san Atanasio (367) son testigos clave. "
          "La crítica textual trabaja hoy con miles de manuscritos griegos; el NT es el texto antiguo mejor documentado.",
          ["¿Qué libros del NT fueron discutidos por más tiempo y por qué?",
           "¿Qué es la crítica textual y para qué sirve?",
           "¿Qué estructura típica tiene una carta del NT?"]),
        S("Hch 2,42-47; Hch 15; Gal 2,1-14; 1 Cor 11,17-34.",
          "Marguerat (dir.), *Introducción al NT* o Brown: el cristianismo primitivo. Stegemann, *Historia social*: las comunidades urbanas.",
          "Las primeras comunidades fueron diversas: judeocristianas en Jerusalén, helenistas, comunidades paulinas en ciudades griegas. "
          "El llamado concilio de Jerusalén (Hch 15; Gal 2) muestra cómo resolvieron el conflicto sobre la Ley. "
          "Los estudios sociales ayudan a entender la vida de las «iglesias domésticas», su composición social y el papel de las mujeres (Febe, Prisca, Junia).",
          ["¿Qué problema se resolvió en el concilio de Jerusalén y cómo?",
           "¿Qué era una iglesia doméstica?",
           "Compara Hch 15 y Gal 2: ¿qué coincide y qué difiere?"]),
        S("2 Tim 3,14-17; Lc 4,16-21; Hch 8,26-40.",
          "PCB, *La interpretación de la Biblia en la Iglesia*: I (métodos) y III (dimensiones de la interpretación católica).",
          "*La interpretación de la Biblia en la Iglesia* (1993) valora el método histórico-crítico como «indispensable», acoge métodos literarios (retórico, narrativo, semiótico) y enfoques contextuales, y rechaza la lectura fundamentalista. "
          "Benedicto XVI, en *Verbum Domini* 34-38, insistió en unir el análisis histórico con la lectura teológica según DV 12: unidad de toda la Escritura, Tradición viva y analogía de la fe.",
          ["¿Por qué la PCB considera peligrosa la lectura fundamentalista?",
           "¿Cuáles son los tres criterios teológicos de DV 12?",
           "¿Qué método te parece más útil para tu servicio pastoral y por qué?"]),
    ],
)

# =========================================================================
PROGRAMA["se-3"] = M(
    objetivos=[
        "Explicar la cuestión sinóptica y la teoría de las dos fuentes, con sus límites.",
        "Reconocer los rasgos literarios y teológicos propios de Marcos, Mateo y Lucas.",
        "Leer Hechos de los Apóstoles como segunda parte de la obra lucana.",
        "Realizar un análisis sinóptico comparando una perícopa en los tres evangelios.",
    ],
    contenidos_minimos="Cuestión sinóptica. Teología de Marcos, Mateo y Lucas. Hechos de los Apóstoles. Método de comparación sinóptica.",
    obligatoria=[
        BIBLIA + " Se recomienda además una *sinopsis* de los evangelios.",
        "R. Aguirre Monasterio – A. Rodríguez Carmona, *Evangelios sinópticos y Hechos de los Apóstoles* (Introducción al estudio de la Biblia 6), Verbo Divino, Estella 1994.",
        "S. Guijarro Oporto, *Los cuatro evangelios*, Sígueme, Salamanca 2010; o del mismo autor *Los Evangelios. Memoria, biografía, escritura*, Sígueme, Salamanca 2012.",
        "*Dei Verbum*, nn. 18-19.",
    ],
    complementaria=[
        "J. M. Edo, *Evangelios sinópticos y Hechos de los Apóstoles*, EUNSA, Pamplona 2016.",
        "L. H. Rivas, *¿Qué es un Evangelio?*, Claretiana, Buenos Aires 1981.",
        "H. Lona, *Jesús según el anuncio de los cuatro evangelios*, Claretiana, Buenos Aires 2009.",
        BROWN_NT,
        JER,
    ],
    online=ONLINE_BASE + [("Benedicto XVI, discurso a la Pontificia Comisión Bíblica (2009)", BXVI_2009)],
    trabajo=("Análisis sinóptico (1.500 a 2.500 palabras). Elige una perícopa presente en los tres sinópticos "
             "(el bautismo de Jesús, la confesión de Pedro, la tempestad calmada o la parábola del sembrador). "
             "a) Copia los tres textos en columnas; b) marca coincidencias y diferencias; c) explica qué revela cada diferencia sobre la teología de cada evangelista; "
             "d) cierra con una aplicación pastoral. Cita al menos dos lecturas del programa."),
    sesiones=[
        S("Mc 1,40-45 // Mt 8,1-4 // Lc 5,12-16; Mc 4,35-41 // Mt 8,23-27 // Lc 8,22-25.",
          "Aguirre – Rodríguez Carmona: la cuestión sinóptica. Guijarro: la tradición oral y las fuentes.",
          "La teoría de las dos fuentes (prioridad de Marcos más una fuente de dichos, «Q») es la más aceptada, pero no la única: la hipótesis de Farrer-Goulder prescinde de Q y otros modelos subrayan la tradición oral. "
          "Ningún manuscrito de Q ha sido encontrado; se reconstruye por comparación de Mateo y Lucas. Conviene presentarla como hipótesis de trabajo, no como dato.",
          ["¿Qué observaciones textuales llevaron a la hipótesis de la prioridad de Marcos?",
           "¿Qué es Q y por qué se discute su existencia?",
           "¿Qué aporta la tradición oral a la explicación del problema sinóptico?"]),
        S("Mc 1,1-15; 8,27–9,1; 15,33-39; 16,1-8.",
          "Aguirre – Rodríguez Carmona: el evangelio de Marcos.",
          "Desde W. Wrede (1901) se discute el llamado «secreto mesiánico». Hoy se lee Marcos como narración teológica: el evangelio avanza hacia la confesión del centurión al pie de la cruz (Mc 15,39). "
          "La datación habitual es en torno al año 70; se discute si fue escrito en Roma o en Siria. El final breve (16,8) es el original según la mayoría de los críticos; 16,9-20 es canónico pero añadido.",
          ["¿Qué es el «secreto mesiánico» y qué función tiene en Marcos?",
           "¿Por qué la confesión del centurión es un punto culminante?",
           "¿Qué consecuencias tiene que Mc 16,9-20 sea un añadido canónico?"]),
        S("Mt 1,1-17; 5–7; 16,13-20; 28,16-20.",
          "Aguirre – Rodríguez Carmona: el evangelio de Mateo.",
          "Mateo organiza el material en cinco grandes discursos, y muchos autores ven en él un paralelo con el Pentateuco. Escribe probablemente para una comunidad judeocristiana en conflicto con el judaísmo fariseo después del año 70. "
          "Esto obliga a leer con cuidado las polémicas (Mt 23) para no convertirlas en antijudaísmo, como advierte la PCB (2001).",
          ["¿Cuáles son los cinco discursos de Mateo?",
           "¿Cómo presenta Mateo a Jesús en relación con la Ley?",
           "¿Cómo leer Mt 23 en la catequesis sin caer en el antijudaísmo?"]),
        S("Lc 1,1-4; 4,16-30; 15; 24,13-35.",
          "Aguirre – Rodríguez Carmona: el evangelio de Lucas.",
          "Lucas escribe una «narración ordenada» (Lc 1,3) en dos tomos, con conciencia de historiador helenístico. H. Conzelmann propuso leerlo como una teología de la historia de la salvación en etapas, lectura que luego fue discutida. "
          "Son característicos de Lucas la misericordia, los pobres, la oración, las mujeres y el Espíritu Santo.",
          ["¿Qué significa que Lucas escribe una «narración ordenada»?",
           "Señala tres temas propios de Lucas con un texto para cada uno.",
           "¿Por qué Lc 4,16-30 se considera un discurso programático?"]),
        S("Hch 1,1-11; 2; 10; 28,16-31.",
          "Aguirre – Rodríguez Carmona: los Hechos de los Apóstoles. Complementa con Marguerat o Brown.",
          "Los estudios sobre Hechos discuten su valor histórico (por ejemplo, la comparación con las cartas de Pablo) y su género: historiografía antigua, monografía apologética o relato de fundación. "
          "Hoy se valora su intención teológica sin negar que transmite datos fiables. Hch 1,8 ofrece el plan del libro: Jerusalén, Judea y Samaría, hasta los confines de la tierra.",
          ["¿Cómo se relaciona Hch 1,8 con la estructura del libro?",
           "¿Qué diferencias hay entre el Pablo de Hechos y el de las cartas?",
           "¿Qué función tienen los discursos en Hechos?"]),
    ],
)

# =========================================================================
PROGRAMA["se-4"] = M(
    objetivos=[
        "Conocer el estado actual de la investigación sobre la formación del Pentateuco.",
        "Interpretar Gn 1–11 respetando su género literario y su mensaje teológico.",
        "Comprender las tradiciones patriarcales y la teología de la promesa.",
        "Explicar la alianza del Sinaí y la Ley en Éxodo, Levítico, Números y Deuteronomio.",
    ],
    contenidos_minimos="Hipótesis sobre la formación del Pentateuco. Historia de los orígenes. Patriarcas. Éxodo y alianza. Leyes y Deuteronomio.",
    obligatoria=[
        BIBLIA,
        "F. García López, *El Pentateuco. Introducción a la lectura de los cinco primeros libros de la Biblia* (Introducción al estudio de la Biblia 3a), Verbo Divino, Estella 2003.",
        "J.-L. Ska, *Introducción a la lectura del Pentateuco. Claves para la interpretación de los cinco primeros libros de la Biblia*, Verbo Divino, Estella 2001.",
        "Catecismo de la Iglesia Católica, nn. 279-421 (creación y caída) y nn. 2052-2082 (el Decálogo).",
    ],
    complementaria=[
        "J. Blenkinsopp, *El Pentateuco. Introducción a los cinco primeros libros de la Biblia*, Verbo Divino, Estella 1999.",
        "M. Tábet, *Introducción al Antiguo Testamento I. Pentateuco y libros históricos*, Palabra, Madrid.",
        SICRE_AT,
        "G. von Rad, *Teología del Antiguo Testamento*, vol. I, Sígueme, Salamanca.",
        "W. Brueggemann, *Teología del Antiguo Testamento*, Sígueme, Salamanca.",
        JER,
    ],
    online=ONLINE_BASE + [("Pío XII, *Divino afflante Spiritu* (1943): los géneros literarios", DAS)],
    trabajo=("Exégesis de una perícopa del Pentateuco (1.500 a 2.500 palabras): Gn 2,4b-25; Gn 22,1-19; Ex 3,1-15 o Ex 19,1-8. "
             "Sigue estos pasos: delimitación del texto, traducción comparada (dos versiones), estructura, género literario, contexto en el libro, "
             "comentario versículo a versículo, teología y actualización. Cita al menos dos lecturas del programa y un documento del Magisterio."),
    sesiones=[
        S("Gn 1,1–2,4a y 2,4b-25; Ex 3 y 6,2-8 (dos relatos de la revelación del nombre).",
          "García López, *El Pentateuco*: la historia de la investigación. Ska, *Introducción*: los problemas literarios.",
          "La hipótesis documental clásica (Wellhausen, fines del siglo XIX) proponía cuatro fuentes: J, E, D y P. Desde los años 70 (Rendtorff, Van Seters, Blum) se cuestionó la existencia de E y la datación antigua de J. "
          "Hoy predominan modelos que distinguen un material sacerdotal (P), uno no sacerdotal y el Deuteronomio, con una redacción final en época persa. Ska ofrece un panorama accesible de este debate.",
          ["¿Qué observaciones textuales dieron origen a la hipótesis documental?",
           "¿Qué críticas recibió esa hipótesis desde 1970?",
           "¿Por qué es importante el período persa para la redacción final?"]),
        S("Gn 1–11 completo; compara con Sal 104 y Jb 38.",
          "García López: Gn 1–11. Catecismo, nn. 337-390.",
          "Los relatos de los orígenes dialogan con mitos mesopotámicos (Enuma Elish, Atrahasis, Gilgamesh) y los reinterpretan desde la fe monoteísta. "
          "Su verdad no es científica sino teológica: Dios creador, la bondad de lo creado, la dignidad humana, el origen del mal en la libertad. El Catecismo (n. 390) habla de un «lenguaje de imágenes» que afirma un acontecimiento primordial.",
          ["¿Qué semejanzas y diferencias hay entre Gn 6–9 y el relato del diluvio en Gilgamesh?",
           "¿Qué enseña Gn 1 sobre el ser humano?",
           "¿Cómo explicarías a un joven la relación entre Génesis y la ciencia?"]),
        S("Gn 12,1-9; 15; 22; 28,10-22; 37–50 (lectura panorámica).",
          "García López: los relatos patriarcales. Ska: Abraham y la promesa.",
          "La historicidad de los patriarcas fue muy discutida desde los años 70 (Thompson, Van Seters). La investigación actual tiende a ver en estos relatos memorias de grupos y tradiciones locales, reelaboradas en época monárquica y exílica. "
          "Su centro teológico es la promesa (tierra, descendencia, bendición) y la fe de Abraham, que el NT retoma (Rom 4; Heb 11).",
          ["¿Cuáles son los tres elementos de la promesa a Abraham?",
           "¿Cómo relee Pablo la figura de Abraham en Rom 4?",
           "¿Qué valor tiene la historia de José como relato sapiencial?"]),
        S("Ex 1–15; 19–24; 32–34.",
          "García López: el libro del Éxodo. Ska: la perícopa del Sinaí.",
          "El éxodo es el acontecimiento fundador de Israel. Aunque su reconstrucción histórica es difícil, la memoria de liberación está en el corazón de la fe bíblica (Dt 26,5-9). "
          "La alianza del Sinaí se ha comparado con tratados de vasallaje del antiguo Oriente (Mendenhall, McCarthy). El Decálogo aparece en dos versiones (Ex 20 y Dt 5), lo que muestra su uso y su relectura.",
          ["¿Qué diferencias hay entre el Decálogo de Ex 20 y el de Dt 5?",
           "¿Qué relación hay entre la liberación y la Ley en el Éxodo?",
           "¿Cómo relee el NT el éxodo y la Pascua?"]),
        S("Lv 19; Lv 25; Nm 6,22-27; Dt 6,4-9; Dt 30,15-20; Dt 34.",
          "García López: Levítico, Números y Deuteronomio. Catecismo, nn. 2052-2082.",
          "El Levítico pertenece en gran parte a la tradición sacerdotal (P) y a la llamada Ley de santidad (Lv 17–26). "
          "El Deuteronomio se relaciona con la reforma de Josías (2 Re 22–23) y con la teología que inspira la historia deuteronomista (Josué–Reyes), según la tesis de M. Noth. "
          "Jesús cita Dt 6,5 y Lv 19,18 como los dos mandamientos principales (Mc 12,28-34).",
          ["¿Qué significa «santidad» en Lv 19?",
           "¿Qué relación propone la investigación entre el Deuteronomio y la reforma de Josías?",
           "¿Por qué el Shemá (Dt 6,4-9) es central para Israel y para Jesús?"]),
    ],
)

# =========================================================================
PROGRAMA["se-5"] = M(
    objetivos=[
        "Definir el profetismo bíblico y distinguirlo de la adivinación.",
        "Situar a los grandes profetas en su contexto histórico.",
        "Explicar los temas centrales: justicia, alianza, juicio, conversión y esperanza.",
        "Leer los textos mesiánicos en su sentido histórico y en su relectura cristiana.",
    ],
    contenidos_minimos="Fenómeno profético. Profetas del siglo VIII. Jeremías. Ezequiel y Segundo Isaías. Profecía postexílica y mesianismo.",
    obligatoria=[
        BIBLIA,
        "J. L. Sicre, *Introducción al profetismo bíblico*, Verbo Divino, Estella.",
        "J. M. Ábrego de Lacy, *Los libros proféticos* (Introducción al estudio de la Biblia 4), Verbo Divino, Estella 1993; o la nueva edición: S. Ausín – L. Barriocanal – F. Ramis, *Libros proféticos*, Verbo Divino, Estella 2023.",
        "*Dei Verbum*, nn. 14-16.",
    ],
    complementaria=[
        "L. Alonso Schökel – J. L. Sicre, *Profetas. Comentario*, 2 vols., Cristiandad, Madrid 1980.",
        "J. L. Sicre, *Los profetas de Israel y su mensaje*, Cristiandad, Madrid 1986.",
        "G. von Rad, *Teología del Antiguo Testamento*, vol. II, Sígueme, Salamanca.",
        PJ_T,
        JER,
    ],
    online=ONLINE_BASE,
    trabajo=("Exégesis de un oráculo profético (1.500 a 2.500 palabras): Is 6,1-13; Is 52,13–53,12; Jr 31,31-34; Ez 37,1-14 o Am 5,21-24. "
             "Incluye contexto histórico del profeta, estructura y género del texto, comentario, relectura en el NT y una actualización pastoral (justicia, esperanza o conversión)."),
    sesiones=[
        S("1 Sam 3; 1 Re 18; Dt 18,9-22; Am 7,10-17.",
          "Sicre, *Introducción al profetismo bíblico*: el fenómeno profético en Israel y en el antiguo Oriente.",
          "Los textos de Mari (siglo XVIII a.C.) muestran que hubo profecía en el Oriente antiguo; el profetismo bíblico se distingue por su vínculo con la alianza y su crítica social y religiosa. "
          "La investigación distingue entre el profeta histórico, las colecciones de sus discípulos y la redacción final de los libros, que puede extenderse durante siglos.",
          ["¿Qué diferencia al profeta bíblico del adivino?",
           "¿Qué criterios da Dt 18 para reconocer al verdadero profeta?",
           "¿Por qué se distingue entre el profeta y el libro que lleva su nombre?"]),
        S("Am 1–2; 5; Os 1–3; 11; Is 1; 5; 6; 7,10-17; Miq 6,1-8.",
          "Sicre: Amós, Oseas, Isaías y Miqueas. Alonso Schökel – Sicre, *Profetas*, para los textos elegidos.",
          "El siglo VIII es la época de la amenaza asiria y de una fuerte desigualdad social. Amós denuncia la injusticia; Oseas, la infidelidad a la alianza con la imagen del matrimonio; Isaías, la falta de confianza en Dios. "
          "Is 7,14 («la joven está embarazada») es un caso clásico: en su contexto alude a un nacimiento cercano; Mt 1,23 lo relee a partir de la traducción griega («la virgen»).",
          ["¿Qué injusticias denuncia Amós?",
           "¿Cómo usa Oseas la imagen del matrimonio?",
           "Explica la relación entre Is 7,14 y Mt 1,23."]),
        S("Jr 1; 7; 20,7-18; 31,31-34; Lam 1.",
          "Sicre: Jeremías. Ábrego de Lacy o Ausín et al.: el libro de Jeremías.",
          "Jeremías es el profeta del que conservamos más rasgos personales (las «confesiones»). El libro tiene dos formas: el texto hebreo y el griego, más breve y con otro orden, lo que muestra su compleja formación. "
          "Jr 31,31-34, la «nueva alianza», es el texto del AT más citado en Hebreos (Heb 8,8-12).",
          ["¿Qué son las confesiones de Jeremías?",
           "¿Qué critica Jeremías en su discurso del templo (Jr 7)?",
           "¿Qué novedad anuncia Jr 31,31-34?"]),
        S("Ez 1–3; 18; 36,22-28; 37; Is 40,1-11; 42,1-9; 52,13–53,12.",
          "Sicre: Ezequiel y el Segundo Isaías.",
          "Desde fines del siglo XIX se distingue en el libro de Isaías un Segundo Isaías (Is 40–55), profeta del exilio, y un Tercer Isaías (56–66), aunque hoy se insiste más en la unidad redaccional del libro. "
          "Los cantos del Siervo de Yahvé se interpretan de forma individual o colectiva (Israel); el NT los aplica a la pasión de Jesús (Hch 8,32-35).",
          ["¿Qué razones llevan a distinguir Is 40–55 del resto del libro?",
           "¿Quién es el Siervo de Yahvé según las distintas interpretaciones?",
           "¿Qué responsabilidad personal afirma Ez 18?"]),
        S("Ag 1; Zac 9,9-10; Mal 3; Jl 3; Is 61,1-3 y Lc 4,16-21.",
          "Sicre: profecía postexílica y esperanza mesiánica. PCB (2001): la esperanza mesiánica.",
          "Después del exilio la profecía se concentra en la reconstrucción del templo y de la comunidad, y poco a poco da paso a la apocalíptica. "
          "La PCB (2001) recuerda que la esperanza mesiánica de Israel era plural y que los cristianos no deben presentar las profecías como si su cumplimiento en Cristo fuera evidente a cualquier lector: es una lectura de fe.",
          ["¿Qué preocupaciones tienen Ageo y Zacarías?",
           "¿Cómo lee Jesús Is 61 en Nazaret?",
           "¿Qué advierte la PCB sobre la relación entre profecía y cumplimiento?"]),
    ],
)

# =========================================================================
PROGRAMA["se-6"] = M(
    objetivos=[
        "Reconstruir la biografía de Pablo combinando las cartas y Hechos.",
        "Distinguir cartas protopaulinas, deuteropaulinas y pastorales, y explicar los criterios.",
        "Exponer los grandes temas de la teología paulina: justificación, Cuerpo de Cristo, cruz y resurrección.",
        "Analizar un pasaje paulino atendiendo a su argumentación.",
    ],
    contenidos_minimos="Vida y misión de Pablo. Género epistolar y autoría. Gálatas y Romanos. Corintios. Filipenses, Tesalonicenses y escatología.",
    obligatoria=[
        BIBLIA,
        "J. Becker, *Pablo. El apóstol de los paganos*, Sígueme, Salamanca 1996.",
        "H. Lona, *Introducción a Pablo*, Claretiana, Buenos Aires 2011; o U. Vanni, *Las cartas de Pablo*, Claretiana, Buenos Aires 2002.",
        "Benedicto XVI, catequesis sobre san Pablo (audiencias generales 2008-2009), en vatican.va.",
    ],
    complementaria=[
        "G. Bornkamm, *Pablo de Tarso*, Sígueme, Salamanca 1991.",
        "J. Gnilka, *Pablo de Tarso. Apóstol y testigo*, Herder, Barcelona 1998.",
        "S. Vidal, *Las cartas originales de Pablo*, Trotta, Madrid 1996; y *Pablo. De Tarso a Roma*, Sal Terrae, Santander 2008.",
        "P. Debergé, *Pablo, el pastor* (Cuadernos Bíblicos 126), Verbo Divino, Estella.",
        "R. Fabris, *Pablo. El apóstol de las gentes*, San Pablo, Madrid.",
        "F. Bartolomé, *Pablo de Tarso. Una introducción a la vida y obra de un apóstol de Cristo*, CCS, Madrid 1997.",
        BROWN_NT,
    ],
    online=ONLINE_BASE,
    trabajo=("Análisis de un argumento paulino (1.500 a 2.500 palabras): Rom 5,1-11; Gal 2,15-21; 1 Cor 12,12-31; 1 Cor 15,1-28 o Flp 2,5-11. "
             "Describe la situación de la comunidad destinataria, la estructura del pasaje, el razonamiento de Pablo paso a paso, los conceptos clave y su actualidad. "
             "Cita al menos dos lecturas del programa."),
    sesiones=[
        S("Gal 1,11-24; Flp 3,4-14; Hch 9,1-30; 2 Cor 11,21-33.",
          "Becker, *Pablo*: la vida de Pablo y su cronología.",
          "La cronología paulina se apoya en pocos datos firmes; uno es la inscripción de Delfos que permite fechar al procónsul Galión (Hch 18,12) hacia el 51-52. "
          "La «nueva perspectiva sobre Pablo» (E. P. Sanders, J. D. G. Dunn, N. T. Wright) cambió la forma de leer su relación con el judaísmo: Pablo no habría combatido un judaísmo de «méritos», sino las barreras que excluían a los paganos.",
          ["¿Por qué la inscripción de Galión es importante para la cronología?",
           "¿Fue la experiencia de Damasco una «conversión» o una «vocación»? Argumenta.",
           "¿Qué cambia la «nueva perspectiva» en la lectura de Pablo?"]),
        S("1 Tes 1,1-10; Flm; 2 Tes 2,1-2; 3,17; Col 1,15-20.",
          "Lona o Vanni: el género epistolar y la autoría. Brown, *Introducción al NT*: cartas deuteropaulinas.",
          "Siete cartas se aceptan casi unánimemente como de Pablo (Rom, 1-2 Cor, Gal, Flp, 1 Tes, Flm). Para Colosenses, Efesios y 2 Tesalonicenses hay debate; las Pastorales (1-2 Tim, Tit) suelen considerarse posteriores. "
          "La pseudoepigrafía era una práctica de la época y no contradice la inspiración ni la canonicidad, como explica la exégesis católica.",
          ["¿Cuáles son las siete cartas indiscutidas?",
           "¿Qué criterios se usan para discutir la autoría de una carta?",
           "¿Por qué una carta deuteropaulina sigue siendo Palabra de Dios?"]),
        S("Gal 2,15–3,14; Rom 1,16-17; 3,21-31; 5,1-11; 8.",
          "Becker o Vidal: Gálatas y Romanos.",
          "La justificación por la fe fue el centro de la controversia de la Reforma. La *Declaración conjunta sobre la doctrina de la justificación* (Iglesia católica y Federación Luterana Mundial, 1999) expresa un consenso básico sobre este tema. "
          "La expresión *pístis Christou* («fe en Cristo» o «fidelidad de Cristo») es uno de los debates exegéticos actuales.",
          ["¿Qué significa «justificar» en el lenguaje de Pablo?",
           "¿Qué afirma la Declaración conjunta de 1999?",
           "¿Qué cambia si traducimos «fidelidad de Cristo» en lugar de «fe en Cristo»?"]),
        S("1 Cor 1,10-31; 11,17-34; 12–14; 2 Cor 4,7-18; 12,1-10.",
          "Lona o Vanni: la correspondencia corintia. Complementa con Debergé, *Pablo, el pastor*.",
          "Corinto era una ciudad portuaria, rica y diversa. Los estudios sociales (Theissen) muestran tensiones entre ricos y pobres incluso en la cena del Señor (1 Cor 11). "
          "2 Corintios podría ser una reunión de varias cartas; es la carta más personal de Pablo y desarrolla una teología del ministerio desde la debilidad.",
          ["¿Qué problemas comunitarios aborda 1 Corintios?",
           "¿Qué criterio da Pablo para valorar los carismas (1 Cor 12–14)?",
           "¿Qué significa «cuando soy débil, entonces soy fuerte»?"]),
        S("1 Tes 4,13–5,11; Flp 1,21-26; 2,5-11; 1 Cor 15.",
          "Becker o Gnilka: escatología paulina.",
          "1 Tesalonicenses (hacia el año 50) es probablemente el escrito más antiguo del NT. En ella Pablo espera la venida del Señor como cercana; en Filipenses aparece la esperanza de «estar con Cristo» al morir. "
          "Flp 2,6-11 es un himno quizá anterior a Pablo y un testimonio temprano de fe en la preexistencia de Cristo.",
          ["¿Qué preocupación de los tesalonicenses responde 1 Tes 4,13-18?",
           "¿Qué afirma el himno de Flp 2,6-11 sobre Cristo?",
           "¿Cómo argumenta Pablo la resurrección en 1 Cor 15?"]),
    ],
)

# =========================================================================
PROGRAMA["se-7"] = M(
    objetivos=[
        "Caracterizar la sabiduría de Israel y su relación con la sabiduría del antiguo Oriente.",
        "Conocer los géneros de los Salmos y su uso en la liturgia.",
        "Analizar los grandes temas de Proverbios, Job, Qohélet, Sirácida, Cantar y Sabiduría.",
        "Relacionar la sabiduría del AT con la cristología del NT.",
    ],
    contenidos_minimos="Sabiduría bíblica. Salterio. Proverbios y Sirácida. Job y Qohélet. Cantar y Sabiduría.",
    obligatoria=[
        BIBLIA,
        "V. Morla Asensio, *Libros sapienciales y otros escritos* (Introducción al estudio de la Biblia 5), Verbo Divino, Estella 1994.",
        "L. Alonso Schökel – C. Carniti, *Salmos*, 2 vols., Verbo Divino, Estella 1992 (introducción general y comentario de los salmos trabajados).",
        "*Ordenación general de la Liturgia de las Horas*, capítulo III: los salmos en la oración de la Iglesia.",
    ],
    complementaria=[
        "M. Tábet, *Introducción a la lectura de los libros poéticos y sapienciales del Antiguo Testamento*, Palabra, Madrid 2007.",
        "L. Alonso Schökel – J. Vílchez, *Proverbios*, Cristiandad, Madrid 1984.",
        "J. Vílchez Líndez, *Sabiduría*, Verbo Divino, Estella 1990; *Eclesiastés o Qohélet*, Verbo Divino, Estella 1994.",
        "G. von Rad, *Sabiduría en Israel*, Cristiandad / Trotta, Madrid.",
        SICRE_AT,
        JER,
    ],
    online=ONLINE_BASE,
    trabajo=("Comentario de un texto poético o sapiencial (1.500 a 2.500 palabras): Sal 22; Sal 51; Sal 139; Jb 38–42; Qo 3,1-15 o Sab 2,12-24. "
             "Incluye género literario, estructura, paralelismos y figuras, comentario, uso en la liturgia o en el NT y una propuesta de oración comunitaria con el texto."),
    sesiones=[
        S("Prov 1,1-7; 8; 1 Re 3,4-15; 5,9-14.",
          "Morla Asensio: introducción a la literatura sapiencial.",
          "La sabiduría bíblica comparte formas con Egipto y Mesopotamia; Prov 22,17–24,22 tiene paralelos estrechos con la *Instrucción de Amenemope* egipcia. "
          "Su interés es la vida cotidiana y el orden del mundo creado; la figura de la Sabiduría personificada (Prov 8) será clave para la cristología (Jn 1; Col 1).",
          ["¿Qué diferencia la sabiduría de la Ley y los Profetas?",
           "¿Qué paralelo existe entre Proverbios y Amenemope?",
           "¿Cómo se relaciona Prov 8 con Jn 1,1-18?"]),
        S("Sal 1; 2; 8; 22; 51; 110; 150.",
          "Alonso Schökel – Carniti, *Salmos*: introducción. Morla: el Salterio.",
          "H. Gunkel clasificó los salmos por géneros (himnos, súplicas, acción de gracias, reales, sapienciales) y por su lugar vital. "
          "Los estudios recientes atienden también a la composición del Salterio como libro, con cinco partes y un recorrido de la súplica a la alabanza. Jesús ora con los salmos en la cruz (Mc 15,34; Lc 23,46).",
          ["¿Qué géneros de salmos distingue Gunkel?",
           "¿Por qué el Salterio termina con alabanzas?",
           "¿Qué significa que Jesús rezara el Sal 22 en la cruz?"]),
        S("Prov 10; 31,10-31; Sir 1; 24; 44,1-15; 51,13-30.",
          "Morla: Proverbios y Eclesiástico. Alonso Schökel – Vílchez, *Proverbios*.",
          "Ben Sira (hacia el 180 a.C.) une sabiduría y Ley (Sir 24) frente al atractivo de la cultura helenística. "
          "Su texto hebreo se perdió y se recuperó en parte desde 1896 (Genizá del Cairo, Qumrán, Masada); es un libro deuterocanónico, ausente del canon hebreo.",
          ["¿Qué relación establece Sir 24 entre Sabiduría y Ley?",
           "¿Cómo se recuperó el texto hebreo del Sirácida?",
           "¿Qué imagen de la mujer presenta Prov 31 y cómo leerla hoy?"]),
        S("Jb 1–3; 38–42; Qo 1–3; 12.",
          "Morla: Job y Qohélet. Vílchez, *Eclesiastés o Qohélet*.",
          "Job y Qohélet cuestionan la «retribución» simple: el justo no siempre es premiado. Job no recibe una explicación del sufrimiento, sino un encuentro con Dios. "
          "Qohélet, con su «vanidad de vanidades» (*hébel*: soplo), es una crítica lúcida que invita a disfrutar la vida como don.",
          ["¿Qué teoría de la retribución critican Job y Qohélet?",
           "¿Qué responde Dios a Job en los capítulos 38–42?",
           "¿Qué significa *hébel* y cómo cambia la lectura de Qohélet?"]),
        S("Cant 2,8-17; 8,6-7; Sab 1–3; 7,22–8,1; 9.",
          "Morla: Cantar de los Cantares y Sabiduría. Vílchez, *Sabiduría*.",
          "El Cantar se lee en su sentido literal como poesía del amor humano y, en la tradición judía y cristiana, como alegoría del amor entre Dios y su pueblo. Ambas lecturas son legítimas. "
          "Sabiduría, escrita en griego probablemente en Alejandría en el siglo I a.C., desarrolla la esperanza en la inmortalidad del justo (Sab 3).",
          ["¿Por qué un poema de amor humano está en la Biblia?",
           "¿Qué afirma Sab 3,1-9 sobre la muerte del justo?",
           "¿Qué relación hay entre Sab 7,22-30 y Heb 1,3?"]),
    ],
)

# =========================================================================
PROGRAMA["se-8"] = M(
    objetivos=[
        "Conocer las cuestiones de autor, comunidad y composición del cuarto evangelio.",
        "Analizar el prólogo, los signos y los discursos joánicos.",
        "Interpretar el relato de la pasión y resurrección como «hora» de la glorificación.",
        "Explicar la teología de las cartas de Juan.",
    ],
    contenidos_minimos="Cuestión joánica. Prólogo. Libro de los signos. Discursos. Libro de la gloria. Cartas joánicas.",
    obligatoria=[
        BIBLIA,
        "J. O. Tuñí – X. Alegre, *Escritos joánicos y cartas católicas* (Introducción al estudio de la Biblia 8), Verbo Divino, Estella 1995.",
        "R. E. Brown, *La comunidad del discípulo amado*, Sígueme, Salamanca 1983.",
        "H. Lona, *El Evangelio de Juan*, Claretiana, Buenos Aires 2001.",
    ],
    complementaria=[
        "R. E. Brown, *El Evangelio según Juan*, 2 vols., Cristiandad, Madrid 1979.",
        "X. Léon-Dufour, *Lectura del evangelio de Juan*, 4 vols., Sígueme, Salamanca.",
        "Y.-M. Blanchard, Cuadernos Bíblicos 138 (2008) y 170 (2015), Verbo Divino, Estella: el evangelio y las cartas de Juan.",
        BROWN_NT,
        JER,
    ],
    online=ONLINE_BASE + [("Catecismo: Jesús, Palabra hecha carne, nn. 456-483", CEC)],
    trabajo=("Exégesis de un texto joánico (1.500 a 2.500 palabras): Jn 1,1-18; Jn 2,1-11; Jn 4,1-42; Jn 11,1-44 o 1 Jn 4,7-21. "
             "Analiza estructura, simbolismo, malentendidos e ironía joánica, relación con el resto del evangelio y su aporte a la cristología. Cita al menos dos lecturas del programa."),
    sesiones=[
        S("Jn 1,35-51; 13,23-26; 19,25-27.35; 20,1-10; 21,20-25.",
          "Tuñí – Alegre: la cuestión joánica. Brown, *La comunidad del discípulo amado*.",
          "La tradición atribuyó el evangelio a Juan, hijo de Zebedeo. Muchos exegetas hablan hoy de un proceso en varias etapas dentro de una «escuela» o comunidad que se apoya en el testimonio del discípulo amado. "
          "Brown reconstruyó la historia de esa comunidad, incluida su ruptura con la sinagoga; su reconstrucción es influyente pero hipotética. El papiro P52 (hacia el 125-150) es el fragmento más antiguo conocido de un texto del NT.",
          ["¿Quién es el discípulo amado según los distintos autores?",
           "¿Qué etapas propone Brown en la historia de la comunidad joánica?",
           "¿Por qué es importante el papiro P52?"]),
        S("Jn 1,1-18; 2,1-11; 4,46-54; 9; 11.",
          "Lona, *El Evangelio de Juan*: prólogo y libro de los signos.",
          "El prólogo es un himno, quizá reelaborado, que retoma la Sabiduría personificada y Gn 1. Juan habla de «signos», no de milagros: hechos que revelan la gloria y llaman a la fe. "
          "R. Bultmann propuso una «fuente de signos»; hoy se insiste más en la unidad narrativa del texto final.",
          ["¿Qué afirma Jn 1,14 y por qué es central?",
           "¿Qué diferencia hay entre «signo» y «milagro»?",
           "¿Qué proceso de fe recorre el ciego de nacimiento en Jn 9?"]),
        S("Jn 3,1-21; 6; 8,12-59; 10; 14–17.",
          "Tuñí – Alegre o Léon-Dufour: discursos y «Yo soy».",
          "Los discursos joánicos usan malentendidos (Nicodemo, la samaritana), ironía y lenguaje simbólico (luz, agua, pan, vida). "
          "Los «Yo soy» absolutos (Jn 8,58) evocan el nombre divino de Ex 3,14 y la versión griega de Is 43,10. El discurso del pan de vida (Jn 6) se relaciona con la eucaristía, aunque Juan no narra su institución.",
          ["¿Cómo funciona el malentendido en el diálogo con Nicodemo?",
           "¿Qué alusión al AT tienen los «Yo soy» absolutos?",
           "¿Por qué Juan no narra la institución de la eucaristía?"]),
        S("Jn 13,1-20; 18–20.",
          "Lona o Brown: el libro de la gloria.",
          "En Juan la cruz es exaltación y glorificación: la «hora» de Jesús. La cronología joánica sitúa la muerte de Jesús en la víspera de Pascua, cuando se sacrificaban los corderos, lo que difiere de los sinópticos. "
          "Jn 20,30-31 expresa el propósito del evangelio: creer para tener vida.",
          ["¿Qué significa la «hora» de Jesús en Juan?",
           "¿Qué diferencia cronológica hay entre Juan y los sinópticos en la pasión?",
           "¿Qué propósito declara Jn 20,30-31?"]),
        S("1 Jn 1,1-4; 2,18-27; 4,1-21; 2 Jn; 3 Jn.",
          "Tuñí – Alegre: las cartas de Juan. Brown, *La comunidad del discípulo amado* (cismas en la comunidad).",
          "1 Juan responde a una crisis interna: algunos «salieron» de la comunidad (1 Jn 2,19) y negaban que Jesús hubiera venido «en la carne» (1 Jn 4,2). "
          "Contra ello, la carta une confesión de fe y amor fraterno. «Dios es amor» (1 Jn 4,8.16) dio título a la primera encíclica de Benedicto XVI (*Deus caritas est*, 2005).",
          ["¿Qué crisis comunitaria refleja 1 Juan?",
           "¿Qué relación establece la carta entre fe y amor al hermano?",
           "¿Qué diferencias de tono hay entre 1 Jn y 2-3 Jn?"]),
    ],
)

# =========================================================================
PROGRAMA["se-9"] = M(
    objetivos=[
        "Explicar el género, la estructura y la cristología sacerdotal de Hebreos.",
        "Conocer las características de la literatura apocalíptica.",
        "Interpretar el Apocalipsis en su contexto histórico y litúrgico, evitando lecturas fundamentalistas.",
        "Relacionar ambos escritos con la esperanza cristiana y la liturgia.",
    ],
    contenidos_minimos="Hebreos: género y estructura; Cristo sumo sacerdote; fe y perseverancia. Apocalíptica. Apocalipsis: estructura, símbolos, contexto e interpretación.",
    obligatoria=[
        BIBLIA,
        "A. Vanhoye, *El mensaje de la carta a los Hebreos* (Cuadernos Bíblicos 19), Verbo Divino, Estella 1978.",
        "L. H. Rivas, *La carta a los Hebreos*, Claretiana, Buenos Aires 2007.",
        "U. Vanni, *Apocalipsis. Una asamblea litúrgica interpreta la historia*, Verbo Divino, Estella 1982.",
    ],
    complementaria=[
        "A. Vanhoye, *La cristología sacerdotal de la carta a los Hebreos*, CEA, Buenos Aires 1997.",
        "J.-M. Carrière, *¡Resistid! La carta a los Hebreos* (Cuadernos Bíblicos 151), Verbo Divino, Estella 2011.",
        "L. Dussaut, «La carta a los Hebreos», en *Introducción crítica al Nuevo Testamento* (Introducción a la Biblia 10), Cristiandad, Madrid 1985.",
        "J. O. Tuñí – X. Alegre, *Escritos joánicos y cartas católicas* (Introducción al estudio de la Biblia 8), Verbo Divino, Estella 1995: el Apocalipsis.",
        "E. Cuvillier, Cuadernos Bíblicos 110 (2002), Verbo Divino, Estella: el Apocalipsis.",
        BROWN_NT,
    ],
    online=ONLINE_BASE + [("Catecismo: «Creo en la vida eterna», nn. 1020-1060", CEC)],
    trabajo=("Exégesis de un texto (1.500 a 2.500 palabras): Heb 4,14–5,10; Heb 11,1-12,3; Ap 1,9-20; Ap 5; Ap 12 o Ap 21,1-8. "
             "Explica el género, el contexto histórico, los símbolos y su trasfondo en el AT, la estructura y el mensaje para la Iglesia de entonces y de hoy. "
             "Incluye una crítica breve de una lectura fundamentalista del texto, si existe."),
    sesiones=[
        S("Heb 1,1–2,18; 4,14–5,10; 7.",
          "Vanhoye, *El mensaje de la carta a los Hebreos*; Rivas, *La carta a los Hebreos*: introducción.",
          "Hebreos no es de Pablo, como ya advertían Orígenes y otros Padres; su autor es desconocido. Más que una carta es un sermón u homilía («palabra de exhortación», Heb 13,22). "
          "A. Vanhoye propuso una estructura concéntrica basada en indicios literarios, muy influyente en la exégesis. La cristología sacerdotal de Hebreos es única en el NT.",
          ["¿Por qué se dice que Hebreos es una homilía?",
           "¿Qué argumentos hay contra la autoría paulina?",
           "¿Qué significa que Cristo es sacerdote «según el orden de Melquisedec»?"]),
        S("Heb 8–10; 11; 12,1-13; 13,7-17.",
          "Rivas o Vanhoye: la nueva alianza. Carrière, *¡Resistid!*: la exhortación a la perseverancia.",
          "Hebreos cita Jr 31,31-34 para mostrar que la alianza nueva perfecciona el culto antiguo. Ciertas expresiones (Heb 8,13) han sido usadas en sentido antijudío; la PCB (2001) pide leerlas en su contexto. "
          "La galería de testigos de Heb 11 presenta la fe como confianza que persevera en la prueba.",
          ["¿Qué relación propone Hebreos entre el culto antiguo y el sacrificio de Cristo?",
           "¿Cómo define la fe Heb 11,1?",
           "¿Cómo evitar una lectura antijudía de Heb 8,13?"]),
        S("Dn 7; Dn 12; Mc 13; Ap 1.",
          "Vanni, *Apocalipsis*: introducción. Cuvillier, Cuadernos Bíblicos 110.",
          "La apocalíptica (Daniel, Henoc, 4 Esdras) es literatura de crisis: usa visiones, símbolos y números para afirmar que Dios es señor de la historia. "
          "La mayoría de los exegetas sitúan el Apocalipsis en Asia Menor hacia fines del reinado de Domiciano (años 90), aunque se discute la intensidad de la persecución. "
          "Vanni subraya su marco litúrgico: una asamblea que lee e interpreta la historia (Ap 1,3).",
          ["¿Qué rasgos tiene el género apocalíptico?",
           "¿Qué significa que el Apocalipsis es un libro de esperanza y no de miedo?",
           "¿Qué importancia tiene el marco litúrgico de Ap 1,3?"]),
        S("Ap 2–3; 4–5; 12; 13; 17–18.",
          "Vanni: los símbolos. Tuñí – Alegre: el Apocalipsis.",
          "Los símbolos del Apocalipsis provienen sobre todo del AT (Ezequiel, Daniel, Zacarías). El número 666 se interpreta comúnmente por gematría como «Nerón César»; la «bestia» y «Babilonia» aluden al poder imperial romano. "
          "La PCB (1993) advierte contra lecturas fundamentalistas que buscan en el libro un calendario del fin del mundo.",
          ["¿Qué significa el Cordero degollado y de pie (Ap 5,6)?",
           "¿Qué representan la bestia y Babilonia en su contexto?",
           "¿Por qué es peligroso leer el Apocalipsis como un calendario?"]),
        S("Ap 19,11–22,21; Is 65,17-25; 2 Pe 3,8-13.",
          "Vanni: la Jerusalén nueva. Catecismo, nn. 1042-1050.",
          "El milenio (Ap 20) dio lugar a lecturas literales (milenarismo) que la Iglesia rechazó (Catecismo, n. 676). La tradición agustiniana lo interpretó como el tiempo de la Iglesia. "
          "La Jerusalén nueva (Ap 21–22) es la imagen de la comunión plena de Dios con la humanidad y de la creación renovada. El libro termina con la oración litúrgica *Maranathá*: «Ven, Señor Jesús».",
          ["¿Qué es el milenarismo y qué dice el Catecismo sobre él?",
           "¿Qué imágenes usa Ap 21–22 para la plenitud?",
           "¿Cómo inspira el Apocalipsis la esperanza y el compromiso hoy?"]),
    ],
)


# Lecturas gratuitas en línea (acceso abierto verificado) -------------------
BIBLIA_URL = "https://www.vatican.va/archive/ESL0506/_INDEX.HTM"
BIBLIA_T = "*El Libro del Pueblo de Dios. La Biblia* (traducción argentina), texto completo en vatican.va"
UCA = "https://repositorio.uca.edu.ar/handle/123456789/"
A_FERRADA_11 = ("A. Ferrada Moreira, «Teología e historia en el Antiguo Testamento», *Teología y Vida* 52/3 (2011)", "https://www.redalyc.org/pdf/322/32221381003.pdf")
A_FERRADA_13 = ("A. Ferrada Moreira, «La mediación de Moisés: autoridad e historia», *Teología y Vida* 54/3 (2013)", "https://scielo.conicyt.cl/scielo.php?script=sci_arttext&pid=S0049-34492013000300011")
A_CHUECAS = ("I. Chuecas, «Tendencias actuales en los estudios del Antiguo Testamento. Desafíos y oportunidades», *Teología y Vida* 53 (2012)", "http://teologiayvida.uc.cl/index.php/tyv/article/view/6762")
A_NAPOLE = ("G. M. Nápole, «“Lo que nuestros padres nos contaron” (Sal 78,3): el Antiguo Testamento y la historia de Israel», UCA (2021)", UCA + "11908")
A_RODELAS = ("J. M. Díaz Rodelas, «Inspiración y verdad de la Sagrada Escritura. La aportación del reciente documento de la Pontificia Comisión Bíblica»", RODELAS)
A_MORENO = ("A. Moreno Casamitjana, «El Pueblo de Dios en el Antiguo Testamento», *Teología y Vida* 26 (1985)", "https://repositorio.uc.cl/handle/11534/15233")
A_ANDINACH = ("P. R. Andiñach, «La teología y las teologías del Antiguo Testamento» (2019)", UCA + "12353")
A_RUIZ = ("E. Ruiz, «A 30 años de *La interpretación de la Biblia en la Iglesia*», *Teología* 60/142 (2023)", RUIZ)
A_RIVAS_DISC = ("L. H. Rivas, «Discípulos para la misión en el Nuevo Testamento», *Teología* 44/94 (2007)", UCA + "18041")
A_RIVAS_LC = ("L. H. Rivas, «“Nosotros esperábamos…” (Lc 24,21)», *Teología* 53/121 (2016)", UCA + "7313")
A_ALEGRE = ("X. Alegre, «Marcos o la corrección de una ideología triunfalista. Pautas para la lectura de un evangelio beligerante y comprometido», *Revista Latinoamericana de Teología*", "https://revistas.uca.edu.sv/index.php/rlt/article/download/6184/6119")
A_TRIANA = ("J. Y. Triana Rodríguez – I. A. Méndez Paniagua, «Experimentar el paso de Dios: diálogo entre exégesis, teología y tradición en Ex 33,12-23», *Theologica Xaveriana* 71 (2021)", "https://revistas.javeriana.edu.co/index.php/teoxaveriana/article/view/33347")
A_RIVAS_VIDA = ("L. H. Rivas, «“Para que tengan vida…”» (el Deuteronomio y los escritos joánicos), *Teología* 45/95 (2008)", UCA + "18011")
A_DOCE = ("D. A. Torino – L. A. Verdini, *Los doce profetas*, Santa María, Buenos Aires 2015 (libro completo en acceso abierto)", UCA + "11231")
A_BRAVO = ("A. Bravo, «Los profetas y san Pablo en la carta a los Gálatas», *Cuestiones Teológicas* 36/86 (2009)", "https://core.ac.uk/download/350031747.pdf")
A_ESPINDOLA = ("L. Espíndola García, «La nueva creación en el pensamiento de Pablo», *Veritas* 35 (2016)", "https://www.redalyc.org/pdf/2911/291147541010.pdf")
A_CAPB_EST = ("A. C. Capboscq, «Atanasio: teólogo, exégeta y maestro de espiritualidad. Aspectos de su “Carta a Marcelino”», *Teología* 59/137 (2022)", "https://doi.org/10.46553/teo.59.137.2022.p30-58")
A_CAPB_TXT = ("San Atanasio, *Carta a Marcelino sobre los Salmos*, trad. A. C. Capboscq, *Teología* 59/137 (2022)", UCA + "13826")
A_LIMA = ("M. de L. Lima, «Alegria e riso em meio à fugacidade da vida» (Qohélet), *Teología y Vida* 62 (2021), en portugués", "http://teologiayvida.uc.cl/index.php/tyv/article/view/38509")
A_RIVAS_JN = ("L. H. Rivas, «El conocimiento de Dios en el Evangelio de San Juan», *Teología* 51/114 (2014)", UCA + "7150")
A_RIVAS_MANA = ("L. H. Rivas, «Las tradiciones sobre el maná y el capítulo VI del Evangelio de San Juan», *Teología* 22/45 (1985), número completo", UCA + "6748")
A_TUNI = ("J. O. Tuñí, «Teología judía y cristología joánica», *Revista Latinoamericana de Teología*", "https://revistas.uca.edu.sv/index.php/rlt/article/download/5255/5222/17042")
A_FERNANDEZ = ("V. M. Fernández, «La vida sacerdotal de los cristianos según la carta a los Hebreos», *Revista Bíblica* 52 (1990)", UCA + "7865")
A_MENDOZA = ("C. B. Mendoza, «“Conozco tus obras…” (Ap 2,2.19; 3,1.8.15)» (fidelidad martirial en el Apocalipsis), *Teología* 59/139 (2022), número completo", UCA + "15708")

# Por módulo: lecturas en línea de cada sesión (1 a 5)
LIBRES = {
    "se-1": {1: [], 2: [A_FERRADA_11], 3: [A_NAPOLE], 4: [A_RODELAS, A_CHUECAS], 5: [A_MORENO]},
    "se-2": {1: [], 2: [], 3: [], 4: [A_RIVAS_DISC], 5: [A_RUIZ]},
    "se-3": {1: [], 2: [A_ALEGRE], 3: [A_RIVAS_DISC], 4: [A_RIVAS_LC], 5: []},
    "se-4": {1: [A_TRIANA, A_CHUECAS], 2: [], 3: [A_FERRADA_11], 4: [A_FERRADA_13], 5: [A_RIVAS_VIDA]},
    "se-5": {1: [A_CHUECAS], 2: [A_DOCE], 3: [], 4: [A_BRAVO], 5: [A_DOCE]},
    "se-6": {1: [A_BRAVO], 2: [], 3: [A_BRAVO], 4: [A_ESPINDOLA], 5: []},
    "se-7": {1: [A_CHUECAS, A_ANDINACH], 2: [A_CAPB_TXT, A_CAPB_EST], 3: [], 4: [A_LIMA], 5: []},
    "se-8": {1: [A_TUNI], 2: [A_RIVAS_JN], 3: [A_RIVAS_MANA], 4: [], 5: [A_RIVAS_VIDA]},
    "se-9": {1: [], 2: [A_FERNANDEZ], 3: [], 4: [A_MENDOZA], 5: []},
}


MAGIS = ("*Dei Verbum*", "Catecismo", "*Ordenación", "Benedicto XVI, catequesis")


def _magis(p):
    return [x for x in p["obligatoria"][1:] if x.startswith(MAGIS)]


def _libros(p):
    return [x for x in p["obligatoria"][1:] if not x.startswith(MAGIS)] + p["complementaria"]


def _articulos(mid):
    vistos, out = set(), []
    for n in range(1, 6):
        for a in LIBRES[mid][n]:
            if a[1] not in vistos:
                vistos.add(a[1]); out.append(a)
    return out


# Presentación --------------------------------------------------------------
HORAS = 30
CARGA = ("| Actividad | Horas |\n|---|---|\n"
         "| 5 sesiones de clase (90 min cada una) | 7,5 |\n"
         "| Lectura bíblica, lecturas en línea y estudio personal (3,5 h por sesión) | 17,5 |\n"
         "| Trabajo escrito | 3,5 |\n"
         "| Sesión de cierre: taller y evaluación final | 1,5 |\n"
         "| **Total** | **30** |")


def _lista(xs):
    return "\n".join(f"- {x}" for x in xs)


def _links(xs):
    return "\n".join(f"- [{t}]({u})" for t, u in xs)


def programa_md(mid, intro):
    p = PROGRAMA[mid]
    return "\n\n".join([
        intro,
        "#### Objetivos",
        _lista(p["objetivos"]),
        "#### Contenidos mínimos",
        p["contenidos"],
        "#### Carga horaria",
        CARGA,
        "#### Lecturas obligatorias (gratuitas, en línea)",
        _lista([f"[{BIBLIA_T}]({BIBLIA_URL}).",
                "Los textos de las cinco sesiones de este módulo, con su pestaña «Lecturas y estudio».",
                "Documentos de la Iglesia:"]) + "\n" + "\n".join([f"  - {x}" for x in _magis(p)] + [f"  - [{t}]({u})" for t, u in p["online"]]),
        "#### Artículos académicos de acceso abierto",
        _links(_articulos(mid)) if _articulos(mid) else "Este módulo se apoya en los textos de las sesiones y en los documentos de la Iglesia.",
        "#### Para profundizar (en bibliotecas)",
        "Manuales de referencia en español. No son obligatorios: úsalos si tienes acceso a la biblioteca de un seminario, una parroquia o una universidad.\n\n" + _lista(_libros(p)),
        "#### Trabajo escrito",
        p["trabajo"] + "\n\nSe entrega a tu relator antes de la sesión de cierre. Extensión indicada, citas con autor, título, editorial y año.",
        "#### Evaluación y aprobación",
        _lista([
            "Asistencia o lectura completa de las 5 sesiones.",
            "Trabajo escrito aprobado por el relator (rúbrica: comprensión del texto 40 %, uso de las lecturas 30 %, claridad y redacción 20 %, aplicación pastoral 10 %).",
            "Evaluación final en la plataforma con un mínimo de 70 %.",
        ]),
        "*Programa elaborado con referencia a los programas de Sagrada Escritura de la Facultad de Teología de la Pontificia Universidad Católica Argentina. "
        "Todas las lecturas obligatorias son gratuitas y están enlazadas; los libros se citan sin páginas.*",
    ])


def estudio_md(mid, n):
    s = PROGRAMA[mid]["sesiones"][n - 1]
    return "\n\n".join([
        "### Lecturas y estudio (3 h 30 min)",
        "#### Lectura bíblica",
        s["biblia"] + f" Puedes leerla en [El Libro del Pueblo de Dios]({BIBLIA_URL}).",
        "#### Lectura en línea",
        _links(LIBRES[mid][n]) if LIBRES[mid][n] else "Para esta sesión basta con la lectura bíblica y el estado de la cuestión.",
        "#### Si tienes acceso a una biblioteca",
        s["manual"],
        "#### Estado de la cuestión",
        s["profundizacion"],
        "#### Preguntas de estudio",
        "\n".join(f"{i}. {q}" for i, q in enumerate(s["preguntas"], 1)),
        "*Responde por escrito en tu cuaderno: estas preguntas preparan el trabajo escrito y la evaluación final.*",
    ])


def taller_md(mid, taller):
    return taller + "\n\n#### Trabajo escrito del módulo\n\n" + PROGRAMA[mid]["trabajo"]
