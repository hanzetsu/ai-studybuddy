import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

from agents.ocr_agent import extract_text_from_image
from agents.gigachat_agent import answer_question, explain_simple
from utils.ticket_manager import add_ticket, get_tickets, delete_ticket

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === Telegram bot ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я StudyBuddy — твой помощник к сессии.\n\n"
        "Отправь текст или фото с вопросом, и я помогу тебе подготовиться.\n"
        "Доступные команды:\n"
        "/tickets — список билетов\n"
        "/train — режим тренировки\n"
        "/delete <номер> — удалить билет\n"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if update.message.photo:
        photo = await update.message.photo[-1].get_file()
        image_path = f"temp_{user_id}.jpg"
        await photo.download_to_drive(image_path)
        question = extract_text_from_image(image_path)
        try:
            os.remove(image_path)
        except Exception:
            pass
    else:
        question = update.message.text

    await update.message.reply_text("🤔 Думаю над ответом...")
    answer = answer_question(question)
    add_ticket(user_id, question, answer)

    keyboard = [[InlineKeyboardButton("📘 Объяснить проще", callback_data=f"explain_{len(get_tickets(user_id)) - 1}")]]
    await update.message.reply_text(f"✅ Ответ сохранён как билет №{len(get_tickets(user_id))}\n\n{answer}", reply_markup=InlineKeyboardMarkup(keyboard))

async def list_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    tickets = get_tickets(user_id)
    if not tickets:
        await update.message.reply_text("📭 У тебя пока нет билетов.")
        return

    text = "📚 Список твоих билетов:\n"
    for i, t in enumerate(tickets):
        text += f"{i+1}. {t['question'][:50]}...\n"

    await update.message.reply_text(text)

async def delete_ticket_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        await update.message.reply_text("Укажи номер билета: /delete <номер>")
        return

    try:
        index = int(context.args[0]) - 1
    except ValueError:
        await update.message.reply_text("Неверный номер билета.")
        return

    if delete_ticket(user_id, index):
        await update.message.reply_text("🗑️ Билет удалён.")
    else:
        await update.message.reply_text("❌ Ошибка: билет не найден.")

async def explain_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    index = int(query.data.split('_')[1])
    ticket = get_tickets(user_id)[index]
    explanation = explain_simple(ticket['answer'])

    await query.message.reply_text(f"📘 Объяснение простыми словами:\n{explanation}")

async def train_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    tickets = get_tickets(user_id)

    if not tickets:
        await update.message.reply_text("Нет сохранённых билетов для тренировки.")
        return

    context.user_data['train_index'] = 0
    await send_train_question(update, context)

async def send_train_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    index = context.user_data.get('train_index', 0)
    tickets = get_tickets(user_id)

    if index >= len(tickets):
        await update.message.reply_text("🎓 Тренировка завершена!")
        return

    question = tickets[index]['question']
    await update.message.reply_text(f"🧩 Вопрос {index+1}: {question}")
    context.user_data['train_index'] += 1

# === Запуск ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tickets", list_tickets))
    app.add_handler(CommandHandler("delete", delete_ticket_cmd))
    app.add_handler(CommandHandler("train", train_mode))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    app.add_handler(CallbackQueryHandler(explain_callback, pattern=r"^explain_\d+"))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
