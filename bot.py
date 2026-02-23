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

# Фейковый сервер, чтобы Render не думал, что процесс мёртв
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
    # Запускаем фейковый сервер в потоке
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))

    print("Бот запущен. Polling...")

    # Запускаем polling без asyncio.run() и без shutdown
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        # Важно: не трогаем цикл, Render сам им управляет
    )

    # Если дойдёт сюда (не дойдёт), но на всякий
    print("Polling завершён (но это не должно произойти)")
