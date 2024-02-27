import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from app.mappers.text_mapper import extract_text_from_response
from app.rest.message_handler import send_message
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

print(env_path)

token = os.getenv("TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!"
                         f"я могу кратко отвечать на твои вопросы"
                         f"задай интересующий тебя вопрос и я постараюсь ответить как можно более кратко")


@dp.message()
async def ai_message_handler(message: types.Message) -> None:
    try:
        await message.bot.send_chat_action(message.chat.id, "typing")
        if message.text:
            try:
                await message.answer(extract_text_from_response(send_message(message.text)))
            except TelegramBadRequest:
                await message.answer("Не хочу об этом говорить")

        else:
            await message.answer("Я могу отвечать только на текстовые сообщения!")
    except TypeError:
        await message.answer("Произошла ошибка при обработке сообщения.")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
