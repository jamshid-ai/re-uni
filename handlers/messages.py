import os
import time
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot
from buttons import Keyboards
from db.v1 import get_all_users


class SendMessages(StatesGroup):
    message = State()


admins = os.getenv("ADMINS")

async def send_to_all(contacts, message):
    for index, contact in enumerate(contacts):
        if index % 25 == 0:
            time.sleep(1)
        try:
            await bot.send_message(contact[3], message)
        except:
            pass
    

@dp.message_handler(commands='send_message')
async def send_message(message: types.Message,
                       state: FSMContext):
    if str(message.chat.id) in admins.split(','):
        await message.answer('Xabar yuboring')
        await SendMessages.message.set()
    else:
        await message.answer('You dont have enough permission')


@dp.message_handler(state=SendMessages.message)
async def recieve_message(message: types.Message,
                          state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    await message.answer("Juda yaxshi) Quyidagi xabarni tasqidlang..")
    kb = await Keyboards.message_confirm()
    await message.answer(message.text, reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(text='ok')
async def confirmed_message(call_data: types.callback_query):
    await call_data.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(call_data.message.chat.id, 'Xabar yuborilmoqda..')
    contacts = get_all_users()
    await send_to_all(contacts, call_data.message.text)
    await bot.send_message(call_data.message.chat.id, "Xabar hammaga yuborildi!")


@dp.callback_query_handler(text='no')
async def cancel_message(call_data: types.callback_query):
    await call_data.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(call_data.message.chat.id,"Qaytadan xabar yuborish uchun /send_message")