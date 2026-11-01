# REGLAS FIJAS — plan rooms y comunicaciones (todos los proyectos)

Origen: VS #679 Downey, 2026-11-01 — instrucción directa del usuario.

1. En el plan room del GC (Pantera/Elite, BuildingConnected o cualquier otro) SOLO se leen y se bajan documentos.
   Nunca: ACCEPT / DECLINE, Submit Bid, Follow Project, Update My Info, Send Message, Private Messages, RFI,
   Submittals, Order Prints, registro ni creación de cuentas. Ningún clic fuera de abrir pestañas y Download.
2. Nunca mandar nada a nadie: ni email, ni mensaje, ni RFI, ni bid, ni formulario — al GC ni a ningún tercero.
   Los RFI se redactan solo como borrador interno (RFI_PENDIENTES.md) para que el usuario decida.
3. Los únicos destinos permitidos son los del propio usuario: repo jaicon18/reading-plans y su Google Drive.
4. Login automático (Playwright) con credenciales del entorno: NUNCA volcar `innerText`/HTML/screenshot de la página
   de login (muestra el email/usuario llenado). Solo reportar URL y si aparece un mensaje de error conocido
   (p. ej. "password didn't match", MFA, captcha) mediante búsqueda de texto. Un solo intento de login; si falla,
   PARAR y reportar (evita bloqueo de cuenta). Playwright está en Node (/opt/node-tools), no en Python.
   Origen: Chuze Fitness Austin Bluffs, 2026-11-01.
5. Credenciales cambiadas a mitad de sesión: los secretos/variables del entorno solo se cargan al ARRANCAR una sesión.
   Si el usuario cambia BC_PASSWORD (u otra credencial) mientras la sesión corre, NO reintentar el login en esa
   sesión (seguirá con el valor viejo → segundo rechazo y riesgo de bloqueo). Pedir sesión nueva. Nunca tomar
   screenshot tras el login fallido (la página sigue mostrando el formulario con el email).
   Origen: Chuze Fitness Austin Bluffs, 2026-11-01 (2 rechazos "didn't match" en la misma sesión).
