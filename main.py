import asyncio
import sqlite3 as sql

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.data_base import userExsists, addUser

db = sql.connect('database.db')
cur = db.cursor()

bot = Bot('7071326741:AAEmSUhX0ZBeVqFH7wJKpb0DN7cyJcU-E2M', parse_mode=ParseMode.HTML)
dp = Dispatcher()

router = Router()

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Играть 🧪',
        web_app=WebAppInfo(
            url=""
        )
    )
    return builder.as_markup()

@router.message(CommandStart())
async def start(message: Message) -> None:
    global user_id
    user_id = message.from_user.id
    user = await userExsists(user_id=user_id)
    if user == False:
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                await addUser(user_id=user_id, referrer_id=referrer_id)
                try:
                    await message.answer('<b>Вы зарегистрировались по реферальной ссылке. На ваш баланс начислено +3000 🧪</b>')

                    await bot.send_message(referrer_id, "<b>По вашей ссылке присоединился новый человек. На ваш баланс начислено +2000 🧪</b>")
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, "Нельзя регистрироваться по своей ссылке!")
        else:
            await addUser(user_id=user_id)
    await message.answer(f"<b>👋 Приветствую {message.from_user.username}.</b> Жми на кнопку ниже чтобы перейти в кликер 👇",
                         reply_markup=webapp_builder())
    
async def get_id() -> int:
    return user_id
    
async def main() -> None:
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())