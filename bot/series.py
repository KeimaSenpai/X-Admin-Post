from typing import Dict
from telegram import Update, ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

import bot.constants as con


def facts_to_str(user_data: Dict[str, str]):
    return (f'🍥 <b>{user_data["nombre"]}</b> 🍱\n\n'
            f'🎭 <b>Estado:</b> {user_data["estado"]}\n'
            f'📽️ <b>Resolución:</b> {user_data["resolucion"]}\n'
            f'🔎 <b>Capítulos:</b> {user_data["capitulos"]}\n'
            f'🎥 <b>Temporada:</b> {user_data["temporada"]}\n\n'
            f'📝 <b>Sinopsis:</b> <blockquote expandable>{user_data["sinopsis"]}</blockquote>\n\n'
            f'🔮 <b>Género:</b> {user_data["genero"]}\n'
            # f' <b>Subido por:</b> <a href="tg://user?id={user}">{name}</a>\n'
            '⚝━━━━━━━━━━━━━━━━━⚝\n'
            f'🍥 <a href="{con.MAIN_CHANNEL}"><b>X Anime</b></a> 🍱 '
            f'🍥 <a href="{con.SERIES_CHANNEL}"><b>Ver</b></a> 🍱')


def series(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        context.bot.send_message(chat_id=update.effective_user.id, text="Enviame la imagen de la plantilla.")
        return con.PHOTO
    else:
        context.bot.send_message(chat_id=update.effective_user.id, text='Debes enviar una imagen, intentalo otra vez.')
        return ConversationHandler.END


def photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('bot/photo/{}.jpg'.format(update.message.chat_id))
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame el nombre.')
    return con.NOMBRE


def nombre(update: Update, context: CallbackContext):
    context.user_data['nombre'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame el estado #Finalizado o #Emisión')
    return con.ESTADO


def estado(update: Update, context: CallbackContext):
    context.user_data['estado'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame la resolución')
    return con.RESOLUCION


def resolucion(update: Update, context: CallbackContext):
    context.user_data['resolucion'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame los capitulos.')
    return con.CAPITULOS


def capitulos(update: Update, context: CallbackContext):
    context.user_data['capitulos'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame la temporada.')
    return con.TEMPORADA


def temporada(update: Update, context: CallbackContext):
    context.user_data['temporada'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame la sinopsis.')
    return con.SINOPSIS


def sinopsis(update: Update, context: CallbackContext):
    context.user_data['sinopsis'] = update.message.text
    context.bot.send_message(chat_id=update.effective_user.id, text='Enviame el genero.')
    return con.GENERO


def genero(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    context.user_data['genero'] = update.message.text

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"✅ Plantilla creada correctamente\n<b>Resultado:</b>\n\n{facts_to_str(context.user_data)}".format(user=user_id, name=first_name) + "\n\nPulsa el botón de debajo para enviar la plantilla. 📢",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup([['Enviar plantilla de serie']], one_time_keyboard=True, resize_keyboard=True)
    )
    return con.SEND_TO_SERIES


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    context.bot.send_photo(
        chat_id=con.SERIES,
        photo=open(f'bot/photo/{update.message.chat_id}.jpg', 'rb'),
        caption=f'{facts_to_str(user_data)}'.format(user=user_id, name=first_name),
        parse_mode=ParseMode.HTML,
    )
    user_data.clear()
    return ConversationHandler.END
