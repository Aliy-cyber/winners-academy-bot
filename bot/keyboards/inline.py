from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ── CTA ────────────────────────────────────────────────────────────────────────────────
def cta_register_keyboard(back_callback: str = "back_to_main") -> InlineKeyboardMarkup:
    """Sinov darsiga yozilish CTA tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Birinchi bepul darsga yozilish", callback_data="register_start")
    builder.button(text="🏠 Asosiy menyu", callback_data=back_callback)
    builder.adjust(1)
    return builder.as_markup()


# ── Test ────────────────────────────────────────────────────────────────────────────────────
def quiz_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Bepul test (15 ta savol)", callback_data="quiz_start")
    builder.button(text="🎯 To’g’ridan-to’g’ri yozilish", callback_data="register_start")
    builder.adjust(1)
    return builder.as_markup()


def quiz_options_keyboard(q_id: int, options: list) -> InlineKeyboardMarkup:
    """Test savoli uchun A, B, C, D tugmalar."""
    builder = InlineKeyboardBuilder()
    labels = ["🅐", "🅑", "🅒", "🅓"]
    for i, opt in enumerate(options):
        builder.button(
            text=f"{labels[i]} {opt}",
            callback_data=f"quiz_answer:{q_id}:{i}",
        )
    builder.adjust(1)
    return builder.as_markup()


def quiz_result_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Sinov darsiga yozilish", callback_data="register_start")
    builder.button(text="🏠 Asosiy menyu", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()


# ── Filiallar ─────────────────────────────────────────────────────────────────────────────
def branches_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📍 Filiallar", callback_data="show_branches")
    builder.button(text="👨🏻‍🏫 Ustozlar", callback_data="show_teachers")
    builder.adjust(2)
    return builder.as_markup()


def branches_list_keyboard(branches: list) -> InlineKeyboardMarkup:
    """6 ta filial tugmalari."""
    builder = InlineKeyboardBuilder()
    for branch in branches:
        builder.button(
            text=f"{branch.icon} {branch.name}",
            callback_data=f"branch:{branch.id}",
        )
    builder.button(text="⬅️ Orqaga", callback_data="back_branches_menu")
    builder.adjust(2)
    return builder.as_markup()


def branch_detail_keyboard(branch_id: str) -> InlineKeyboardMarkup:
    """Filial batafsil sahifasidagi tugmalar."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="👨🏻‍🏫 Ushbu filialdagi ustozlarni ko’rish",
        callback_data=f"branch_teachers:{branch_id}",
    )
    builder.button(
        text="📍 Lokatsiyani ko’rish",
        callback_data=f"branch_location:{branch_id}",
    )
    builder.button(
        text="🚀 Shu filialda sinov darsiga yozilish",
        callback_data=f"register_from_branch:{branch_id}",
    )
    builder.button(text="⬅️ Filiallar ro’yxatiga", callback_data="show_branches")
    builder.adjust(1)
    return builder.as_markup()


def teachers_list_keyboard(branches: list) -> InlineKeyboardMarkup:
    """Barcha ustozlar (filial bo’yicha)."""
    builder = InlineKeyboardBuilder()
    for branch in branches:
        for t in branch.teachers:
            builder.button(
                text=f"{t.name} — {branch.icon}",
                callback_data=f"teacher:{branch.id}:{branch.teachers.index(t)}",
            )
    builder.button(text="⬅️ Orqaga", callback_data="back_branches_menu")
    builder.adjust(1)
    return builder.as_markup()


def teacher_detail_keyboard(branch_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚀 Shu filialda sinov darsiga yozilish",
        callback_data=f"register_from_branch:{branch_id}",
    )
    builder.button(text="⬅️ Ustozlar ro’yxatiga", callback_data="show_teachers")
    builder.adjust(1)
    return builder.as_markup()


# ── Kurslar ─────────────────────────────────────────────────────────────────────────────────
def courses_list_keyboard(courses: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for course in courses:
        builder.button(
            text=f"{course.icon} {course.name}",
            callback_data=f"course:{course.id}",
        )
    builder.adjust(2)
    return builder.as_markup()


def course_detail_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Sinov darsiga yozilish", callback_data="register_start")
    builder.button(text="⬅️ Kurslar ro’yxatiga", callback_data="back_courses")
    builder.adjust(1)
    return builder.as_markup()


# ── Ro’yxat: Filial tanlash ───────────────────────────────────────────────────────────────
def register_branches_keyboard(branches: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for branch in branches:
        builder.button(
            text=f"{branch.icon} {branch.name}",
            callback_data=f"reg_branch:{branch.id}",
        )
    builder.adjust(2)
    return builder.as_markup()


def register_courses_keyboard(courses: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for course in courses:
        builder.button(
            text=f"{course.icon} {course.name}",
            callback_data=f"reg_course:{course.id}",
        )
    builder.adjust(2)
    return builder.as_markup()


def register_time_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌅 Ertalab (08:00–12:00)", callback_data="reg_time:Ertalab (08:00–12:00)")
    builder.button(text="☀️ Tushdan keyin (14:00–18:00)", callback_data="reg_time:Tushdan keyin (14:00–18:00)")
    builder.button(text="🌙 Kechki (18:00–20:00)", callback_data="reg_time:Kechki (18:00–20:00)")
    builder.adjust(1)
    return builder.as_markup()
