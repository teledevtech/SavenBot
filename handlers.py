from aiogram import F, Router, Bot, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery, Dice
from aiogram.fsm.state import StatesGroup, State
import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from StomdiscontBot.bot.db import get_item

router = Router()


@router.message(CommandStart())
async def StartButton(message:Message):
    await message.answer("""Stomdiscont\n
    Стоматологические товары по низким ценам
    """, reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def Catalog_button(message:Message):
    await message.answer("Выберите категорию товара", reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, state: FSMContext):
    try:
        category_id = callback.data.split('_')[1]
        await callback.answer('Вы выбрали категорию')
        await state.update_data(basket={})
        await callback.message.answer('Выберите товар по категории', reply_markup=await kb.items(category_id))
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")
        print(f"Exception in category handler: {e}")


@router.callback_query(F.data == 'back')
async def to_back_page(callback:CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data == 'to_main')
async def to_main_page(callback:CallbackQuery):
    await callback.message.answer("""Stomdiscont\n
    Стоматологические товары по низким ценам
    """, reply_markup=kb.main)


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item_data = get_item(item_id)
    await callback.answer('Вы выбрали товар')
    add_to_basket = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в корзину!', callback_data=f'add_basket-{item_id}')
            ]
        ]
    )

    await callback.message.edit_text(
        f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}р',
        reply_markup=add_to_basket
    )


@router.callback_query(F.data.startswith('add_basket'))
async def add_basket_b(callback:CallbackQuery, state: FSMContext):
    item_id = F.data.split("-")[1]
    ud = await state.get_data()
    if item_id in ud["category_id"]:
        await state.update_data(basket=ud["basket"])
        ud["basket"][item_id] += 1
    else:
        ud["basket"][item_id] = 1

    await callback.answer('Товар в корзине!')
    await callback.message.edit_text('Выберите категорию товара', reply_markup=kb.main)






















# @router.callback_query(F.data == '-')
# async def minus(callback:CallbackQuery):
#     if amount_result == 0:
#         pass
#     elif amount_result > 0:
#         amount_result -= 1
#     await callback.message.edit_text('')
