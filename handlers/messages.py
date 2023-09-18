import os
import time
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from loader import dp, bot
from buttons import Keyboards
from db.v1 import get_all_users


class SendMessages(StatesGroup):
    message = State()


admins = os.getenv("ADMINS")

async def send_to_all(contacts, message=None,**kwargs):
    file_id = kwargs.get('file_id')
    photo = kwargs.get('photo')
    video = kwargs.get('video')
    location = kwargs.get('location')
    longitude = kwargs.get('longitude')
    latitude = kwargs.get('latitude')
    for index, contact in enumerate(contacts):
        if index % 25 == 0:
            time.sleep(1)
        if photo:
            try:
                await bot.send_photo(contact[3], photo=file_id, caption=message)
            except:
                pass
        elif video:
            try:
                await bot.send_video(contact[3], video=file_id, caption=message)
            except:
                pass
        elif location:
            try:
                await bot.send_location(chat_id=contact[3],
                                        longitude=longitude,
                                        latitude=latitude)
            except:
                pass
        elif not photo and not video:
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


@dp.message_handler(state=SendMessages.message,
                    content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.TEXT, ContentType.LOCATION])
async def recieve_message(message: types.Message,
                          state: FSMContext):
    kb = await Keyboards.message_confirm()
    if message.content_type == 'text':
        await message.answer("Juda yaxshi) Quyidagi xabarni tasqidlang..")
        await message.answer(message.text, reply_markup=kb)
        await state.finish()
    elif message.content_type == 'photo':
        await message.answer("Juda yaxshi) Quyidagi xabarni tasqidlang..")
        await bot.send_photo(message.chat.id,
                             photo=message.photo[0].file_id,
                             caption=message.caption,
                             reply_markup=kb)
        await state.finish()
    elif message.content_type == 'video':
        await message.answer("Juda yaxshi) Quyidagi xabarni tasqidlang..")
        await bot.send_video(message.chat.id,
                             video=message.video.file_id,
                             caption=message.caption,
                             reply_markup=kb)
        await state.finish()
    elif message.content_type == 'location':
        await message.answer("Juda yaxshi) Quyidagi xabarni tasqidlang..")
        await bot.send_location(message.chat.id,
                                latitude=message.location.latitude,
                                longitude=message.location.longitude,
                                reply_markup=kb)
        await state.finish()


@dp.callback_query_handler(text='ok')
async def confirmed_message(call_data: types.callback_query):
    await call_data.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(call_data.message.chat.id, 'Xabar yuborilmoqda..')
    contacts = get_all_users()
    if call_data.message.photo:
        file_id = call_data.message.photo[0].file_id
        await send_to_all(contacts, call_data.message.caption, photo=True, file_id=file_id)
    elif call_data.message.video:
        file_id = call_data.message.video.file_id
        await send_to_all(contacts, call_data.message.caption, video=True, file_id=file_id)
    elif call_data.message.location:
        longitude = call_data.message.location.longitude
        latitude = call_data.message.location.latitude
        await send_to_all(contacts, location=True, longitude=longitude, latitude=latitude)
    else:
        await send_to_all(contacts, call_data.message.text)
    await bot.send_message(call_data.message.chat.id, "Xabar hammaga yuborildi!")


@dp.callback_query_handler(text='no')
async def cancel_message(call_data: types.callback_query):
    await call_data.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(call_data.message.chat.id,"Qaytadan xabar yuborish uchun /send_message")