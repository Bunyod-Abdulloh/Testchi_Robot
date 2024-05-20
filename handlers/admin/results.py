import os
from datetime import datetime, timedelta

from aiogram import Router, F, types

from handlers.admin.users_ import download_users
from keyboards.reply.admin_buttons import results_main_kb
from loader import db
from utils.pgtoexcel import export_to_excel

router = Router()


@router.message(F.text == "📊 Natijalar bo'limi")
async def kunlik_natijalar(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=results_main_kb
    )


@router.message(F.text == "Kunlik natijalar")
async def kunlik_natijalar(message: types.Message):
    today = datetime.today().date()
    kunlik = await db.select_results_by_date(
        date=today
    )
    send_to_xls = list()
    file_path = f"downloads/KUNLIK_NATIJA_{today}.xlsx"
    for n in kunlik:
        telegram_id = n['telegram_id']
        get_fullname = await db.select_user(
            telegram_id=n['telegram_id']
        )
        full_name = get_fullname['full_name']
        get_book = await db.select_book_by_id(
            id_=n['book_id']
        )
        book_name = get_book['table_name']
        result = str(n['result'])
        send_to_xls.append([today, telegram_id, full_name, book_name, result])
    await export_to_excel(data=send_to_xls, headings=["DATE", "TELEGRAM_ID", "FULL_NAME", "BOOK_NAME", "RESULT"],
                          filepath=file_path)
    await message.answer_document(document=types.input_file.FSInputFile(file_path),
                                  caption="Kunlik natijalar to'g'risidagi jadval")
    os.remove(file_path)


@router.message(F.text == "Haftalik natijalar")
async def haftalik_natijalar(message: types.Message):
    today = datetime.now().date()
    last_week = today - timedelta(days=today.weekday()) - timedelta(days=7)
    haftalik = await db.select_results_by_between(
        last=last_week, today=today
    )
    send_to_xls = list()
    file_path = f"downloads/HAFTALIK_NATIJA_{datetime.now().date()}.xlsx"
    for n in haftalik:
        telegram_id = n['telegram_id']
        get_fullname = await db.select_user(
            telegram_id=n['telegram_id']
        )
        full_name = get_fullname['full_name']
        get_book = await db.select_book_by_id(
            id_=n['book_id']
        )
        book_name = get_book['table_name']
        result = str(n['result'])
        send_to_xls.append([telegram_id, full_name, book_name, result])
    await export_to_excel(data=send_to_xls, headings=["TELEGRAM_ID", "FULL_NAME", "BOOK_NAME", "RESULT"],
                          filepath=file_path)
    await message.answer_document(document=types.input_file.FSInputFile(file_path),
                                  caption="Haftalik natijalar to'g'risidagi jadval")
    os.remove(file_path)


@router.message(F.text == "Oylik natijalar")
async def oylik_natijalar(message: types.Message):
    input_dt = datetime.now().date()
    first_day_of_month = input_dt.replace(day=1)
    current_date = datetime.now().date()
    oylik = await db.select_results_by_between(
        last=first_day_of_month, today=current_date
    )
    send_to_xls = list()
    file_path = f"downloads/OYLIK_NATIJA_{datetime.now().date()}.xlsx"
    for n in oylik:
        telegram_id = n['telegram_id']
        get_fullname = await db.select_user(
            telegram_id=n['telegram_id']
        )
        full_name = get_fullname['full_name']
        get_book = await db.select_book_by_id(
            id_=n['book_id']
        )
        book_name = get_book['table_name']
        result = str(n['result'])
        send_to_xls.append([telegram_id, full_name, book_name, result])
    await export_to_excel(data=send_to_xls, headings=["TELEGRAM_ID", "FULL_NAME", "BOOK_NAME", "RESULT"],
                          filepath=file_path)
    await message.answer_document(document=types.input_file.FSInputFile(file_path),
                                  caption="Oylik natijalar to'g'risidagi jadval")
    os.remove(file_path)


@router.message(F.text == "Barcha natijalar")
async def barcha_natijalar(message: types.Message):
    await download_users(message=message)
