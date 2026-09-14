import aiosqlite
from typing import List
from bot.config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tg_id INTEGER UNIQUE NOT NULL,"
            "username TEXT,"
            "full_name TEXT,"
            "language_code TEXT DEFAULT 'uz',"
            "is_blocked INTEGER DEFAULT 0,"
            "joined_at TEXT DEFAULT (datetime('now'))"
            ")"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS applications ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tg_id INTEGER NOT NULL,"
            "full_name TEXT,"
            "phone TEXT,"
            "branch TEXT,"
            "course TEXT,"
            "time_pref TEXT,"
            "quiz_score TEXT DEFAULT NULL,"
            "quiz_level TEXT DEFAULT NULL,"
            "created_at TEXT DEFAULT (datetime('now'))"
            ")"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS user_actions ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tg_id INTEGER NOT NULL,"
            "action TEXT NOT NULL,"
            "detail TEXT DEFAULT NULL,"
            "created_at TEXT DEFAULT (datetime('now'))"
            ")"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS broadcasts ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "text TEXT NOT NULL,"
            "sent_count INTEGER DEFAULT 0,"
            "failed_count INTEGER DEFAULT 0,"
            "created_at TEXT DEFAULT (datetime('now'))"
            ")"
        )
        await db.commit()


# ── Users ──────────────────────────────────────────────────────────────────────
async def save_user(tg_id: int, username: str, full_name: str, language_code: str = "uz"):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (tg_id, username, full_name, language_code) VALUES (?, ?, ?, ?)",
            (tg_id, username or "", full_name or "", language_code),
        )
        await db.execute(
            "UPDATE users SET username=?, full_name=? WHERE tg_id=?",
            (username or "", full_name or "", tg_id),
        )
        await db.commit()


async def get_all_users() -> List[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT tg_id, username, full_name, joined_at FROM users WHERE is_blocked=0 ORDER BY joined_at DESC"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_user_count() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users WHERE is_blocked=0")
        row = await cursor.fetchone()
        return row[0]


async def get_new_users_count(days: int = 1) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE joined_at >= datetime('now', ? || ' days') AND is_blocked=0",
            (f"-{days}",),
        )
        row = await cursor.fetchone()
        return row[0]


async def get_all_user_ids() -> List[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT tg_id FROM users WHERE is_blocked=0")
        rows = await cursor.fetchall()
        return [r[0] for r in rows]


async def mark_user_blocked(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET is_blocked=1 WHERE tg_id=?", (tg_id,))
        await db.commit()


# ── Applications ───────────────────────────────────────────────────────────────
async def save_application(
    tg_id: int,
    full_name: str,
    phone: str,
    branch: str,
    course: str,
    time_pref: str,
    quiz_score: str = None,
    quiz_level: str = None,
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO applications (tg_id, full_name, phone, branch, course, time_pref, quiz_score, quiz_level) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tg_id, full_name, phone, branch, course, time_pref, quiz_score, quiz_level),
        )
        await db.commit()


async def get_applications_count() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM applications")
        row = await cursor.fetchone()
        return row[0]


async def get_recent_applications(limit: int = 10) -> List[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM applications ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


# ── User Actions ───────────────────────────────────────────────────────────────
async def log_action(tg_id: int, action: str, detail: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO user_actions (tg_id, action, detail) VALUES (?, ?, ?)",
            (tg_id, action, detail),
        )
        await db.commit()


async def get_popular_actions(limit: int = 10) -> List[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT action, COUNT(*) as count FROM user_actions GROUP BY action ORDER BY count DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


# ── Broadcasts ─────────────────────────────────────────────────────────────────
async def save_broadcast(text: str, sent_count: int, failed_count: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO broadcasts (text, sent_count, failed_count) VALUES (?, ?, ?)",
            (text, sent_count, failed_count),
        )
        await db.commit()


async def get_broadcast_history(limit: int = 5) -> List[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, text, sent_count, failed_count, created_at FROM broadcasts "
            "ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
