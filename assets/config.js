/* Configuración de Mi Ruta.

   Mientras firebase sea null, la plataforma funciona en modo local: sin cuentas,
   con los avances guardados solo en el navegador.

   Para activar las cuentas, sigue CONFIGURAR-FIREBASE.md y pega aquí el bloque
   firebaseConfig de tu proyecto. Estos datos no son secretos: la seguridad la
   dan las reglas de Firestore (firestore.rules). */
window.MIRUTA_CONFIG = {
  firebase: {
    apiKey: "AIzaSyAK942g5nKGomgTmO6iTP5zgrmJxBjnWzU",
    authDomain: "mi-ruta-12352.firebaseapp.com",
    projectId: "mi-ruta-12352",
    storageBucket: "mi-ruta-12352.firebasestorage.app",
    messagingSenderId: "926757532439",
    appId: "1:926757532439:web:7636464964c5b8222d3d52"
  },
  // Correos de Google de los primeros administradores (en minúsculas).
  // Deben coincidir con los que pongas en firestore.rules.
  administradores: ["iperezconus84@gmail.com"]
};
