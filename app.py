import logging

from aiogram import executor

from loader import dp
import middlewares, handlers

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dp)