/* Configuración de Mi Ruta.

   Mientras firebase sea null, la plataforma funciona en modo local: sin cuentas,
   con los avances guardados solo en el navegador.

   Para activar las cuentas, sigue CONFIGURAR-FIREBASE.md y pega aquí el bloque
   firebaseConfig de tu proyecto. Estos datos no son secretos: la seguridad la
   dan las reglas de Firestore (firestore.rules). */
window.MIRUTA_CONFIG = {
  firebase: null,
  // Correos de Google de los primeros administradores (en minúsculas).
  // Deben coincidir con los que pongas en firestore.rules.
  administradores: []
};
