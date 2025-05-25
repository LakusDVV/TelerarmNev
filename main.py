import asyncio
import dotenv
import os
import requests

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")



dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

@dp.message(Command("cat"))
async def get_cat_image(message: Message) -> None:
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        response.raise_for_status()  # Проверяем, что ответ успешен
        data = response.json()
        cat_url = data[0]["url"]
        await message.answer_photo(photo=cat_url)
    except Exception as e:
        await message.answer("Не удалось получить кота :(")




# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
