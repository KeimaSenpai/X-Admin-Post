# Post-Bot-Channel

Bot de Telegram para crear plantillas de forma rápida y enviarlas a un canal.

## Enviroment Vars

* **TELEGRAM_TOKEN**: Crea un bot en [@BotFather](https://t.me/BotFather) con /newbot y sigue las instrucciones. Es requerido añadir la variable en un archivo `.env`.

## Global

Estas variables son necesarias pero pueden ser modificadas a gusto del usuario.
Por defecto, debes añadir solo texto en las siguientes variables:

* **MAIN_CHANNEL**
* **ANIME_CHANNEL**
* **SERIES_CHANNEL**

En estas variables se almacena el `CHAT_ID` del canal o canales a donde serán enviados los posts.
Puedes encontrar el `CHAT_ID` reenviado un mensaje del canal hacia [@ShowJsonBot](https://t.me/ShowJsonBot).
Ambos son valores enteros [`int`] no lo trates como texto. Debes añadir el simbolo `-` en la variable.

**Formato:** `PELICULAS = -1234567890`

* **PELICULAS**
* **SERIES**

## ¿Deseas añadir canales adicionales a donde enviar plantillas?

Para esto es necesario crear nuevos 'steps' para el ConversationHandler, es decir, crear nuevas variables las cuales se interpretan como pasos, donde se guardará la información introducida por el usuario. Ambos módulos funcionan perfectamente por separado, añadir un módulo adicional es solo crear los 'steps' necesarios en `constants.py` e indicarle al ConversationHandler el orden en que recibirá la información.

## ¿Es necesaria la carpeta "photo"?

Si, esta carpeta es totalmente necesaria para guardar las imagenes introducidas al crear la plantilla. En caso de ser eliminada, el sistema volverá a generarla.

## ¿Puedo saltar algún paso en el momento de introducir la información?

Por el momento esa caracteristica no está implementada.
