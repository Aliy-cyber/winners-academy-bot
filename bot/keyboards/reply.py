from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="\U0001f680 Sinov darsiga yozilish"),
                KeyboardButton(text="\U0001f4da Kurslarimiz"),
            ],
            [
                KeyboardButton(text="\U0001f3e2 Filiallar va Ustozlar"),
                KeyboardButton(text="\U0001f4de Bog'lanish va Tarmoqlar"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Quyidagi bo'limlardan birini tanlang \U0001f447",
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="\U0001f4f2 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="\u2b05\ufe0f Orqaga")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="yoki raqamingizni qoldiring",
    )


def back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="\u2b05\ufe0f Orqaga")]],
        resize_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
