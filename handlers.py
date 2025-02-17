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
        category_id = callback.data.split('_')[1]               # Получаем из callback_query ID категории.
        await callback.answer('Вы выбрали категорию')
        ud = await state.get_data()
        if "basket" not in ud:                                  # Проверяем, есть ли у нас в state корзина. state это не только FSM, а и локальная база данных, привязанная к одномц пользоваелю.
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
async def category(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.split('_')[1]  # Получаем из callback_query ID товара
    item_data = get_item(item_id)
    await callback.answer('Вы выбрали товар')

    ud = await state.get_data() # получаем данные из state

    if item_id in ud["basket"]:     # если данный товар есть, то мы можем его убрать (добавили кнопку минус), в ином случае, только добавить в корзину есть
        add_to_basket = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='+', callback_data=f'add_basket-{item_id}'),
                    InlineKeyboardButton(text='-', callback_data=f'delete_basket-{item_id}')
                ]
            ]
        )
    else:
        add_to_basket = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='+', callback_data=f'add_basket-{item_id}')
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
    ud = await state.get_data()  # получили данные из state
    bskt = ud["basket"]
    if item_id in ud["basket"]: # проверяем наличие товара, если есть в корзине, то добавляем, если нет, то создаем под него ключ. все данные в state хранятся в виде словаря (ключ - значение) (база данных называется - Redis)
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



@router.callback_query(F.data.startswith('delete_basket'))
async def delete_basket_b(callback:CallbackQuery, state: FSMContext):
    # здесь аналогично add_basket_b, только мы уверены на 100 проц, что товар есть
    item_id = callback.data.split("-")[1]
    ud = await state.get_data()
    bskt = ud["basket"]
    bskt[item_id] -= 1
    await state.update_data(basket=bskt)
    backet = ""
    for i_b in bskt:
        backet += f"{bskt[i_b]} x {get_name(i_b)}\n"
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f'Выберите категорию товара\n\n{backet}', reply_markup=kb.main_after)



@router.message(F.text == "Очистить корзину")
async def clear_bascket(message: Message, state: FSMContext):
    await state.clear() # очищаем state
    await message.answer("Корзина очищена", reply_markup=kb.main)





