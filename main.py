import logging
import random
import requests
import asyncio
import datetime
import markups as nav
import listings as list
import config as cfg
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)
def is_member(user_id):
    query = f'{cfg.TELEGRAM_API_URL}/getChatMember?chat_id={cfg.CHAT_ID_KH}&user_id={user_id}'
    response = requests.get(query)
    if response.status_code == 200:
        json_response = response.json()
        return json_response['ok'] and (json_response['result']['status'] in ['creator', 'administrator', 'member'])
    return False

# Таймер
async def send_reminder(chat_id: int):
    """Эта функция отправляет уведомление за 30 секунд до истечения таймера"""
    await asyncio.sleep(60 * 1) # ожидаем 5 минут (300 секунд) перед началом проверки
    while True:
        time_left = end_time - datetime.datetime.now()
        if time_left.seconds <= 30:
            await bot.send_message(chat_id, '⏳ Осталось 30 секунд!')
        await asyncio.sleep(31)

@dp.message_handler(commands=['timer'])
async def set_timer(message: types.Message):
    global end_time
    try:
        minutes = int(message.text.split()[1])
        end_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        # отправляем сообщение о таймере
        await message.reply(f'🙎🏻 Таймер установлен на {minutes} минут(ы)!')

        # запускаем асинхронную функцию для отправки уведомления
        loop = asyncio.get_running_loop()
        task = loop.create_task(send_reminder(message.chat.id))

        # ожидаем окончания времени таймера
        while end_time > datetime.datetime.now():
            await asyncio.sleep(1)

        # останавливаем задачу с отправкой уведомления
        if not task.done():
            task.cancel()

        # отправляем сообщение о том, что таймер закончился
        await message.reply('⌛ Время вышло!')

    except (IndexError, ValueError):
        await message.reply('🕐 Пожалуйста, установите таймер по образцу: /timer 5')

@dp.message_handler(commands=['reset'])
async def reset_timer(message: types.Message):
    global end_time
    end_time = datetime.datetime.now()
    await message.reply('Таймер сброшен!')

