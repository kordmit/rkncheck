import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import csv
import requests
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

def block_resources():
    response = requests.get("https://reestr.rublacklist.net/api/v3/domains/")
    return response.json()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Присылай мне CSV файл для обработки.\nВ файле должны быть только домены БЕЗ РАЗДЕЛИТЕЛЕЙ!!!\nЕсли у тебя после конвертации из хlsx в файле есть знаки ;,. и т.д, то используй комбинацию клавиш ctrl+H, чтобы убрать их.\nСкрипт работает только с кодировкой UTF-8")


@dp.message(F.document)
async def handle_docs(message: types.Message):
    if message.document.mime_type == 'text/csv':
        document_id = message.document.file_id
        file_info = await bot.get_file(document_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        try:
            content = downloaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            await message.reply("Ошибка: Файл должен быть в кодировке UTF-8.")
            return
        csv_reader = csv.reader(StringIO(content))
        domains = [row[0] for row in csv_reader]

        blocked_resources = block_resources()
        matches = [domain for domain in domains if domain in blocked_resources]

        if matches:
            response_message = "Найдены совпадения:\n" + "\n".join(matches)
            await message.reply(response_message)
        else:
            await message.reply("Совпадений не найдено.")
    else:
        await message.reply("Пожалуйста, пришлите CSV файл.")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())