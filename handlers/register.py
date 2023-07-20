import re
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter, CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, ParseMode, InputFile, ChatActions

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from loader import dp, bot
from buttons import Keyboards
from helpfull import congrats_message, contract_fee
from db.v1 import create_user, get_user


# Set up the Jinja environment
env = Environment(loader=FileSystemLoader("contract"))

# Load the HTML template
template = env.get_template("index.html")

now = datetime.now()
formatted_date = now.strftime("%m.%d")


class Register(StatesGroup):
    phone = State()
    edu_lang = State()
    edu_state = State()
    edu_major = State()
    full_name = State()


# phone number validation function
async def is_valid_phone(phone_number):
    match = re.search(r'^\+998|998[0-9]{9}$', phone_number)
    if match:
        return True
    else:
        return False

@dp.message_handler(CommandStart(), state="*")
async def send_welcome(message: types.Message):
    if len(get_user(message.chat.id)) == 0:
        create_user(message.chat.first_name, message.chat.last_name, message.chat.id)

    kb = await Keyboards.phone_kb()
    await Register.phone.set()
    await bot.send_message(message.chat.id, "Assalomu alaykum, RENAISSANCE UNIVERSITY ga xush kelibsiz! Iltimos, universitetga ro'yxatdan o'tish uchun telefon raqamingizni yuboring\nNamuna: +998333582024", reply_markup=kb)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='🏠BOSH SAHIFA', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    kb = await Keyboards.about()
    await bot.send_message(message.from_user.id,
                           "RENAISSANCE UNIVERSITY",
                           reply_markup=kb)
    await state.finish()


@dp.message_handler(Text(equals=("RO'YHATDAN O'TISH")))
async def start_state(message: types.message):
    kb = await Keyboards.phone_kb()
    await Register.phone.set()
    await bot.send_message(message.chat.id, "Ro'yxatdan o'tish uchun iltimos telefon raqamingizni kiriting!\nNamuna: +998333582024", reply_markup=kb)


@dp.message_handler(state=Register.phone,
                    content_types=[ContentType.CONTACT, ContentType.TEXT])
async def get_phone(message: types.Message, state: FSMContext):
    if message.content_type == 'text' and await is_valid_phone(message.text):
        await state.update_data(phone=message.text)
        await Register.next()
        kb = await Keyboards.uni_kb()
        await bot.send_message(message.chat.id, 'Iltimos, Universitetni tanlang', reply_markup=kb)
    elif message.content_type == 'contact':
        await state.update_data(phone=message.contact.phone_number)
        await Register.next()
        kb = await Keyboards.edu_lang_kb()
        await bot.send_message(message.chat.id, "Iltimos, ta'lim tilini tanlang", reply_markup=kb)
    else:
        await bot.send_message(message.chat.id, 'Iltimos to\'g\'ri raqam kiriting!\nNamuna: +998333582024')


@dp.message_handler(state=Register.edu_lang)
async def get_edu_lang(message: types.Message, state: FSMContext):
    if message.text == "🔙ORQAGA":
        await Register.phone.set()
        kb = await Keyboards.phone_kb()
        await bot.send_message(message.chat.id, "Ro'yhatdan o'tish uchun iltimos telefon raqamingizni kiriting!\nNamuna: +998333582024", reply_markup=kb)
    else:
        await state.update_data(edu_lang=message.text)
        await Register.next()
        kb = await Keyboards.edu_state_kb()
        await bot.send_message(message.chat.id, "Iltimos, ta'lim shaklini tanlang", reply_markup=kb)


@dp.message_handler(state=Register.edu_state)
async def get_edu_state(message: types.Message, state: FSMContext):
    if message.text == "🔙ORQAGA":
        await Register.edu_lang.set()
        kb = await Keyboards.edu_lang_kb()
        await bot.send_message(message.chat.id, "Iltimos, ta'lim tilini tanlang", reply_markup=kb)
    else:
        await state.update_data(edu_state=message.text)
        await Register.next()
        kb = await Keyboards.edu_majors_kb()
        async with state.proxy() as data:
            if data['edu_lang'] == "O'ZBEK" and data['edu_state'] in ['KUNDUZGI', 'KECHKI']:
                kb = await Keyboards.edu_majors_kb(uzb=True)
            elif data['edu_lang'] == "RUS" and data['edu_state'] in ['KUNDUZGI', 'KECHKI']:
                kb = await Keyboards.edu_majors_kb(rus=True)
            elif data['edu_lang'] == "O'ZBEK" and data['edu_state'] == "SIRTQI":
                kb = await Keyboards.edu_majors_kb(sirtqi_uzb=True)
            elif data['edu_lang'] == "RUS" and data['edu_state'] == "SIRTQI":
                kb = await Keyboards.edu_majors_kb(sirtqi_rus=True)
        await bot.send_message(message.chat.id, "Iltimos, ta'lim yo'nalishini tanglang", reply_markup=kb)

