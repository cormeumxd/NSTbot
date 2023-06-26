import logging
from aiogram import Bot, Dispatcher, types
from config import token

first_photo = False
second_photo = False

#Hyperparametres
epochs = 100
alpha = 10
betta = 1000
IMG_SIZE = 128

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['epochs'])
async def set_epochs(message: types.Message):
    try:
        if int(message.text.split()[1]) < 50 or int(message.text.split()[1]) > 300:
            raise ValueError
        epochs = int(message.text.split()[1])
        await message.answer(f'Количетво эпох: {epochs}')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 50 до 300!')

@dp.message_handler(commands=['imgsize'])
async def set_imgsize(message: types.Message):
    try:
        if int(message.text.split()[1]) < 64 or int(message.text.split()[1]) > 256:
            raise ValueError
        IMG_SIZE = int(message.text.split()[1])
        await message.answer(f'Качество картинки: {IMG_SIZE}x{IMG_SIZE} пикселей')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 64 до 256!')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я могу перенести стиль одной фотографии на другую. Для этого отправь мне две фотографии")


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