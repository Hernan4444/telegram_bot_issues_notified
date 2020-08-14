# Aplicación en Flask para notificación de issues.

Esta pequeña aplicación sirve para conectar un bot de telegram con un repositorio de Github y notificar cuando un alumno haga alguna issue o comentario. Tambien permite ejecutar el comando `\github` que retorna las issues pendientes. Una issue pendiente se define como aquellas abiertas donde no hay respuesta o el último comentario es de un alumno.

El **teacher_assistant.txt** indica los usuarios que son ayudantes para omitir la notificación en caso de que ellos hagan issues.

El archivo **funciones.py** contiene en el `if __name__ == "__main__":` una subrutina para resumir la cantidad de issues y comentarios en donde participaron los ayudantes del archivo **teacher_assistant.txt**.

El archivo **generador de webhooks.py** se encarga de conectar el bot con una URL para los webhook de telegram.

Variables de entorno:

* `TELEGRAM_USER`: Nombre de usuario de telegram capaz de ejecutar el comando `\github`.
* `ORGANIZATION`: Nombre de la organización de Github donde están las issues.
* `REPO`: Repositorio de Github donde están las issues.
* `ID_COURSE`: ID del chat donde el bot mandará los mandejes o por donde aceptará ejecutar el comando `\github`.
* `ID_PERSONAL`: ID del chat entre el usuario que adminstra el bot y el bot. Por ejemplo, `176690304` para bot `HernyBot` y el usuario `HernyV`.
* `TOKEN`: Token del bot.
* `DESTINATION`: URL para conectar el webhook del bot con algún endpoint de la api en Flask.
* `FLASK_APP`: En caso de ejecutar en Heroku, esta variable debe indicar cual es el archivo a ejecutar de flask. Por defecto debe ser `main.py`
* `USER`: Nombre del usuario de github para poder no tener un límite de request tan bajo al momento de ejecutar el comando `\github`
* `PASSWORD`: Token personal del usuario de github


## Sugerencias de como hacer funcionar todo

1. Setear webhook con el **generador de webhooks.py**.
2. Subir código al servidor y definir `ID_COURSE` e `ID_PERSONAL` con cualquier valor.
3. Hablar con tu bot (`/start`) para que te diga el `ID_PERSONAL`.
4. Actualizar variables de entorno con el valor de `ID_PERSONAL`.
5. Incluir al bot a tu grupo de telegram. El bot te indicará por interno el `ID_COURSE`
6. Actualizar variables de entorno con el valor de `ID_COURSE`.
6. Setear webhook de github con el servidor.