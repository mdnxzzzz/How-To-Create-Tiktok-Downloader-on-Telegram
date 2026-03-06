import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Cargar token desde variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Envíame un enlace de TikTok para descargar el video.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        await update.message.reply_text("Por favor, envía un enlace válido de TikTok.")
        return

    msg = await update.message.reply_text("Descargando video... ⏳")
    
    # Configuración básica de yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Enviar el video descargado
        with open('video.mp4', 'rb') as video:
            await update.message.reply_video(video=video, caption="¡Aquí tienes tu video!")
        
        # Limpiar archivo local
        os.remove('video.mp4')
        await msg.delete()
        
    except Exception as e:
        await update.message.reply_text(f"Error al procesar el video: {str(e)}")

def main():
    if not TOKEN:
        print("Error: No se encontró TELEGRAM_TOKEN en el entorno.")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
