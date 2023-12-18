import telebot
from telebot import types


TOKEN = '6378053363:AAFDlqyTZqpKvqtn5zXhzHT3uJDZXHjtyiQ'
bot = telebot.TeleBot(TOKEN)

def generate_inline_markup(buttons):
    markup = types.InlineKeyboardMarkup()
    for button in buttons:
        markup.add(types.InlineKeyboardButton(text=button, callback_data=button))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = generate_inline_markup(['Печерський район', 'Шевченківський район', 'Подільський район', 'Оболонький район', 'Святошинський район'])
    bot.send_message(message.chat.id, '"ЖитлоБот" - це інтелектуальний телеграм-бот, який призначений для полегшення процесу пошуку та вибору житла. Бот створений з метою забезпечити користувачам швидкий та зручний доступ до актуальної інформації про квартири в оренду.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ['Печерський район', 'Шевченківський район', 'Подільський район', 'Оболонький район', 'Святошинський район']:
        markup = generate_inline_markup(['До 40 кв. м.', 'До 60 кв. м.', 'До 90 кв. м.', 'До 120 кв. м.', 'До 200 кв. м.', 'Back'])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ви обрали: " + call.data, reply_markup=markup)
    if call.data == 'До 40 кв. м.':
        bot.send_message('BLA BLA BLA BLA BLA')
    elif call.data == 'Back':
        markup = generate_inline_markup(['Печерський район', 'Шевченківський район', 'Подільський район', 'Оболонький район', 'Святошинський район'])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='"ЖитлоБот" - це інтелектуальний телеграм-бот, який призначений для полегшення процесу пошуку та вибору житла. Бот створений з метою забезпечити користувачам швидкий та зручний доступ до актуальної інформації про квартири в оренду.', reply_markup=markup)

@bot.message_handler(commands=['LOL'])
def send_welcome(message):
    # List of photo file IDs or file paths
    photo_files = ["D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-22 (2).jpg", "D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-22 (3).jpg", "D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-22 (4).jpg", "D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-22.jpg", "D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-23.jpg", "D:\\KSE\\Webinclass\\RieltorBot\\RieltorBot\\PrestigeHall\\photo_2023-12-18_23-45-24.jpg"]

    for photo in photo_files:
    # Send photo with optional caption
        bot.send_photo(message.chat.id, photo, caption="📍 #ЖКPrestigeHall\nВасиля Тютюнника вул., буд. 37/1\nПоверх: 11/25\nКвадратура: 60 м²\nКімнат: #1кімната\nЦіна: 1 100 $🔥\n📲 @at_chak\n📞 +380660195209\nⓂ️ метро #ПалацУкраїни 15 хвилин пішки 🚶")

bot.infinity_polling()
