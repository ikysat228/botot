import asyncio
from aiogram import Bot, Dispatcher, types
from openai import AsyncOpenAI

# --- НАЛАШТУВАННЯ ---
TELEGRAM_TOKEN = "8255131327:AAF9VfeC8AE8q6dydjrFxjshr0nrSi7IyrA"
GITHUB_TOKEN = "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"

# Налаштування клієнта для роботи з GitHub Models
client = AsyncOpenAI(
    api_key=GITHUB_TOKEN,
    base_url="https://models.inference.ai.azure.com" # ВАЖЛИВО: адреса серверів GitHub
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message()
async def gpt_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, action="typing")
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Ти крутий асистент. Відповідай коротко і по суті.Ти опитний гравець в гру rust в тебе 9400 годин у цій грі, ти відповідаєш як задрот який з компютера взагалі не вилазить і ніколи не трогав траву ."},
                {"role": "user", "content": message.text}
            ],
            model="gpt-4o-mini",
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        await message.answer(answer, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"Помилка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())