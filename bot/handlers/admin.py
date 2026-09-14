import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import ADMIN_IDS
from bot.database import (
    get_user_count, get_new_users_count, get_all_user_ids,
    get_all_users, get_applications_count, get_recent_applications,
    get_popular_actions, save_broadcast, mark_user_blocked,
    get_broadcast_history,
)

logger = logging.getLogger(__name__)
router = Router(name="admin")


class BroadcastFSM(StatesGroup):
    waiting_message = State()
    confirm = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def admin_panel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Statistika", callback_data="adm_stats")
    builder.button(text="👥 Foydalanuvchilar", callback_data="adm_users")
    builder.button(text="📋 So'nggi arizalar", callback_data="adm_apps")
    builder.button(text="📈 Mashhur bo'limlar", callback_data="adm_actions")
    builder.button(text="📣 Broadcast (Xabar yuborish)", callback_data="adm_broadcast")
    builder.button(text="📨 Broadcast tarixi", callback_data="adm_broadcast_history")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def back_admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Admin Panel", callback_data="adm_panel")
    builder.adjust(1)
    return builder.as_markup()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ Sizda bu buyruqdan foydalanish huquqi yo'q.")
        return
    await message.answer(
        "🛡️ <b>Winners Academy — Admin Panel</b>\n\nQuyidagi bo'limlardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=admin_panel_keyboard(),
    )


