from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser, WebAppInfo


def main_button(competition: str, rating: str, manual: str, questions: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"⚔️ {competition}")
            ],
            [
                KeyboardButton(text=f"📊 {rating}"),
                KeyboardButton(text=f"ℹ️ {manual}", web_app=WebAppInfo(
                    url="https://telegra.ph/Testchi-Robot--Qollanma-05-27"
                ))
            ],
            [
                KeyboardButton(text=f"❓ {questions}")
            ]
        ],
        resize_keyboard=True
    )
    return markup


def rival_offer_cbutton(opponent_text: str, back_text: str):
    button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"🤝 {opponent_text}", request_user=KeyboardButtonRequestUser(request_id=1)
                               )
            ],
            [
                KeyboardButton(text=f"⬅️ {back_text}")
            ]
        ],
        resize_keyboard=True
    )
    return button
