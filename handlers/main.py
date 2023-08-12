import os

from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot


@dp.message_handler(Text(equals="BIZ HAQIMIZDA"))
async def about_uni(message: types.Message):
    about_photo = types.InputFile('./about/about.jpg', "Media")
    about_video = types.InputFile('./about/video.mp4', "Media")

    await types.ChatActions.upload_photo()
    await bot.send_photo(message.chat.id,
                         photo=about_photo)
    await types.ChatActions.upload_video()
    await bot.send_video(message.chat.id,
                         video=about_video,
                         caption="Renaissance university haqida batafsil")


@dp.message_handler(Text(equals="LOKATSIYA"))
async def location_uni(message: types.Message):
    latitude = 41.290556
    longtitude = 69.193572
    await bot.send_location(message.chat.id, latitude=latitude, longitude=longtitude)
    await bot.send_message(message.chat.id, text="""🏢 Universitet manzili Toshkent shahar, Uchtepa tumani Guzar, Lutfi ko‘chasi 18-uy.

📍 Qulaylik uchun Renaissanse University lokatsiyasi.""")


@dp.message_handler(Text(equals="BOG'LANISH"))
async def contact(message: types.message):
    text = """Biz bilan bog’lanish uchun:
+998333372023
+998333582024
+998332022324
+998333202324

t.me/ruuniver1
t.me/ruuniver_menejer
t.me/ruuniver2
t.me/runiver1"""
    await bot.send_message(message.chat.id, text)
