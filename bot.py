import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для общения с ИИ
async def ask_ai(text: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    # Бесплатная модель
    data = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": text}]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Ошибка API: {response.status}"

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я умный бот с искусственным интеллектом. Задай мне любой вопрос!")

# Отправляем текст нейросети
@dp.message()
async def ai_handler(message: types.Message):
    await message.answer("Думаю... 🤔")
    ai_response = await ask_ai(message.text)
    await message.answer(ai_response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())