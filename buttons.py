from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton,
    ReplyKeyboardMarkup, InputFile, ReplyKeyboardRemove
)

class Keyboards:

    @staticmethod
    async def welcome_kb():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("RO'YHATDAN O'TISH"))
        kb.add(
            KeyboardButton('LOKATSIYA'),
            KeyboardButton('BIZ HAQIMIZDA')
        )
        return kb

    @staticmethod
    async def uni_kb():
        btns = [
            KeyboardButton("RENAISSANCE UNIVERSITY")
        ]
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.add(*btns)
        return kb
        
    @staticmethod
    async def phone_kb():
        btns = [
            KeyboardButton("Telefon raqamni yuborish", request_contact=True)
        ]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*btns)
        return kb

    @staticmethod
    async def edu_lang_kb():
        btns = [
            KeyboardButton("O'ZBEK"),
            KeyboardButton("RUS")
        ]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*btns)
        kb.add(
            KeyboardButton('🔙ORQAGA'),
            KeyboardButton("🏠BOSH SAHIFA")
        )
        return kb

    @staticmethod
    async def edu_state_kb():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        btns = [
            KeyboardButton("KUNDUZGI"),
            KeyboardButton('KECHKI'),
            KeyboardButton('SIRTQI')
        ]
        kb.add(*btns)
        kb.add(
            KeyboardButton('🔙ORQAGA'),
            KeyboardButton("🏠BOSH SAHIFA")
        )
        return kb

    @staticmethod
    async def edu_majors_kb(**kwargs):
        if kwargs.get('uzb'):
            btns = [
                KeyboardButton("Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Logistika (yo‘nalishlar bo‘yicha)"),
                KeyboardButton("Menejment (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Iqtisodiyot (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (ingliz tili)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (o‘zbek tili)"),
                KeyboardButton("Tarix"),
                KeyboardButton("Boshlang‘ich ta’lim"),
            ]
            kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            kb.add(*btns)
            kb.add(KeyboardButton('ORQAGA'))
            return kb
        elif kwargs.get('sirtqi_uzb'):
            btns = [
                KeyboardButton("Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Logistika (yo‘nalishlar bo‘yicha)"),
                KeyboardButton("Menejment (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Iqtisodiyot (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (o‘zbek tili)"),
                KeyboardButton("Tarix"),
                KeyboardButton("Boshlang‘ich ta’lim")
            ]
            kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            kb.add(*btns)
            kb.add(
                KeyboardButton('🔙ORQAGA'),
                KeyboardButton("🏠BOSH SAHIFA"))
            return kb
        elif kwargs.get('rus'):
            btns = [
                KeyboardButton("Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Logistika (yo‘nalishlar bo‘yicha)"),
                KeyboardButton("Menejment (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Iqtisodiyot (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (rus tili)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (ingliz tili)"),
                KeyboardButton("Tarix"),
                KeyboardButton("Boshlang‘ich ta’lim")
            ]
            kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            kb.add(*btns)
            kb.add(
                KeyboardButton('🔙ORQAGA'),
                KeyboardButton("🏠BOSH SAHIFA"))
            return kb
        elif kwargs.get('sirtqi_rus'):
            btns = [
                KeyboardButton("Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Logistika (yo‘nalishlar bo‘yicha)"),
                KeyboardButton("Menejment (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Iqtisodiyot (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Tarix"),
                KeyboardButton("Boshlang‘ich ta’lim")
            ]
            kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            kb.add(*btns)
            kb.add(
                KeyboardButton('🔙ORQAGA'),
                KeyboardButton("🏠BOSH SAHIFA"))
            return kb
        else:
            btns = [
                KeyboardButton("Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Logistika (yo‘nalishlar bo‘yicha)"),
                KeyboardButton("Menejment (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Iqtisodiyot (tarmoqlar va sohalar bo‘yicha)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (ingliz tili)"),
                KeyboardButton("Filologiya va tillarni o‘qitish (rus tili)"),    
                KeyboardButton("Filologiya va tillarni o‘qitish (o‘zbek tili)"),
                KeyboardButton("Tarix"),
                KeyboardButton("Boshlang‘ich ta’lim")
            ]
            kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            kb.add(*btns)
            kb.add(
                KeyboardButton('🔙ORQAGA'),
                KeyboardButton("🏠BOSH SAHIFA"))
            return kb
    
    @staticmethod
    async def cancel():
        btns = [
            KeyboardButton("🔙ORQAGA"),
            KeyboardButton("🏠BOSH SAHIFA")
        ]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*btns)
        return kb

    @staticmethod
    async def remove():
        kb = ReplyKeyboardRemove()
        return kb

    @staticmethod
    async def about():
        btns = [
            KeyboardButton("BIZ HAQIMIZDA"),
            KeyboardButton("LOKATSIYA")
        ]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*btns)
        kb.add(KeyboardButton("BOG'LANISH"))
        return kb
