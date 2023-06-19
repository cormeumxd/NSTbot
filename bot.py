import logging
from aiogram import Bot, Dispatcher, types

first_photo = False
second_photo = False

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='6237469218:AAEJ8-31b43Dy2XS5la-yRu9Rf1jZJdXlBY')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я могу перенести стиль одной фотографии на другую. Для этого отправь мне две фотографии")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_media_group(message: types.Message):
    global first_photo
    global second_photo
    if not first_photo and not second_photo:
        await message.answer('Первое фото получено! '
                            'Теперь пришлите второе фото '
                            '/cancel для отмены')
        first_photo = True
        #TODO Download photo
    elif first_photo and not second_photo:
        #TODO Download photo
        await message.answer('Второе фото получено! Думаю...')
        first_photo = False
        second_photo = False

@dp.message_handler(commands=['cancel'])
async def cancel_command(message: types.Message):
    global first_photo
    global second_photo
    if first_photo and not second_photo:
        await message.answer('Отправка отменена')
        first_photo = False
        #TODO Delete


@dp.message_handler()
async def unhandled_message(message: types.Message):
    await message.answer('Я пока не могу с этим справиться. Пришлите две фотографии и я перенесу стиль первой на вторую')