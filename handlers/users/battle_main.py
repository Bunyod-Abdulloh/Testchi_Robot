from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.start import uz_start_buttons
from keyboards.inline.buttons import battle_ibuttons
from loader import db

router = Router()


async def result_time_game(start_time, end_time):
    """
    O'yin boshlangan va tugagan vaqtni qabul qilib oradagi
    farqni chiqaruvchi funksiya
    """
    difference = end_time - start_time
    return difference


@router.message(F.text == "⚔️ Bellashuv")
async def uz_battle_main(message: types.Message, state: FSMContext):
    await state.clear()
    telegram_id = message.from_user.id
    # Users jadvalidan game_on ustunini FALSE holatiga tushirish
    await db.edit_status_users(
        game_on=False, telegram_id=telegram_id
    )
    all_books = await db.select_all_tables()
    builder = InlineKeyboardBuilder()
    for book in all_books:
        if not book['questions']:
            pass
        else:
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{book['table_name']}", callback_data=f"table_{book['id']}"
                )
            )
    builder.add(
        types.InlineKeyboardButton(text=f"⬅️ Ortga", callback_data=f"back_battle_main")
    )
    builder.adjust(1)
    await message.answer(
        text="Savollar beriladigan kitob nomini tanlang",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("table_"))
async def get_book_name(call: types.CallbackQuery):
    book_id = int(call.data.split("_")[1])
    book_name = await db.select_book_by_id(
        id_=book_id
    )
    book = book_name['table_name']
    if book_name['comment_one']:
        book += f"\n\n{book_name['comment_one']}"
    await call.message.edit_text(
        text=f"{book}\n\nBellashuv turini tanlang", reply_markup=battle_ibuttons(
            random_opponent="Tasodifiy raqib bilan", offer_opponent="Do'stni taklif qilish",
            playing_alone="Yakka o'yin", back="Ortga", back_callback="back_select_book", book_id=str(book_id)
        )
    )


@router.callback_query(F.data == "back_battle_main")
async def uz_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )


@router.callback_query(F.data == "back_select_book")
async def uz_back_books(call: types.CallbackQuery):
    all_books = await db.select_all_tables()
    builder = InlineKeyboardBuilder()
    for book in all_books:
        if not book['questions']:
            pass
        else:
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{book['table_name']}", callback_data=f"table_{book['id']}"
                )
            )
    builder.add(
        types.InlineKeyboardButton(text=f"⬅️ Ortga", callback_data=f"back_battle_main")    )
    builder.adjust(1)
    await call.message.edit_text(
        text="Savollar beriladigan kitob nomini tanlang",
        reply_markup=builder.as_markup()
    )
