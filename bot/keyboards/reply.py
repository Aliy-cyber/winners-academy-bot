from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy 4 ta menyu tugmalari."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🚀 Sinov darsiga yozilish"),
                KeyboardButton(text="📚 Kurslarimiz"),
            ],
            [
                KeyboardButton(text="🏢 Filiallar va Ustozlar"),
                KeyboardButton(text="📞 Bog’lanish va Tarmoqlar"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Quyidagi bo’limlardan birini tanlang 👇",
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqami yuborish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="yoki raqamingizni qoldiring",
    )


def back_keyboard() -> ReplyKeyboardMarkup:
    """Faqat orqaga tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Orqaga")]],
        resize_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
