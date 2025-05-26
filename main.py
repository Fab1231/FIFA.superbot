import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "TOKEN_AQUI"  # será reemplazado por variable de entorno en Railway

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

resultados = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Bot activo! Usa /guardar y /prediccion.")

def guardar(update: Update, context: CallbackContext):
    texto = ' '.join(context.args)
    resultados.append(texto)
    update.message.reply_text(f"Guardado: {texto}")

def prediccion(update: Update, context: CallbackContext):
    if not resultados:
        update.message.reply_text("No hay datos.")
        return
    goles_totales = 0
    for r in resultados:
        try:
            goles = r.split()[1].split("-")
            goles_totales += int(goles[0]) + int(goles[1])
        except:
            continue
    prom = round(goles_totales / len(resultados), 2)
    msg = f"Promedio: {prom}. "
    msg += "Juega OVER 2.5" if prom > 2.5 else "Juega UNDER 2.5"
    update.message.reply_text(msg)

def main():
    from os import getenv
    updater = Updater(getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("guardar", guardar))
    dp.add_handler(CommandHandler("prediccion", prediccion))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
