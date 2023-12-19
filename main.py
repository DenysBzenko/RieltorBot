import telebot
from telebot import types

# Створення бота
bot = telebot.TeleBot("6378053363:AAFDlqyTZqpKvqtn5zXhzHT3uJDZXHjtyiQ")

# Зберігання даних користувача
user_data = {}

# Обробник вітального повідомлення
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Привіт! Виберіть район:", reply_markup=create_district_keyboard())

# Обробник вибору району
@bot.callback_query_handler(func=lambda call: call.data.startswith('district_'))
def handle_district_choice(call):
    district = call.data.split('_')[1]
    user_data[call.message.chat.id]['district'] = district
    bot.send_message(call.message.chat.id, f"Вибрано район: {district}\nВиберіть кількість кімнат:", reply_markup=create_room_keyboard())

# Обробник вибору кількості кімнат
@bot.callback_query_handler(func=lambda call: call.data.startswith('room_'))
def handle_room_choice(call):
    room = call.data.split('_')[1]
    user_data[call.message.chat.id]['room'] = room
    bot.send_message(call.message.chat.id, f"Вибрано кількість кімнат: {room}\nВиберіть кількість кв.м:", reply_markup=create_area_keyboard())

# Обробник вибору кількості кв.м
@bot.callback_query_handler(func=lambda call: call.data.startswith('area_'))
def handle_area_choice(call):
    area = call.data.split('_')[1]
    user_data[call.message.chat.id]['area'] = area
    bot.send_message(call.message.chat.id, f"Вибрано кількість кв.м: {area}\nВиберіть Ваш максимальний бюджет:", reply_markup=create_budget_keyboard())

# Обробник вибору бюджету
@bot.callback_query_handler(func=lambda call: call.data.startswith('budget_'))
def handle_budget_choice(call):
    budget = call.data.split('_')[1]
    user_data[call.message.chat.id]['budget'] = budget
    bot.send_message(call.message.chat.id, f"Вибрано максимальний бюджет: {budget}\nГотово!", reply_markup=create_summary_keyboard(call.message.chat.id))

# Обробник натискання кнопок зі стиснутим текстом
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def callback_handler(call):
    chat_id = call.message.chat.id
    # Повернутися на попередній крок
    prev_step = user_data[chat_id].get('prev_step', 'start')
    bot.send_message(chat_id, f"Повертаємось на крок: {prev_step}", reply_markup=prev_step_keyboard(prev_step))

# Функції для створення клавіатур з кнопками
def create_district_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    districts = ["Голосіївський", "Печерський", "Шевченківський", "Соломʼянський", "Подільський", "Дарницький", "Дніпровський", "Оболонський", "Святошинський"]
    buttons = [types.InlineKeyboardButton(text=district, callback_data=f'district_{district}') for district in districts]
    keyboard.add(*buttons)
    return keyboard

def create_room_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    rooms = ["1-кімнатна", "2-кімнатна", "3-кімнатна", "4-кімнатна", "4+ -кімнатна"]
    buttons = [types.InlineKeyboardButton(text=room, callback_data=f'room_{room}') for room in rooms]
    keyboard.add(*buttons)
    return keyboard

def create_area_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    areas = ["до 30", "до 40", "до 50", "до 70", "до 90", "до 110", "до 130", "до 150", "до 170", "до 190", "від 200"]
    buttons = [types.InlineKeyboardButton(text=area, callback_data=f'area_{area}') for area in areas]
    keyboard.add(*buttons)
    return keyboard

def create_budget_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    budgets = ["до 800$", "до 900$", "до 1000$", "до 1100$", "до 1200$", "до 1300$", "до 1400$", "до 1500$", "до 1700$", "до 1900$", "до 2100$", "до 2300$", "до 2500$", "до 3000$", "від 3000$"]
    buttons = [types.InlineKeyboardButton(text=budget, callback_data=f'budget_{budget}') for budget in budgets]
    keyboard.add(*buttons)
    return keyboard

def create_summary_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard

def prev_step_keyboard(prev_step):
    if prev_step == 'start':
        return create_district_keyboard()
    elif prev_step == 'district':
        return create_room_keyboard()
    elif prev_step == 'room':
        return create_area_keyboard()
    elif prev_step == 'area':
        return create_budget_keyboard()

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
