import telebot
from telebot import types

# Токен бота
TOKEN = "6378053363:AAFDlqyTZqpKvqtn5zXhzHT3uJDZXHjtyiQ"
bot = telebot.TeleBot(TOKEN)

# Зберігання даних користувача
user_data = {}

# Послідовність кроків
STEPS = ['district', 'room', 'area', 'budget']

# Функція для отримання попереднього кроку
def get_prev_step(chat_id):
    current_index = STEPS.index(user_data[chat_id]['current_step'])
    return STEPS[max(0, current_index - 1)]

# Функція для обробки вибору користувача
def handle_choice(chat_id, data, message_id):
    current_step = user_data[chat_id]['current_step']
    user_data[chat_id][current_step] = data.split('_')[1]

    next_step_index = STEPS.index(current_step) + 1
    if next_step_index < len(STEPS):
        # Перехід до наступного кроку
        next_step = STEPS[next_step_index]
        user_data[chat_id]['current_step'] = next_step
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Вибрано {data.split('_')[1]}. Ваш наступний вибір:", reply_markup=get_keyboard(next_step))
    else:
        # Всі вибори зроблено, виведення результатів
        summary = "\n".join([f"{key}: {value}" for key, value in user_data[chat_id].items() if key != 'current_step'])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Фільтрація завершена! Ось ваші вибори:\n{summary}")

# Обробник всіх запитів від inline клавіатур
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if data == 'back':
        # Користувач натиснув кнопку "Назад"
        prev_step = get_prev_step(chat_id)
        user_data[chat_id]['current_step'] = prev_step
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"Повертаємось на крок: {prev_step}", reply_markup=get_keyboard(prev_step))
    else:
        # Обробка вибору користувача
        handle_choice(chat_id, data, call.message.message_id)

# Вітальне повідомлення
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'current_step': 'district'}
    bot.send_message(chat_id, "Привіт! Почнемо вибір району.", reply_markup=create_district_keyboard())

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

# Функція для отримання клавіатури залежно від кроку
def get_keyboard(step):
    keyboard = types.InlineKeyboardMarkup()
    # Додати кнопку "Назад" (крім першого кроку)
    if step != 'district':
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    # Визначення клавіатур для кожного кроку
    if step == 'district':
        return create_district_keyboard()
    elif step == 'room':
        return create_room_keyboard()
    elif step == 'area':
        return create_area_keyboard()
    elif step == 'budget':
        return create_budget_keyboard()
    return keyboard

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
