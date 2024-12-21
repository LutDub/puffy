import asyncio

from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

def webapp_builder():
    builder = InlineKeyboardBuilder()
    builder.button(
        text = "Let's Click", web_app = WebAppInfo(
            url = "..."
        )
    )
    return builder.as_markup()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        "Click! Click! Click!",
        reply_markup=webapp_builder()
    )

bot = Bot("6121749004:AAHP_g9EgrNZylWGH0BE6hymzehFW4dOA3c")

