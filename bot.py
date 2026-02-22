import asyncio
import os
import signal
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    await update.message.reply_text(f"Круто, {name}! Теперь я тебя знаю. Что дальше?")

async def main():
    print("Бот запущен. Жду команды /start...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    
    # Явная инициализация и запуск — это решает проблему на Render
    await app.initialize()
    await app.start()
    
    # Запускаем polling
    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        poll_interval=0.5  # чуть чаще, чтобы не висеть
    )
    
    # Держим процесс живым, пока Render не пришлёт SIGTERM
    stop_event = asyncio.Event()
    
    def handle_shutdown(signum, frame):
        print("Получен сигнал остановки...")
        stop_event.set()
    
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, handle_shutdown, signal.SIGTERM, None)
    
    await stop_event.wait()  # ждём сигнала
    
    # Чистая остановка
    await app.updater.stop()
    await app.stop()
    await app.shutdown()
    print("Бот остановлен корректно.")

if __name__ == "__main__":
    asyncio.run(main())
