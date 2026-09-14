from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.data.branches import BRANCHES, BRANCH_MAP
from bot.keyboards.inline import (
    branches_menu_keyboard,
    branches_list_keyboard,
    branch_detail_keyboard,
    teachers_list_keyboard,
    teacher_detail_keyboard,
)

router = Router(name="branches")


@router.message(F.text == "🏢 Filiallar va Ustozlar")
async def show_branches_menu(message: Message):
    text = (
        "🏢 <b>Filiallar va Ustozlar</b>\n\n"
        "Quyidagilardan birini tanlang:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=branches_menu_keyboard())


@router.callback_query(F.data == "back_branches_menu")
async def back_branches_menu(callback: CallbackQuery):
    text = "🏢 <b>Filiallar va Ustozlar</b>\n\nQuyidagilardan birini tanlang:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=branches_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "show_branches")
async def show_branches_list(callback: CallbackQuery):
    text = (
        "📍 <b>Bizning filiallarimiz</b>\n\n"
        "Termiz bo'ylab 6 ta filialimizda ta'lim beramiz.\n"
        "Ko'proq ma'lumot olish uchun filialni tanlang 👇"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=branches_list_keyboard(BRANCHES),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("branch:"))
async def show_branch_detail(callback: CallbackQuery):
    branch_id = callback.data.split(":")[1]
    branch = BRANCH_MAP.get(branch_id)
    if not branch:
        await callback.answer("Filial topilmadi!")
        return

    teachers_count = len(branch.teachers)
    text = (
        f"{branch.icon} <b>{branch.name}</b>\n\n"
        f"📍 <b>Manzil:</b> {branch.address}\n"
        f"🗺 <b>Mo'ljal:</b> {branch.landmark}\n\n"
        f"👨🏫 Ushbu filialda <b>{teachers_count} ta</b> tajribali ustozimiz ishlaydi\n"
        f"👇 Ustozlar bilan tanishish uchun tugmani bosing"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=branch_detail_keyboard(branch_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("branch_location:"))
async def send_branch_location(callback: CallbackQuery):
    branch_id = callback.data.split(":")[1]
    branch = BRANCH_MAP.get(branch_id)
    if not branch:
        await callback.answer("Filial topilmadi!")
        return

    await callback.message.answer_location(
        latitude=branch.latitude,
        longitude=branch.longitude,
    )
    await callback.message.answer(
        f"📍 <b>{branch.name}</b> manzili\n"
        f"🗺 Mo'ljal: {branch.landmark}\n\n"
        f"<i>Ustiga bosib Navigator orqali yo'l topishingiz mumkin!</i>",
        parse_mode="HTML",
        reply_markup=branch_detail_keyboard(branch_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("branch_teachers:"))
async def show_branch_teachers(callback: CallbackQuery):
    branch_id = callback.data.split(":")[1]
    branch = BRANCH_MAP.get(branch_id)
    if not branch:
        await callback.answer("Filial topilmadi!")
        return

    lines = [f"👨🏫 <b>{branch.icon} {branch.name} — Ustozlar</b>\n"]
    for t in branch.teachers:
        lines.append(
            f"👤 <b>{t.name}</b>\n"
            f"   📚 {t.specialization}\n"
            f"   🎓 Daraja: {t.level}\n"
            + (f"   ⭐️ {t.extra}\n" if t.extra else "")
        )

    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=teacher_detail_keyboard(branch_id),
    )
    await callback.answer()


@router.callback_query(F.data == "show_teachers")
async def show_all_teachers(callback: CallbackQuery):
    lines = ["👨🏫 <b>Barcha ustozlarimiz</b>\n"]
    for branch in BRANCHES:
        for t in branch.teachers:
            lines.append(
                f"\n{branch.icon} <b>{t.name}</b>\n"
                f"   📍 Filial: {branch.name}\n"
                f"   📚 Yo'nalish: {t.specialization}\n"
                f"   🎓 Daraja: {t.level}\n"
                + (f"   ⭐️ {t.extra}\n" if t.extra else "")
            )

    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=teachers_list_keyboard(BRANCHES),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("teacher:"))
async def show_teacher_detail(callback: CallbackQuery):
    parts = callback.data.split(":")
    branch_id = parts[1]
    teacher_idx = int(parts[2])

    branch = BRANCH_MAP.get(branch_id)
    if not branch or teacher_idx >= len(branch.teachers):
        await callback.answer("Ustoz topilmadi!")
        return

    t = branch.teachers[teacher_idx]
    text = (
        f"👤 <b>{t.name}</b>\n\n"
        f"📍 <b>Filial:</b> {branch.icon} {branch.name}\n"
        f"📚 <b>Ixtisoslik:</b> {t.specialization}\n"
        f"🎓 <b>Daraja:</b> {t.level}\n"
        + (f"⭐️ <b>Qo'shimcha:</b> {t.extra}\n" if t.extra else "")
        + "\n🚀 <i>Ushbu ustoz darsi bilan sinov darsiga yozilishingiz mumkin!</i>"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=teacher_detail_keyboard(branch_id),
    )
    await callback.answer()
