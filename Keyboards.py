import sqlite3
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton

# main = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
#          [InlineKeyboardButton(text='Отзывы', callback_data='marks')]
#     ])

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)

main_after = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Очистить корзину')]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)


# Catalog_items = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Оформить заказ', callback_data='make_order')]
# ], resize_keyboard=True)

def categories():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    all_categories = cursor.fetchall()
    conn.close()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(0, len(all_categories), 2):
        buttons = []
        if i < len(all_categories):
            buttons.append(
                InlineKeyboardButton(text=all_categories[i][1], callback_data=f'category_{all_categories[i][0]}'))
        if i + 1 < len(all_categories):
            buttons.append(InlineKeyboardButton(text=all_categories[i + 1][1],
                                                callback_data=f'category_{all_categories[i + 1][0]}'))

        keyboard.inline_keyboard.append(buttons)

    keyboard.inline_keyboard.append([InlineKeyboardButton(text='На главную', callback_data='to_main')])

    return keyboard


def items(category_id):               #Ищет нужный предмет в выбранной категории по Foregnt Key, и по итогу возвращает кнопки с названиями категорий из БД
    try:
        category_id = int(category_id) # Преобразование к int, если необходимо

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM item WHERE category = ?', (category_id,))
        all_items = cursor.fetchall()
        conn.close()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        for i_item in all_items:
            keyboard.inline_keyboard.append(
                [
                    InlineKeyboardButton(text=i_item[1], callback_data=f'item_{i_item[0]}')
                ]
            )
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    except Exception as e:
        print(f"Exception in items: {e}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[]) # Обработка ошибки

    return keyboard







