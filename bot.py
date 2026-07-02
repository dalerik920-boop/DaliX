from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq
from config import BOT_TOKEN, GROQ_API_KEY, CREATOR_NAME

# подключение Groq AI
client = Groq(api_key=GROQ_API_KEY)

# 🎵 музыка (YouTube поиск)
def music_link(query):
    return f"https://www.youtube.com/results?search_query={query}+music"

# 🖼 генерация картинок (бесплатно)
def image_link(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt}"

# 🌐 поиск
def web_search(query):
    return f"https://www.google.com/search?q={query}"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я Dalix AI PRO\n\n"
        "Я умею:\n"
        "🎵 музыка (просто напиши)\n"
        "🖼 создать картинку\n"
        "🌐 искать информацию\n"
        "🤖 отвечать как AI\n"
    )


# 💬 главный чат
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # 👑 создатель
    if "кто твой создатель" in text or "кто тебя создал" in text:
        await update.message.reply_text(
            f"👑 Мой создатель — {CREATOR_NAME}. Он 2012 года рождения и создал меня 2 июля 2026 года."
        )
        return

    # 🎵 музыка
    if "музыка" in text:
        query = text.replace("музыка", "").strip()
        await update.message.reply_text("🎵 Вот музыка:\n" + music_link(query))
        return

    # 🖼 картинка
    if "картинку" in text or "изображение" in text:
        prompt = text.replace("создай", "").replace("картинку", "").strip()
        await update.message.reply_text("🖼 Вот изображение:\n" + image_link(prompt))
        return

    # 🌐 поиск
    if "найди" in text or "поиск" in text:
        query = text.replace("найди", "").replace("поиск", "").strip()
        await update.message.reply_text("🌐 Вот результаты:\n" + web_search(query))
        return

    # 🤖 AI (Groq)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Ты Dalix AI. Сейчас 2026 год. Отвечай понятно и коротко."
            },
            {"role": "user", "content": text}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


# 📌 запуск бота
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🚀 Dalix AI запущен!")

app.run_polling()