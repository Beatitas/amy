from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

'''
btnTime = InlineKeyboardButton(text ='Таймер на 3 минуты', callback_data='timer_3')
timeMenu = InlineKeyboardMarkup(row_width = 1)
timeMenu.insert(btnTime)
'''

btnPaypal = InlineKeyboardButton(text ='PAYPAL', url = 'https://www.paypal.me/aakittyhawk')
payMenu = InlineKeyboardMarkup(row_width = 1)
payMenu.insert(btnPaypal)

btnMain = KeyboardButton('👣 Вернуться в начало')
btnAdmin = KeyboardButton('😺 Я служащий')
btnUser = KeyboardButton('😃 Я новичок/участник')
btnTimer = KeyboardButton('⏱ Таймер')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnAdmin, btnUser, btnTimer)

# --- Меню админа (Admin's menu) ---
btnKittyHawk = KeyboardButton('✈ АА Китти Хок')
btnTraining = KeyboardButton('🏋️‍♀️ Обучающий режим')
menuModer = ReplyKeyboardMarkup(resize_keyboard = True).add(btnKittyHawk, btnTraining, btnMain)

btnThemesTrain = KeyboardButton('Случайная тема')
btnStepsTrain = KeyboardButton('12 шагов')
btnRulesTrain = KeyboardButton('Правила')
btnPony = KeyboardButton('🦄 Пони')
menuTrain = ReplyKeyboardMarkup(resize_keyboard = True).add(btnThemesTrain, btnStepsTrain, btnRulesTrain, btnPony, btnMain)

btnSeven = KeyboardButton('7️⃣ 7 традиция')
btnRandomTheme = KeyboardButton('📆 Случайная доп.тема')
btnStepsBot = KeyboardButton('🦶 12 шагов')
btnNineStep = KeyboardButton('9️⃣ Обещание 9 шага')
btnAdvert = KeyboardButton('📣 Блок объявлений')
btnTearoom = KeyboardButton('☕️ Правила чайной')
btnTable = KeyboardButton('🕰 Расписание')

menuKittyHawk = ReplyKeyboardMarkup(resize_keyboard = True).add(btnRandomTheme, btnSeven, btnStepsBot, btnNineStep, btnAdvert, btnTearoom, btnTable, btnMain)

# --- Меню пользователя (User's menu) ---
btnGroupAdress = KeyboardButton('👩‍❤️‍👨 Ищу группы АА онлайн')
btnSponsors = KeyboardButton('🥸 Ищу спонсора или доверенного')
menuUser = ReplyKeyboardMarkup(resize_keyboard = True).add(btnGroupAdress, btnSponsors, btnMain)

