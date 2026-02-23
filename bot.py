import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    await update.message.reply_text(f"Круто, {name}! Теперь я тебя знаю. Что дальше?")

# Фейковый сервер для Render (чтобы не думал, что процесс умер)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_dummy_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Запускаем фейковый сервер в фоне
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))

    print("Бот запущен. Polling...")

    # Создаём и запускаем свой цикл событий
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(app.initialize())
        loop.run_until_complete(app.start())
        loop.run_until_complete(app.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        ))
        # Держим цикл живым
        loop.run_forever()
    except KeyboardInterrupt:
        print("Остановка бота...")
    finally:
        # Чистим без ошибок
        loop.run_until_complete(app.updater.stop())
        loop.run_until_complete(app.stop())
        loop.run_until_complete(app.shutdown())
        loop.close()
