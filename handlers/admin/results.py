import os
from datetime import datetime, timedelta

from aiogram import Router, F, types

from handlers.admin.users_ import download_users
from keyboards.reply.admin_buttons import results_main_kb
from loader import db
from utils.pgtoexcel import export_to_excel

router = Router()


@router.message(F.text.in_(["📊 Natijalar bo'limi", "Kunlik natijalar", "Haftalik natijalar", "Oylik natijalar"]))
async def kunlik_natijalar(message: types.Message):
    if message.text == "📊 Natijalar bo'limi":
        await message.answer(
            text=message.text, reply_markup=results_main_kb
        )

    today = datetime.now().date()
    send_to_xls = list()

    # Kunlik natijalar
    if message.text == "Kunlik natijalar":
        kunlik = await db.select_results_by_date(
            date=today
        )
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

    # Haftalik natijalar
    if message.text == "Haftalik natijalar":
        last_week = today - timedelta(days=today.weekday()) - timedelta(days=7)
        haftalik = await db.select_results_by_between(
            last=last_week, today=today
        )
        file_path = f"downloads/HAFTALIK_NATIJA_{today}.xlsx"
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

    # Oylik natijalar
    if message.text == "Oylik natijalar":
        first_day_of_month = today.replace(day=1)
        oylik = await db.select_results_by_between(
            last=first_day_of_month, today=today
        )
        file_path = f"downloads/OYLIK_NATIJA_{today}.xlsx"
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