@router.callback_query(F.data == "adm_panel")
async def cb_admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    await callback.message.edit_text(
        "🛡️ <b>Winners Academy — Admin Panel</b>\n\nQuyidagi bo'limlardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=admin_panel_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "adm_stats")
async def cb_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    total = await get_user_count()
    today = await get_new_users_count(1)
    week = await get_new_users_count(7)
    month = await get_new_users_count(30)
    apps = await get_applications_count()
    text = (
        "📊 <b>Bot Statistikasi</b>\n\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {total} ta\n"
        f"📅 <b>Bugun qo'shildi:</b> {today} ta\n"
        f"📆 <b>Bu hafta:</b> {week} ta\n"
        f"🗓 <b>Bu oy:</b> {month} ta\n\n"
        f"📝 <b>Jami arizalar:</b> {apps} ta"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_admin_keyboard())
    await callback.answer()


@router.callback_query(F.data == "adm_users")
async def cb_users(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    users = await get_all_users()
    if not users:
        await callback.message.edit_text("Hozircha foydalanuvchilar yo'q.", reply_markup=back_admin_keyboard())
        await callback.answer()
        return
    lines = ["👥 <b>So'nggi 20 ta foydalanuvchi:</b>\n"]
    for i, u in enumerate(users[:20], 1):
        uname = f"@{u['username']}" if u["username"] else "—"
        joined = u["joined_at"][:16] if u["joined_at"] else "—"
        lines.append(f"{i}. <b>{u['full_name']}</b> | {uname} | {joined}")
    lines.append(f"\n<i>Jami: {len(users)} ta foydalanuvchi</i>")
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_admin_keyboard())
    await callback.answer()


@router.callback_query(F.data == "adm_apps")
async def cb_applications(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    apps = await get_recent_applications(10)
    if not apps:
        await callback.message.edit_text("Hozircha arizalar yo'q.", reply_markup=back_admin_keyboard())
        await callback.answer()
        return
    lines = ["📋 <b>So'nggi 10 ta ariza:</b>\n"]
    for i, a in enumerate(apps, 1):
        score_text = f" | Test: {a['quiz_level']}" if a.get("quiz_level") else ""
        lines.append(
            f"{i}. <b>{a['full_name']}</b>\n"
            f"   📱 {a['phone']} | {a['branch']}\n"
            f"   📚 {a['course']} | {a['time_pref']}{score_text}\n"
            f"   🕐 {a['created_at'][:16]}\n"
        )
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_admin_keyboard())
    await callback.answer()


@router.callback_query(F.data == "adm_actions")
async def cb_popular_actions(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    actions = await get_popular_actions(10)
    if not actions:
        await callback.message.edit_text("Harakatlar yo'q.", reply_markup=back_admin_keyboard())
        await callback.answer()
        return
    lines = ["📈 <b>Eng mashhur bo'limlar:</b>\n"]
    for i, a in enumerate(actions, 1):
        lines.append(f"{i}. {a['action']} — <b>{a['count']}</b> marta")
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_admin_keyboard())
    await callback.answer()


@router.callback_query(F.data == "adm_broadcast")
async def cb_broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    total = await get_user_count()
    await callback.message.edit_text(
        f"📣 <b>Barcha foydalanuvchilarga xabar yuborish</b>\n\n"
        f"👥 Jami: <b>{total} ta</b> foydalanuvchiga yuboriladi.\n\n"
        "Yuboriladigan xabar matnini kiriting:\n"
        "<i>(HTML: &lt;b&gt;qalin&lt;/b&gt;, &lt;i&gt;kursiv&lt;/i&gt;)</i>",
        parse_mode="HTML",
        reply_markup=back_admin_keyboard(),
    )
    await state.set_state(BroadcastFSM.waiting_message)
    await callback.answer()


@router.message(BroadcastFSM.waiting_message)
async def get_broadcast_message(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(broadcast_text=message.text or "")
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Ha, yuboring!", callback_data="adm_broadcast_confirm")
    builder.button(text="❌ Bekor qilish", callback_data="adm_panel")
    builder.adjust(2)
    total = await get_user_count()
    await message.answer(
        f"📤 <b>Ko'rib chiqing:</b>\n\n{message.text}\n\n"
        f"<i>Bu xabar <b>{total} ta</b> foydalanuvchiga yuboriladi. Tasdiqlaysizmi?</i>",
        parse_mode="HTML",
        reply_markup=builder.as_markup(),
    )
    await state.set_state(BroadcastFSM.confirm)


@router.callback_query(F.data == "adm_broadcast_confirm", BroadcastFSM.confirm)
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    data = await state.get_data()
    text = data.get("broadcast_text", "")
    await state.clear()
    user_ids = await get_all_user_ids()
    total = len(user_ids)
    progress_msg = await callback.message.edit_text(f"⏳ Yuborilmoqda... 0 / {total}", reply_markup=None)
    sent = 0
    failed = 0
    for i, uid in enumerate(user_ids):
        try:
            await bot.send_message(uid, text, parse_mode="HTML")
            sent += 1
        except Exception as e:
            logger.warning(f"Broadcast failed for {uid}: {e}")
            if "blocked" in str(e).lower() or "deactivated" in str(e).lower():
                await mark_user_blocked(uid)
            failed += 1
        if (i + 1) % 20 == 0:
            try:
                await progress_msg.edit_text(f"⏳ Yuborilmoqda... {i + 1} / {total}")
            except Exception:
                pass
        await asyncio.sleep(0.05)
    await save_broadcast(text, sent, failed)
    await progress_msg.edit_text(
        f"✅ <b>Broadcast yakunlandi!</b>\n\n"
        f"📤 Yuborildi: <b>{sent}</b> ta\n"
        f"❌ Xatolik: <b>{failed}</b> ta\n"
        f"👥 Jami: <b>{total}</b> ta",
        parse_mode="HTML",
        reply_markup=back_admin_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "adm_broadcast_history")
async def cb_broadcast_history(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Huquq yo'q!", show_alert=True)
        return
    history = await get_broadcast_history(5)
    if not history:
        await callback.message.edit_text("Broadcast tarixi yo'q.", reply_markup=back_admin_keyboard())
        await callback.answer()
        return
    lines = ["📨 <b>So'nggi 5 ta broadcast:</b>\n"]
    for h in history:
        short = h["text"][:60] + ("..." if len(h["text"]) > 60 else "")
        lines.append(
            f"📤 <b>{h['sent_count']}</b> ga yuborildi | ❌ {h['failed_count']} xato\n"
            f"⏰ {h['created_at'][:16]}\n"
            f"<i>{short}</i>\n"
        )
    await callback.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_admin_keyboard())
    await callback.answer()
