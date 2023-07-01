import logging
import io
from aiogram import Bot, Dispatcher, types
from config import token
from nst import NeuralStyleTransform
from transform import image_load_transform, tensor_to_image

first_photo = False
second_photo = False



#Hyperparametres
user_hyperparametres = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

#model
model = NeuralStyleTransform()

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['epochs'])
async def set_epochs(message: types.Message):
    global user_hyperparametres
    try:
        if int(message.text.split()[1]) < 50 or int(message.text.split()[1]) > 300:
            raise ValueError
        user_hyperparametres[message.from_user.id]['epochs'] = int(message.text.split()[1])
        await message.answer(f'Количетво эпох: {user_hyperparametres[message.from_user.id]["epochs"]}')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 50 до 300!')


@dp.message_handler(commands=['alpha'])
async def set_alpha(message: types.Message):
    global user_hyperparametres
    try:
        if int(message.text.split()[1]) < 1 or int(message.text.split()[1]) > 100000:
            raise ValueError
        user_hyperparametres[message.from_user.id]['alpha'] = int(message.text.split()[1])
        await message.answer(f'Параметр alpha: { user_hyperparametres[message.from_user.id]["alpha"]}')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 1 до 100000!')


@dp.message_handler(commands=['betta'])
async def set_betta(message: types.Message):
    global user_hyperparametres
    try:
        if int(message.text.split()[1]) < 1 or int(message.text.split()[1]) > 100000:
            raise ValueError
        user_hyperparametres[message.from_user.id]['betta'] = int(message.text.split()[1])
        await message.answer(f'Параметр betta: {user_hyperparametres[message.from_user.id]["betta"]}')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 1 до 100000!')


@dp.message_handler(commands=['imgsize'])
async def set_imgsize(message: types.Message):
    global user_hyperparametres
    try:
        if int(message.text.split()[1]) < 64 or int(message.text.split()[1]) > 256:
            raise ValueError
        user_hyperparametres[message.from_user.id]['imgsize'] = int(message.text.split()[1])
        await message.answer(f'Качество картинки: {user_hyperparametres[message.from_user.id]["imgsize"]}x{user_hyperparametres[message.from_user.id]["imgsize"]} пикселей')
    except (ValueError, IndexError):
        await message.answer(f'Пожалуйста, введите целое число от 64 до 256!')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    global user_hyperparametres
    user_id = message.from_id.id
    if user_id not in user_hyperparametres:
        user_hyperparameters[user_id] = {
            'epochs': 100,
            'alpha': 10,
            'betta': 1000,
            'imgsize': 128
        }
    await message.answer('Привет! Я могу перенести стиль одной фотографии на другую. Для этого отправь мне две фотографии\n'
                        '/epochs n - установить количество эпох, равное n\n'
                        '/imgsize n - установить размер получаемого изображения на nXn\n'
                        '/alpha n - установить параметр alpha, равный n\n'
                        '/betta n - установить параметр betta, равный n\n')

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_media_group(message: types.Message):
    global first_photo
    global second_photo
    global style_file
    global content_file
    global user_hyperparametres
    user_id = message.from_user.id
    if not first_photo and not second_photo:
        await message.answer('Первое фото получено! '
                            'Теперь пришлите второе фото '
                            '/cancel для отмены')
        first_photo = True
        style_id = message.photo[-1].file_id
        style_file = await bot.download_file_by_id(style_id)
    elif first_photo and not second_photo:
        content_id = message.photo[-1].file_id
        content_file = await bot.download_file_by_id(content_id)
        await message.answer('Второе фото получено! Думаю...')
        first_photo = False
        second_photo = False

        style_image = image_load_transform(io.BytesIO(style_file.getvalue()), user_hyperparametres[user_id]['imgsize'])
        content_image = image_load_transform(io.BytesIO(content_file.getvalue()), user_hyperparametres[user_id]['imgsize'])

        model.load_images(style_image, content_image)
        final_image = model.transform(user_hyperparametres[user_id]['epochs'], user_hyperparametres[user_id]['alpha'], user_hyperparametres[user_id]['betta'], learning_rate=3e-2)

        img = tensor_to_image(final_image.squeeze())

        await bot.send_photo(chat_id=message.chat.id, photo=img)
        


@dp.message_handler(commands=['cancel'])
async def cancel_command(message: types.Message):
    global first_photo
    global second_photo
    if first_photo and not second_photo:
        await message.answer('Отправка отменена')
        first_photo = False
    else:
        await message.answer('Нечего отменять')


@dp.message_handler()
async def unhandled_message(message: types.Message):
    await message.answer('Я пока не могу с этим справиться. Пришлите две фотографии и я перенесу стиль первой на вторую')