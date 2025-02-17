from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from StomdiscontBot.bot.db import get_item, get_name

router = Router()


@router.message(CommandStart())
async def StartButton(message:Message):
    await message.answer("""Stomdiscont\n
    Стоматологические товары по низким ценам
    """, reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def Catalog_button(message:Message):
    await message.answer("Выберите категорию товара", reply_markup=kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery, state: FSMContext):
    try:
        category_id = callback.data.split('_')[1]
        await callback.answer('Вы выбрали категорию')
        ud = await state.get_data()
        if "basket" not in ud:
            await state.update_data(basket={})
        await callback.message.edit_text('Выберите товар по категории', reply_markup=kb.items(category_id))
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")
        print(f"Exception in category handler: {e}")


@router.callback_query(F.data == 'back')
async def to_back_page(callback:CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите категорию товара', reply_markup=kb.categories())


@router.callback_query(F.data == 'to_main')
async def to_main_page(callback:CallbackQuery):
    await callback.answer()
    await callback.message.delete()
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
        f'Название: {item_data[1]}\nОписание: {item_data[2]}\nЦена: {item_data[3]}р',
        reply_markup=add_to_basket
    )


@router.callback_query(F.data.startswith('add_basket'))
async def add_basket_b(callback:CallbackQuery, state: FSMContext):
    item_id = callback.data.split("-")[1]
    ud = await state.get_data()
    bskt = ud["basket"]
    if item_id in ud["basket"]:
        bskt[item_id] += 1
    else:
        bskt[item_id] = 1
    await state.update_data(basket=bskt)
    backet = ""
    for i_b in bskt:
        backet += f"{bskt[i_b]} x {get_name(i_b)}\n"
    await callback.answer('Товар в корзине!')
    await callback.message.delete()
    await callback.message.answer(f'Выберите категорию товара\n\n{backet}', reply_markup=kb.main_after)


@router.message(F.text == "Очистить корзину")
async def clear_bascket(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Корзина очищена", reply_markup=kb.main)


















# @router.callback_query(F.data == '-')
# async def minus(callback:CallbackQuery):
#     if amount_result == 0:
#         pass
#     elif amount_result > 0:
#         amount_result -= 1
#     await callback.message.edit_text('')
