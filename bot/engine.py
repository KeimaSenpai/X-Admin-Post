import os
import logging

from telegram import Update, ParseMode, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, ConversationHandler

import bot.constants as con
import bot.peliculas as peli
import bot.series as serie

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if user_id in con.administradores:
        update.message.reply_text(text=(
            f'<a href="https://i.imgur.com/3UiHLoz.jpg">🎁</a><b> Hola <a href="tg://user?id={user_id}">{first_name}</a></b>\n'
            '<b>Este bot le permite crear una plantilla con gran facilidad para X Anime.</b>\n\n'
            '<b>Pulsa /inicio para empezar.</b>'
        ),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='🍀 Canal 🍀', url=con.MAIN_CHANNEL)]]), parse_mode=ParseMode.HTML
        )
        context.bot.set_my_commands([
            BotCommand(command='start', description='Bot On.'),
            BotCommand(command='inicio', description='Generar una plantilla.'),
            BotCommand(command='cancelar', description='Detener el proceso actual.')
        ]
        )
    else:
        update.message.reply_text(
            text=(
                f'<a href="https://i.imgur.com/bmEER3j.jpg">🍀</a> <b>Hola <a href="tg://user?id={user_id}">{first_name}</a></b>\n'
                '<b>No tienes acceso para usar este bot.</b>'
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='🍀 X Anime 🍀', url=con.ANIME_CHANNEL)],
                [InlineKeyboardButton(text='🍀 X Anime Series 🍀', url=con.SERIES_CHANNEL)]
            ]),
            parse_mode=ParseMode.HTML
        )


def inicio(update: Update, context: CallbackContext):
        update.message.reply_text(text='¿Que plantilla necesitas generar?',
        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Series', callback_data='series')],
                [InlineKeyboardButton(text='Peliculas', callback_data='peliculas')],
            ]
        )
    )

def stop(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        update.message.reply_text(text='Operación cancelada.', reply_markup=ReplyKeyboardRemove(selective=True))
        return ConversationHandler.END
    else:
        update.message.reply_to_message(text='No.')


def main():
    token = os.getenv('TELEGRAM_TOKEN', '6184630791:AAFW4JDa2Aw6s4ddVJ9S7Seck4OKkK2MaPI')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(serie.series, pattern='series'),
            CallbackQueryHandler(peli.peliculas, pattern='peliculas')
        ],
        states={
            con.PHOTO: [MessageHandler(Filters.photo, serie.photo),],
            con.NOMBRE: [MessageHandler(Filters.text, serie.nombre)],
            con.ESTADO: [MessageHandler(Filters.text, serie.estado)],
            con.RESOLUCION: [MessageHandler(Filters.text, serie.resolucion)],
            con.CAPITULOS: [MessageHandler(Filters.text, serie.capitulos)],
            con.TEMPORADA: [MessageHandler(Filters.text, serie.temporada)],
            con.SINOPSIS: [MessageHandler(Filters.text, serie.sinopsis),],
            con.GENERO: [MessageHandler(Filters.text, serie.genero),],

            con.PHOTO_PELI: [MessageHandler(Filters.photo, peli.photo),],
            con.NOMBRE_PELI: [MessageHandler(Filters.text, peli.nombre)],
            con.RESOLUCION_PELI: [MessageHandler(Filters.text, peli.resolucion)],
            con.SINOPSIS_PELI: [MessageHandler(Filters.text, peli.sinopsis),],
            con.GENERO_PELI: [MessageHandler(Filters.text, peli.genero),],
            con.SUBTITULOS: [MessageHandler(Filters.text, peli.subs)],
            con.YEAR: [MessageHandler(Filters.text, peli.year)],
            con.AUDIO: [MessageHandler(Filters.text, peli.audio)],

            con.SEND_TO_PELI: [MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Enviar plantilla de pelicula$')), peli.done)],
            con.SEND_TO_SERIES: [MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Enviar plantilla de serie$')), serie.done)],
        },
        fallbacks=[
            MessageHandler(Filters.regex('^Enviar plantilla de serie$'), serie.done),
            MessageHandler(Filters.regex('^Enviar plantilla de pelicula$'), peli.done),
            CommandHandler('cancelar', stop),
        ],
        allow_reentry=True
    )
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('inicio', inicio))
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