@dp.message_handler(state=Register.edu_major)
async def get_edu_major(message: types.Message, state: FSMContext):
    if message.text == "🔙ORQAGA":
        await Register.edu_state.set()
        kb = await Keyboards.edu_state_kb()
        await bot.send_message(message.chat.id, "Iltimos, ta'lim shaklini tanlang", reply_markup=kb)
    else:
        await state.update_data(edu_major=message.text)
        await Register.next()
        kb = await Keyboards.cancel()
        await bot.send_message(message.chat.id, "Iltimos, *familiya, ismi, sharif*ingizni passport bo'yicha yozib yuboring\n\nMasalan: *Abdullayev Abdulla Abdulla o'g'li*", parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


@dp.message_handler(state=Register.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    if message.text == '🔙ORQAGA':
        await Register.edu_major.set()
        kb = await Keyboards.edu_majors_kb()
        async with state.proxy() as data:
            if data['edu_lang'] == "O'ZBEK" and data['edu_state'] in ['KUNDUZGI', 'KECHKI']:
                kb = await Keyboards.edu_majors_kb(uzb=True)
            elif data['edu_lang'] == "RUS" and data['edu_state'] in ['KUNDUZGI', 'KECHKI']:
                kb = await Keyboards.edu_majors_kb(rus=True)
            elif data['edu_lang'] == "O'ZBEK" and data['edu_state'] == "SIRTQI":
                kb = await Keyboards.edu_majors_kb(sirtqi_uzb=True)
            elif data['edu_lang'] == "RUS" and data['edu_state'] == "SIRTQI":
                kb = await Keyboards.edu_majors_kb(sirtqi_rus=True)
        await bot.send_message(message.chat.id, "Iltimos, ta'lim yo'nalishini tanglang", reply_markup=kb)
    else:
        await state.update_data(full_name=message.text)
        async with state.proxy() as data:
            text = f"""F.I.SH: {data['full_name']}
Telefon raqam: {data['phone']}
Ta'lim yo'nalishi: {data['edu_major']}"""

        kb = await Keyboards.about()
        await bot.send_message(message.chat.id, "Shartnoma yuborilmoqda ....")
        await ChatActions.upload_document()

        with open(f'{os.path.abspath("contract_id.txt")}', 'r') as f:
            contract_id = f.read()
        with open(f'{os.path.abspath("contract_id.txt")}', 'w') as f:
            f.write(f'{int(contract_id)+1}')
        if data["edu_state"] == "KECHKI":
            edu_duration = '4,5 yil (2028-yil yakunlanadi)'
        elif data["edu_state"] == "KUNDUZGI":
            edu_duration = '4 yil (2027-yil yakunlanadi)'
        elif data["edu_state"] == "SIRTQI":
            edu_duration = '5 yil (2028-yil yakunlanadi)'
        else:
            edu_duration = '4,5 yil (2028-yil yakunlanadi)'

        formatted_contract_id = str(int(contract_id)+1).zfill(7)
        fee = contract_fee[data['edu_major']][data['edu_state']]

        rendered_html = template.render(
            contract_id=formatted_contract_id,
            now_date=formatted_date,
            full_name=data['full_name'],
            contract_fee=fee,
            edu_state=data['edu_state'],
            edu_duration=edu_duration,
            edu_major=data['edu_major']
        )
        base_url = os.path.abspath("contract")
        # Convert HTML to PDF using WeasyPrint
        pdf = HTML(string=rendered_html, base_url=base_url).write_pdf()

        # Save the PDF to a file
        pdf_file_path = f"kontrakt_{formatted_contract_id}.pdf"
        with open(pdf_file_path, "wb") as f:
            f.write(pdf)

        # Send the PDF file to the user
        with open(pdf_file_path, "rb") as f:
            await ChatActions.upload_document()
            await bot.send_document(message.chat.id, InputFile(f), caption=text)

        # Remove the temporary PDF file
        os.remove(pdf_file_path)
        await state.finish()
        await bot.send_message(message.chat.id, congrats_message, reply_markup=kb)