# Код главного меню
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, '🙎🏻 Привет, {0.first_name}!\nИспользование меню даёт возможность доступа к моим функциям.\nЕсли ты новичок в АА, то нажми кнопку "😃 Я участник". Этот раздел содержит полезную информацию и ссылки"'.format(message.from_user), reply_markup = nav.mainMenu)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '😺 Я служащий': # MAIN MENU
        if is_member(message.from_user.id):
            user_name = message.from_user.first_name
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, f'🙎🏻 Спасибо за служение, {user_name}! Для прохождения обучения нажми соответствующую кнопку меню', reply_markup=nav.menuModer, parse_mode=types.ParseMode.HTML)
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '✈ АА Китти Хок': # MODER MENU
        if is_member(message.from_user.id):
            user_name = message.from_user.first_name
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '<b>ВНИМАНИЕ! Сообщения напрямую отправляются в основной чат группы "Китти Хок"! Будьте внимательны при выборе!</b>', reply_markup=nav.menuKittyHawk, parse_mode=types.ParseMode.HTML)
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '🏋️‍♀️ Обучающий режим': # MODER MENU
        if is_member(message.from_user.id):
            user_name = message.from_user.first_name
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '🙎🏻 Включен <b>обучающий режим</b>. Для того, чтобы продолжить, необходимо состоять в группе <b><a href = "https://t.me/+l0tnmnBnph8yMThi">«Обучение новичков Китти Хок»</a></b>\n\n'
                                                         'Снизу расположены кнопки меню, которые позволяют отправить в чат необходимые сообщения. При нажатии бот отправит в основной чат '
                                                         'информацию, необходимую для проведения собрания. В обучающем режиме сообщения отправятся в тестовую группу.', reply_markup = nav.menuTrain, parse_mode = types.ParseMode.HTML)
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup = nav.mainMenu)

        # MODER MENU
    elif message.text == '📆 Случайная доп.тема': # MODER MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID,'<b>Доп.тема:</b> ' + str(random.choice(list.THEMES)), parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, '🙎🏻 Случайная тема отправлена в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '7️⃣ 7 традиция': # MODER MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID, '<b>7 ТРАДИЦИЯ</b>\n❗️Пометка «7 традиция» при переводе\n\n🌍<b>РФ</b>\nСБЕР <b>4276 2800 1685 5840</b>\nили по номеру телефона\n<b>+79121281712</b>\n\n🌏<b>ДРУГИЕ СТРАНЫ</b>\nКнопка PAYPAL', reply_markup=nav.payMenu, parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, '🙎🏻 Реквизиты 7 традиции отправлены в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '🦶 12 шагов': # MODER MENU
        if is_member(message.from_user.id):
            photo = types.InputFile('amy_w_bot/steps.jpg')
            await bot.send_photo(cfg.CHAT_ID, photo=photo)
            await bot.send_message(message.from_user.id, '🙎🏻 Список 12-и шагов отправлен в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '9️⃣ Обещание 9 шага': # MODER MENU
        if is_member(message.from_user.id):
            photo = types.InputFile('amy_w_bot/ninestep.jpg')
            await bot.send_photo(cfg.CHAT_ID, photo=photo)
            await bot.send_message(message.from_user.id, '🙎🏻 Обещание 9 шага отправлено в чат группы Китти Хок!')

        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '📣 Блок объявлений': # MODER MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID, list.ADVERT, parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, '🙎🏻 Блок объявлений отправлен в чат группы Китти Хок!')

        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '☕️ Правила чайной': # MODER MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID, list.TEA_ROOM , parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, '🙎🏻 Правила чайной отправлены в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup = nav.mainMenu)

    elif message.text == '🕰 Расписание':  # MODER MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID, list.TABLE, parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, '🙎🏻 Расписание отправлено в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id,
                                   '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!',
                                   reply_markup=nav.mainMenu)

        # TRAIN MENU
    elif message.text == 'Случайная тема': # TRAIN MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID_TRAIN, '<b>Доп.тема:</b> ' + str(random.choice(list.THEMES)), parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, 'Случайная тема отправлена в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == '12 шагов': # TRAIN MENU
        if is_member(message.from_user.id):
            photo = types.InputFile('amy_w_bot/steps.jpg')
            await bot.send_photo(cfg.CHAT_ID_TRAIN, photo=photo)
            await bot.send_message(message.from_user.id, 'Список 12-и шагов отправлен в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup=nav.mainMenu)

    elif message.text == 'Правила': # TRAIN MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            await bot.send_message(cfg.CHAT_ID_TRAIN, list.TEA_ROOM , parse_mode=types.ParseMode.HTML)
            await bot.send_message(message.from_user.id, 'Правила чайной отправлены в чат группы Китти Хок!')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id, '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!', reply_markup = nav.mainMenu)

    elif message.text == '🦄 Пони':  # TRAIN MENU
        if is_member(message.from_user.id):
            await asyncio.sleep(0.2)
            animation = types.InputFile('amy_w_bot/pony.gif')
            await bot.send_animation(cfg.CHAT_ID_TRAIN, animation=animation)
            await bot.send_message(message.from_user.id, 'Пони побежал в чат')
        else:
            await asyncio.sleep(0.2)
            await bot.send_message(message.from_user.id,
                                   '❗️ Извини, но этот раздел только для служащих группы АА "Китти Хок". Чтобы стать служащим группы, обратись к администраторам!',
                                   reply_markup=nav.mainMenu)

        # USER MENU
    elif message.text == '👣 Вернуться в начало': # USER MENU
        await asyncio.sleep(0.2)
        await bot.send_message(message.from_user.id, '🙎🏻 Пожалуйста, выбери необходимый пункт меню', reply_markup=nav.mainMenu)

    elif message.text == '😃 Я новичок/участник': # MAIN MENU
        await asyncio.sleep(0.2)
        await bot.send_message(message.from_user.id, '🙎🏻 В этом разделе содержится полезная информация и ссылки сообщества Анонимные Алкоголики', reply_markup=nav.menuUser)

    elif message.text == '👩‍❤️‍👨 Ищу группы АА онлайн': # USER MENU
        await asyncio.sleep(0.2)
        await bot.send_message(message.from_user.id, text=str(list.GROUPS), reply_markup=nav.menuUser, parse_mode=types.ParseMode.HTML)

    elif message.text == '🥸 Ищу спонсора или доверенного': # USER MENU
        await asyncio.sleep(0.2)
        await bot.send_message(message.from_user.id, '🙎🏻 При переходе по ссылке ты получишь всю необходимую актуальную информацию о людях, готовых поделиться опытом прохождения 12 шагов Анонимных Алкоголиков и собственном опыте выздоровления от алкоголизма.\n\n'
                                                          '<a href = "https://docs.google.com/spreadsheets/d/119MZmYJje7kURVoHKTVDbauUEeomFImS8q33vFDge8U/edit#gid=0"> Телефоны спонсоров и доверенных группы АА "Китти Хок" </a>', reply_markup=nav.menuUser, parse_mode=types.ParseMode.HTML)

    elif message.text == '⏱ Таймер': # MAIN MENU
        await asyncio.sleep(0.2)
        await bot.send_message(message.from_user.id, '🙎🏻 Функция таймера позволяет засекать время высказывания на собраниях групп. Таймер может быть установлен на любое время в минутах при помощи команды "/timer n", где n это число отсчитываемых минут.'
                                                     'За 30 секунд до окончания времени бот предупредит Вас об этом сообщением.\n'
                                                     'Таймер можно запустить находясь в любом разделе меню.\n'
                                                     'Отсчёт времени можно сбросить при помощи команды "/reset", отправив её боту.', reply_markup=nav.mainMenu, parse_mode=types.ParseMode.HTML)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
