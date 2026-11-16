"""Piezas comunes del curso «Profundización ISE» (Integridad en el Servicio Eclesial, CECh 2020)."""
from cd_base import u, q  # noqa: F401

ISE_PDF = "https://www.iglesia.cl/prevenirabusos/documentos/ise.pdf"
ISE_WEB = "https://www.iglesia.cl/prevenirabusos/ise/"
PREV = "https://www.iglesia.cl/prevenirabusos/"
CYE = "https://www.iglesia.cl/documentos_sac/27052015_938am_5565bacb65812.pdf"
FORM_DENUNCIA = "https://www.iglesia.cl/prevenirabusos/documentos/FORMULARIO_Recepcion_denuncias.pdf"
CARTA_PD = "https://www.vatican.va/content/francesco/es/letters/2018/documents/papa-francesco_20180820_lettera-popolo-didio.html"
CARTA_CHILE = "https://www.vatican.va/content/francesco/es/letters/2018/documents/papa-francesco_20180531_lettera-popolodidio-cile.pdf"
VELM = "https://www.vatican.va/content/francesco/es/motu_proprio/documents/20230325-motu-proprio-vos-estis-lux-mundi-aggiornato.html"
EG = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20131124_evangelii-gaudium.html"
CV = "https://www.vatican.va/content/francesco/es/apost_exhortations/documents/papa-francesco_esortazione-ap_20190325_christus-vivit.html"
LS = "https://www.vatican.va/content/francesco/es/encyclicals/documents/papa-francesco_20150524_enciclica-laudato-si.html"
FT = "https://www.vatican.va/content/francesco/es/encyclicals/documents/papa-francesco_20201003_enciclica-fratelli-tutti.html"
DCE = "https://www.vatican.va/content/benedict-xvi/es/encyclicals/documents/hf_ben-xvi_enc_20051225_deus-caritas-est.html"
LG = "https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19641121_lumen-gentium_sp.html"
CDSI = "https://www.vatican.va/roman_curia/pontifical_councils/justpeace/documents/rc_pc_justpeace_doc_20060526_compendio-dott-soc_sp.html"
CDC = "https://www.vatican.va/archive/ESL0506/_INDEX.HTM"
PDV = "https://www.vatican.va/content/john-paul-ii/es/apost_exhortations/documents/hf_jp-ii_exh_25031992_pastores-dabo-vobis.html"


def ise(ref, texto):
    return (f"Integridad en el Servicio Eclesial, {ref}", ISE_PDF, texto)


C_CARTA_PD = ("Francisco, Carta al Pueblo de Dios (20 de agosto de 2018)", CARTA_PD,
              "Parte de la frase de san Pablo «si un miembro sufre, todos sufren con él». Reconoce los abusos sexuales, de poder y de conciencia, pide decir no a toda forma de clericalismo y llama a todo el Pueblo de Dios a construir una cultura del cuidado.")
C_CARTA_CHILE = ("Francisco, Carta al Pueblo de Dios que peregrina en Chile (31 de mayo de 2018)", CARTA_CHILE,
                 "Pide un «nunca más» a la cultura del abuso y al sistema de encubrimiento que la hace posible, y recuerda que la renovación de la Iglesia necesita la participación de todo el Pueblo de Dios.")
C_VELM = ("Francisco, Vos estis lux mundi (versión definitiva de 2023)", VELM,
          "Norma universal de la Iglesia sobre la recepción de informes de abuso: obliga a clérigos y consagrados a informar, pide a cada diócesis un organismo u oficina de fácil acceso para recibirlos y protege de represalias a quien informa.")
C_CYE = ("Cuidado y Esperanza. Líneas Guía de la Conferencia Episcopal de Chile (2015)", CYE,
         "Líneas guía de los obispos de Chile para tratar los casos de abuso sexual a menores de edad; su capítulo IV se dedica a la prevención y a los ambientes sanos y seguros.")

R_ISE = ("Integridad en el Servicio Eclesial (texto completo)", ISE_PDF, "El documento de la Conferencia Episcopal de Chile que estudia este curso.")
R_PREV = ("Prevención de abusos · Conferencia Episcopal de Chile", PREV, "Sitio oficial con los documentos, las buenas prácticas y los canales de denuncia.")

NOTA_VIGENCIA = ("*El ISE fue aprobado «ad experimentum» por tres años (2020-2022). Revisa en el sitio de prevención de la Conferencia Episcopal "
                 "y en tu diócesis cuál es la versión y las normas vigentes hoy.*")
