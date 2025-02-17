# import sqlite3
from gc import callbacks

from bot.DataBase.models import async_session
from bot.DataBase.models import Item
from sqlalchemy import select
from bot.DataBase.requests import get_categories, get_item_category
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# conn = sqlite3.connect('item.db')
# cursor = conn.cursor()
# cursor.execute("""
#
#     SELECT Catalog FROM items
# """)
# Catalog = cursor.fetchall()
# conn.close()


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
# Catalog_items = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Оформить заказ', callback_data='make_order')]
# ], resize_keyboard=True)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()




async def items(category_id):               #Ищет нужный предмет в выбранной категории по Foregnt Key, и по итогу возвращает кнопки с названиями категорий из БД
    try:
        category_id = int(category_id) # Преобразование к int, если необходимо
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Item).where(Item.category == category_id))
                buttons = []
                for item in result.scalars(): # Итерация по результату без .all()
                    buttons.append([InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}')])
                buttons.append([InlineKeyboardButton(text='Назад', callback_data='back')])
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    except Exception as e:
        print(f"Exception in items: {e}")
        keyboard = InlineKeyboardMarkup() # Обработка ошибки

    return keyboard







