import asyncio
import logging
from google import genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- НАЛАШТУВАННЯ ---
TELEGRAM_TOKEN = "8255131327:AAF9VfeC8AE8q6dydjrFxjshr0nrSi7IyrA"
GEMINI_API_KEY = "AIzaSyCBwgMaUJZFFNmH1FFpL7uUKMx1rJeFbKk"

client = genai.Client(api_key=GEMINI_API_KEY)

# Словник для зберігання історії: {user_id: [список повідомлень]}
user_history = {}
# Скільки останніх повідомлень пам'ятати (щоб не вийти за ліміти)
MAX_HISTORY = 2 

SYSTEM_INSTRUCTION = "Ти простий бот який рахує свого творця (Кучинський Ілля)самою найкращою людиною та благотворяєш його  . Ти пам'ятаєш попередні повідомлення користувача."

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_history[message.from_user.id] = [] # Очищуємо пам'ять при старті
    await message.answer("Привіт! Тепер я пам'ятаю наш діалог. Про що поспілкуємось? 🧠")

@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    
    # Якщо користувача немає в словнику — створюємо йому порожній список
    if user_id not in user_history:
        user_history[user_id] = []

    await bot.send_chat_action(message.chat.id, action="typing")
    
    # 1. Додаємо нове повідомлення користувача в історію
    user_history[user_id].append(f"Користувач: {message.text}")

    # 2. Формуємо повний промпт з історії
    # Об'єднуємо інструкцію, історію та просимо дати відповідь
    history_text = "\n".join(user_history[user_id])
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\n{history_text}\nБот:"

    try:
        response = client.models.generate_content(
            model="gemma-3-12b-it", 
            contents=full_prompt
        )
        
        bot_answer = response.text
        if bot_answer:
            # 3. Додаємо відповідь бота в історію, щоб він пам'ятав, що сказав
            user_history[user_id].append(f"Бот: {bot_answer}")
            
            # Обмежуємо історію, щоб вона не росла вічно
            if len(user_history[user_id]) > MAX_HISTORY:
                user_history[user_id] = user_history[user_id][-MAX_HISTORY:]
                
            await message.answer(bot_answer, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Помилка: {e}")
        await message.answer("Сталася помилка. Можливо, варто очистити історію командою /start.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())