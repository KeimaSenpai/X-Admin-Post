from typing import Dict
from telegram import Update, ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

import bot.constants as con


def facts_to_str(user_data: Dict[str, str]):
    return (f'🍥 <b>{user_data["nombre"]}</b> 🍱\n\n'
            f'🎭 <b>Año:</b> {user_data["year"]}\n'
            f'📽️ <b>Resolución:</b> {user_data["resolucion"]}\n'
            f'🔎 <b>Subtitulos:</b> {user_data["subs"]}\n'
            f'🎥 <b>Audio:</b> {user_data["audio"]}\n\n'
            f'📝 <b>Sinopsis:</b> {user_data["sinopsis"]}\n\n\n'
            f'🔮 <b>Género:</b> {user_data["genero"]}\n'
            # f' <b>Subido por:</b> <a href="tg://user?id={user}">{name}</a>\n'
            '⚝━━━━━━━━━━━━━━━━━━━⚝\n'
            f'🍥 <a href="{con.MAIN_CHANNEL}"><b>X Anime</b></a> 🍱 '
            f'🍥 <a href="{con.PELICULAS_CHANNEL}"><b>Ver</b></a> 🍱')


def peliculas(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        context.bot.send_message(chat_id=update.effective_user.id, 
                                 text='<b>Enviame la imagen de la película.</b>',
                                 parse_mode=ParseMode.HTML
                                 )
        return con.PHOTO_PELI
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text='Debes enviar una imagen.')
        return ConversationHandler.END


def photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('bot/photo/{}.jpg'.format(update.message.chat_id))
    context.bot.send_message(chat_id=update.effective_user.id, 
                             text='<b>Enviame el nombre.</b>',
                             parse_mode=ParseMode.HTML
                             )
    return con.NOMBRE_PELI


def nombre(update: Update, context: CallbackContext):
    context.user_data['nombre'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, 
                             text='<b>📽️ Enviame la resolucion.</b>\n<b>Calidades:</b> <code>CAM</code> <code>720p</code> <code>1080p</code>',
                             parse_mode=ParseMode.HTML
                             )
    return con.RESOLUCION_PELI


def resolucion(update: Update, context: CallbackContext):
    context.user_data['resolucion'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, 
                             text='<b>🎭 Enviame el año.</b>',
                             parse_mode=ParseMode.HTML
                             )
    return con.YEAR


def year(update: Update, context: CallbackContext):
    context.user_data['year'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, 
                             text='<b>Enviame el audio.</b>',
                             parse_mode=ParseMode.HTML
                             )
    return con.AUDIO


def audio(update: Update, context: CallbackContext):
    context.user_data['audio'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame los subtitulos.')
    return con.SUBTITULOS


def subs(update: Update, context: CallbackContext):
    context.user_data['subs'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame la sinopsis')
    return con.SINOPSIS_PELI


def sinopsis(update: Update, context: CallbackContext):
    context.user_data['sinopsis'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame el genero.')
    return con.GENERO_PELI


def genero(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    context.user_data['genero'] = update.message.text

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"✅ Plantilla creada correctamente\n<b>Resultado:</b>\n\n{facts_to_str(context.user_data)}".format(user=user_id, name=first_name) + "\n\nPulsa el botón de debajo para enviar la plantilla. 📢",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup([['Enviar plantilla de pelicula']], one_time_keyboard=True, resize_keyboard=True)
    )
    return con.SEND_TO_PELI


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    context.bot.send_photo(
        chat_id=con.PELICULAS,
        photo=open(f'bot/photo/{update.message.chat_id}.jpg', 'rb'),
        caption=f'{facts_to_str(user_data)}'.format(user=user_id, name=first_name),
        parse_mode=ParseMode.HTML,
    )
    user_data.clear()
    return ConversationHandler.END
