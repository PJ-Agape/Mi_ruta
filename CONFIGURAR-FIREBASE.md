# Activar las cuentas de Mi Ruta (Firebase)

Con esta configuración, cada participante crea su cuenta con Google o con su correo y una contraseña, su avance lo acompaña en todos sus dispositivos, los relatores aprueban cuentas e inscriben en cursos desde **Gestión**, y las constancias se pueden verificar con su código.

Mientras no hagas estos pasos, Mi Ruta sigue funcionando como hasta ahora: en modo local, sin cuentas.

Usa el **plan gratuito (Spark)** de Firebase: no pide tarjeta y alcanza de sobra para empezar.

## 1. Crear el proyecto

1. Entra a <https://console.firebase.google.com> con una cuenta de Google del equipo (ideal: una cuenta compartida, no personal).
2. **Crear un proyecto** con el nombre `mi-ruta`. Puedes desactivar Google Analytics.

## 2. Activar los métodos de ingreso

1. Menú **Compilación → Authentication → Comenzar**.
2. Pestaña **Método de acceso**:
   - **Google → Habilitar** → elige un correo de asistencia → **Guardar**.
   - **Correo electrónico/contraseña → Habilitar** (solo la primera opción, no la de «vínculo de correo») → **Guardar**.
3. Pestaña **Configuración → Dominios autorizados → Agregar dominio** → `pj-agape.github.io`.
4. Opcional: en **Plantillas**, cambia el idioma de los correos (verificación y recuperar contraseña) a español.

## 3. Crear la base de datos

1. **Compilación → Firestore Database → Crear base de datos**.
2. Ubicación: `southamerica-west1` (Santiago) si aparece; si no, `southamerica-east1` (São Paulo). **No se puede cambiar después.**
3. Elige **modo de producción**.

## 4. Pegar las reglas de seguridad

1. En Firestore Database, pestaña **Reglas**.
2. Borra lo que haya y pega el contenido completo del archivo `firestore.rules` de este repositorio.
3. Reemplaza `tu_correo@gmail.com` por el correo de Google de quien será el **primer administrador**, en minúsculas. Puedes poner más de uno: `['correo1@gmail.com', 'correo2@gmail.com']`.
4. **Publicar**.

Las reglas son las que protegen los datos: las cuentas nuevas quedan pendientes hasta que un relator las aprueba, cada persona escribe solo su propio avance, las notas personales son privadas y solo el equipo emite constancias.

## 5. Conectar la plataforma

1. En Firebase: ícono de engranaje → **Configuración del proyecto** → sección **Tus apps** → ícono web `</>`.
2. Nombre: `Mi Ruta web` (no marques Hosting) → **Registrar app**.
3. Copia el bloque `firebaseConfig` que aparece.
4. En `assets/config.js` de este repositorio:
   - reemplaza `firebase: null,` por `firebase: { ...lo que copiaste... },`
   - en `administradores: []` pon el mismo correo del paso 4: `administradores: ["tu_correo@gmail.com"]`.
5. Sube el cambio a GitHub (o pídeselo a Claude).

Estos datos no son secretos: están pensados para ir en una página pública. La seguridad la dan las reglas del paso 4.

## 6. Primer ingreso

1. Abre Mi Ruta, toca **Ingresar** → **Continuar con Google** con el correo administrador. Tu cuenta se crea activa y como administrador.
2. Entra a **Gestión**. Desde ahí:
   - **Por revisar:** aprueba las cuentas nuevas y las solicitudes de inscripción.
   - **Participantes:** habilita o quita cursos, pon cuentas en pausa y, si eres administrador, cambia roles (participante, relator, administrador).
   - **Ver avance y emitir constancias:** revisa el avance de cada persona y emite su constancia cuando corresponda.

## Roles

| Rol | Qué puede hacer |
| --- | --- |
| Participante | Cursar los cursos habilitados, guardar su avance y ver sus constancias |
| Relator | Además: vista relator (guías y todos los módulos), aprobar cuentas, inscribir participantes, ver avances y emitir constancias |
| Administrador | Además: cambiar roles y eliminar datos |

## Qué se guarda y dónde

| Dato | Colección | Quién lo ve |
| --- | --- | --- |
| Nombre, correo, comunidad, rol, estado, cursos | `usuarios` | La persona y el equipo |
| Clases completadas y evaluaciones | `avance` | La persona y el equipo |
| Bitácora, plantillas y casillas de práctica | `notas` | Solo la persona |
| Constancias emitidas | `constancias` | Cualquiera que tenga el código (para verificar) |

## Si algo no funciona

- **«Esta app no está autorizada»** al ingresar con Google: falta agregar `pj-agape.github.io` en los dominios autorizados (paso 2.3).
- **«No tienes permiso»** al aprobar o emitir: revisa que las reglas estén publicadas y que el correo del administrador esté bien escrito en el paso 4.
- **Una persona no recibe el correo para recuperar la contraseña:** que revise la carpeta de spam.
