print("""
╔══════════════════════════════════════════════════════════════╗
║         PORO BOT - ربات مدیریت کامل بله                    ║
║         نسخه: poro v3.0 (debugged)                         ║
║         زبان: Python 3.10+                                  ║
╚══════════════════════════════════════════════════════════════╝
""")

import requests
import time
import sqlite3
import os
import sys
import json
import hashlib
import random
import string
import subprocess
import threading
import logging
import traceback
import zipfile
import shutil
import ast
import re
import importlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any

# ─────────────────────────────────────────────
#  پیکربندی اصلی
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  پیکربندی اصلی و متغیرهای محیطی برای ریلوای
# ─────────────────────────────────────────────
TOKEN = os.getenv("BOT_TOKEN")  
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "2063033830").split(",")]
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN", "WALLET-TEST-1111111111111111")
CHANNEL_USERNAME = "@koddan"
INVITE_BASE = "https://ble.ir/kodbot?start="
REQUIRED_INVITES = 1

# ─────────────────────────────────────────────
#  تنظیم مسیرها بر اساس دیسک پایدار ریلوای (/app/data)
# ─────────────────────────────────────────────
DATA_DIR = Path("/app/data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = str(DATA_DIR / "kodbot_pororjrhmaxsing.db")
BOTS_DIR = DATA_DIR / "deploydjhred_bots"
LOGS_DIR = DATA_DIR / "botndnd_logs"
LIBS_DIR = DATA_DIR / "crjjdnustom_libs"

BOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
LIBS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
#  تنظیمات لاگر
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("PoroBot")

# ─────────────────────────────────────────────
#  سطوح کاربری
# ─────────────────────────────────────────────
PLANS = {
    "free": {
        "name": "🟢 رایگان",
        "max_bots": 1,
        "max_code_lines": 50,
        "max_memory_mb": 50,
        "max_libraries": 1,
        "log_retention_days": 1,
        "support_level": "معمولی (پاسخ در ۲۴ ساعت)",
        "monthly_bandwidth_gb": 1,
        "max_concurrent_connections": 2,
        "bot_uptime_hours": 240,
        "auto_recovery": True,
        "powerful_terminal": False,
        "custom_library": False,
        "personal_mirror": False,
        "processing_priority": "low",
        "max_discount_codes": 0,
        "subscriptions": {
            "monthly": {"price": 0, "gift_points": 10, "max_buy": 1}
        }
    },
    "basic": {
        "name": "🟡 پایه",
        "max_bots": 3,
        "max_code_lines": 200,
        "max_memory_mb": 100,
        "max_libraries": 10,
        "log_retention_days": 7,
        "support_level": "سریع (پاسخ در ۱۲ ساعت)",
        "monthly_bandwidth_gb": 5,
        "max_concurrent_connections": 5,
        "bot_uptime_hours": 720,
        "auto_recovery": True,
        "powerful_terminal": True,
        "custom_library": False,
        "personal_mirror": True,
        "processing_priority": "medium",
        "max_discount_codes": 1,
        "extra_costs": {
            "bandwidth_gb": 8000,
            "memory_mb": 1500,
            "extra_bot": 25000,
            "extra_code_line": 500
        },
        "subscriptions": {
            "monthly": {"price": 50000, "gift_points": 120, "max_buy": 3},
            "quarterly": {"price": 150000, "gift_points": 250, "max_buy": 3},
            "biannual": {"price": 300000, "gift_points": 450, "max_buy": 2},
            "annual": {"price": 600000, "gift_points": 800, "max_buy": 1}
        },
        "mandatory_upgrade": {
            "enabled": True,
            "condition": "buy_3_basic",
            "target_plan": "professional"
        }
    },
    "professional": {
        "name": "🔴 حرفه‌ای",
        "max_bots": 10,
        "max_code_lines": -1,
        "max_memory_mb": 1024,
        "max_libraries": -1,
        "log_retention_days": 30,
        "support_level": "ویژه (پاسخ در ۶ ساعت)",
        "monthly_bandwidth_gb": 20,
        "max_concurrent_connections": 15,
        "bot_uptime_hours": -1,
        "auto_recovery": True,
        "powerful_terminal": True,
        "custom_library": True,
        "personal_mirror": True,
        "processing_priority": "high",
        "max_discount_codes": 2,
        "extra_costs": {
            "bandwidth_gb": 6000,
            "memory_mb": 1200,
            "extra_bot": 20000,
            "extra_code_line": 0
        },
        "subscriptions": {
            "monthly": {"price": 150000, "gift_points": 200, "max_buy": 3},
            "quarterly": {"price": 450000, "gift_points": 400, "max_buy": 2},
            "biannual": {"price": 900000, "gift_points": 650, "max_buy": 2},
            "annual": {"price": 1800000, "gift_points": 950, "max_buy": 1}
        }
    },
    "enterprise": {
        "name": "⚫ سازمانی",
        "max_bots": -1,
        "max_code_lines": -1,
        "max_memory_mb": 4096,
        "max_libraries": -1,
        "log_retention_days": 90,
        "support_level": "۲۴/۷ (پاسخ فوری)",
        "monthly_bandwidth_gb": 100,
        "max_concurrent_connections": -1,
        "bot_uptime_hours": -1,
        "auto_recovery": True,
        "powerful_terminal": True,
        "custom_library": True,
        "personal_mirror": True,
        "processing_priority": "critical",
        "max_discount_codes": 5,
        "subscriptions": {
            "monthly": {"price": -1, "gift_points": 300},
            "quarterly": {"price": -1, "gift_points": 500},
            "biannual": {"price": -1, "gift_points": 750},
            "annual": {"price": -1, "gift_points": 1000}
        }
    }
}

SHOP_ITEMS = {
    "extra_bot": {
        "name": "🤖 ربات اضافه",
        "desc": "افزایش سقف تعداد ربات‌های قابل استقرار",
        "points": {"free": None, "basic": 25, "professional": 15, "enterprise": 5}
    },
    "extra_memory": {
        "name": "💾 حافظه اضافی",
        "desc": "افزایش سقف حافظه (۱۰۰ مگابایت)",
        "points": {"free": None, "basic": 15, "professional": 10, "enterprise": 3}
    },
    "extra_log": {
        "name": "📋 لاگ اضافی",
        "desc": "افزایش مدت نگهداری لاگ (۷ روز)",
        "points": {"free": None, "basic": 10, "professional": 7, "enterprise": 2}
    },
    "extra_library": {
        "name": "📦 کتابخانه اضافی",
        "desc": "افزایش سقف تعداد کتابخانه‌های قابل نصب",
        "points": {"free": None, "basic": 8, "professional": 5, "enterprise": 1}
    },
    "extra_bandwidth": {
        "name": "🌐 پهنای باند اضافی",
        "desc": "افزایش سقف پهنای باند ماهانه (۱ گیگابایت)",
        "points": {"free": None, "basic": 20, "professional": 12, "enterprise": 4}
    }
}

# ─────────────────────────────────────────────
#  دیتابیس
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        plan TEXT DEFAULT 'free',
        points INTEGER DEFAULT 0,
        invite_count INTEGER DEFAULT 0,
        invited_by INTEGER DEFAULT NULL,
        is_active INTEGER DEFAULT 0,
        is_blocked INTEGER DEFAULT 0,
        block_reason TEXT DEFAULT NULL,
        block_until TEXT DEFAULT NULL,
        channel_joined INTEGER DEFAULT 0,
        joined_at TEXT DEFAULT NULL,
        last_active TEXT DEFAULT NULL,
        total_spent INTEGER DEFAULT 0,
        plan_expires_at TEXT DEFAULT NULL,
        extra_bots INTEGER DEFAULT 0,
        extra_memory_mb INTEGER DEFAULT 0,
        extra_log_days INTEGER DEFAULT 0,
        extra_libraries INTEGER DEFAULT 0,
        extra_bandwidth_gb INTEGER DEFAULT 0,
        basic_buy_count INTEGER DEFAULT 0,
        subscription_duration TEXT DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS deployed_bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bot_name TEXT,
        file_path TEXT,
        extra_files TEXT DEFAULT '[]',
        status TEXT DEFAULT 'pending',
        approved_by INTEGER DEFAULT NULL,
        deployed_at TEXT DEFAULT NULL,
        log_file TEXT DEFAULT NULL,
        pid INTEGER DEFAULT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS library_installs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        library_name TEXT,
        mirror_url TEXT DEFAULT NULL,
        status TEXT DEFAULT 'pending',
        approved_by INTEGER DEFAULT NULL,
        installed_at TEXT DEFAULT NULL,
        tracking_code TEXT UNIQUE,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS custom_libraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        lib_name TEXT,
        lib_key TEXT UNIQUE,
        mappings TEXT DEFAULT '{}',
        file_path TEXT DEFAULT NULL,
        created_at TEXT DEFAULT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        duration TEXT,
        amount INTEGER,
        status TEXT DEFAULT 'pending',
        transaction_id TEXT,
        provider_id TEXT,
        payload TEXT,
        created_at TEXT DEFAULT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS discount_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        type TEXT,
        value INTEGER,
        is_percent INTEGER DEFAULT 1,
        max_uses INTEGER DEFAULT 1,
        used_count INTEGER DEFAULT 0,
        expires_at TEXT DEFAULT NULL,
        created_by INTEGER,
        plan_target TEXT DEFAULT NULL,
        is_active INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS discount_uses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code_id INTEGER,
        user_id INTEGER,
        used_at TEXT,
        UNIQUE(code_id, user_id)
    );

    CREATE TABLE IF NOT EXISTS weekly_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start TEXT,
        week_end TEXT,
        active_users INTEGER DEFAULT 0,
        new_users INTEGER DEFAULT 0,
        active_bots INTEGER DEFAULT 0,
        stopped_bots INTEGER DEFAULT 0,
        lib_installs INTEGER DEFAULT 0,
        revenue INTEGER DEFAULT 0,
        data TEXT DEFAULT '{}'
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        message TEXT,
        status TEXT DEFAULT 'open',
        reply TEXT DEFAULT NULL,
        replied_by INTEGER DEFAULT NULL,
        created_at TEXT DEFAULT NULL,
        replied_at TEXT DEFAULT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS code_challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'active',
        created_by INTEGER,
        created_at TEXT DEFAULT NULL,
        winner_user_id INTEGER DEFAULT NULL,
        prize_desc TEXT DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS challenge_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenge_id INTEGER,
        user_id INTEGER,
        code_file TEXT,
        submitted_at TEXT DEFAULT NULL,
        FOREIGN KEY(challenge_id) REFERENCES code_challenges(id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS lotteries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        prize TEXT,
        min_points INTEGER DEFAULT 0,
        max_winners INTEGER DEFAULT 1,
        status TEXT DEFAULT 'active',
        created_by INTEGER,
        created_at TEXT DEFAULT NULL,
        drawn_at TEXT DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS lottery_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lottery_id INTEGER,
        user_id INTEGER,
        entered_at TEXT DEFAULT NULL,
        UNIQUE(lottery_id, user_id)
    );

    CREATE TABLE IF NOT EXISTS admin_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );

    CREATE TABLE IF NOT EXISTS pending_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        user_id INTEGER,
        data TEXT DEFAULT '{}',
        status TEXT DEFAULT 'pending',
        admin_msg_id INTEGER DEFAULT NULL,
        created_at TEXT DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        state TEXT,
        data TEXT DEFAULT '{}',
        updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        media_file_id TEXT DEFAULT NULL,
        media_type TEXT DEFAULT NULL,
        status TEXT DEFAULT 'draft',
        sent_count INTEGER DEFAULT 0,
        created_by INTEGER,
        created_at TEXT DEFAULT NULL,
        sent_at TEXT DEFAULT NULL
    );

    CREATE TABLE IF NOT EXISTS code_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_type TEXT,
        title TEXT,
        description TEXT,
        budget INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        admin_reply TEXT DEFAULT NULL,
        replied_by INTEGER DEFAULT NULL,
        file_path TEXT DEFAULT NULL,
        created_at TEXT DEFAULT NULL,
        replied_at TEXT DEFAULT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """)

    conn.commit()
    conn.close()
    log.info("✅ دیتابیس آماده شد.")


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # جلوگیری از lock در multi-thread
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def get_user(user_id: int) -> Optional[Dict]:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        return dict(row) if row else None


def upsert_user(user_id: int, username: str = None, full_name: str = None):
    now = datetime.now().isoformat()
    with get_db() as conn:
        existing = conn.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,)).fetchone()
        if existing:
            conn.execute(
                "UPDATE users SET username=?, full_name=?, last_active=? WHERE user_id=?",
                (username, full_name, now, user_id)
            )
        else:
            conn.execute(
                "INSERT INTO users (user_id, username, full_name, joined_at, last_active) VALUES (?,?,?,?,?)",
                (user_id, username, full_name, now, now)
            )
        conn.commit()


def get_setting(key: str, default=None):
    with get_db() as conn:
        row = conn.execute("SELECT value FROM admin_settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key: str, value: str):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO admin_settings (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value)
        )
        conn.commit()


# ─────────────────────────────────────────────
#  توابع API بله
# ─────────────────────────────────────────────
def api(method: str, data: dict = None, files=None) -> dict:
    url = f"{BASE_URL}/{method}"
    try:
        if files:
            r = requests.post(url, data=data, files=files, timeout=30)
        else:
            r = requests.post(url, json=data, timeout=30)
        return r.json()
    except Exception as e:
        log.error(f"API Error [{method}]: {e}")
        return {"ok": False, "error": str(e)}


def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown",
                 reply_to_message_id=None, disable_web_page_preview=True):
    d = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_web_page_preview
    }
    if reply_markup:
        d["reply_markup"] = reply_markup
    if reply_to_message_id:
        d["reply_to_message_id"] = reply_to_message_id
    return api("sendMessage", d)


def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
    d = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        d["reply_markup"] = reply_markup
    return api("editMessageText", d)


def answer_callback(callback_id, text="", alert=False):
    return api("answerCallbackQuery", {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": alert
    })


def send_document(chat_id, file_path, caption="", reply_to=None):
    with open(file_path, "rb") as f:
        d = {"chat_id": chat_id, "caption": caption}
        if reply_to:
            d["reply_to_message_id"] = reply_to
        return api("sendDocument", d, files={"document": f})


def send_photo(chat_id, file_path, caption=""):
    with open(file_path, "rb") as f:
        return api("sendPhoto", {"chat_id": chat_id, "caption": caption}, files={"photo": f})


def send_invoice(chat_id, title, description, payload, prices, photo_url=None, reply_to=None):
    global PAYMENT_TOKEN
    pt = get_setting("payment_token", PAYMENT_TOKEN)
    d = {
        "chat_id": chat_id,
        "title": title,
        "description": description,
        "payload": payload,
        "provider_token": pt,
        "currency": "IRR",
        "prices": prices
    }
    if photo_url:
        d["photo_url"] = photo_url
    if reply_to:
        d["reply_to_message_id"] = reply_to
    return api("sendInvoice", d)


def get_updates(offset=0, timeout=30):
    r = requests.get(
        f"{BASE_URL}/getUpdates",
        params={"offset": offset, "timeout": timeout},
        timeout=timeout + 5
    )
    return r.json()


def delete_message(chat_id, message_id):
    return api("deleteMessage", {"chat_id": chat_id, "message_id": message_id})


def send_broadcast(text, parse_mode="Markdown"):
    with get_db() as conn:
        users = conn.execute("SELECT user_id FROM users").fetchall()
    ok = 0
    fail = 0
    for u in users:
        try:
            res = send_message(u["user_id"], text, parse_mode=parse_mode)
            if res.get("ok"):
                ok += 1
            else:
                fail += 1
        except:
            fail += 1
        time.sleep(0.3)
    return ok, fail


# ─────────────────────────────────────────────
#  کیبوردهای inline
# ─────────────────────────────────────────────
def inline_keyboard(buttons: list) -> dict:
    """
    buttons = [[(\"متن\", \"callback_data\"), ...], ...]
    یا برای URL: [(\"متن\", \"url\", \"https://...\")]
    """
    keyboard = []
    for row in buttons:
        r = []
        for btn in row:
            if len(btn) == 3 and btn[1] == "url":
                r.append({"text": btn[0], "url": btn[2]})
            else:
                r.append({"text": btn[0], "callback_data": btn[1]})
        keyboard.append(r)
    return {"inline_keyboard": keyboard}


def glass_keyboard(items: list, prefix: str, cols: int = 2) -> dict:
    """ساخت کیبورد شیشه‌ای از لیست آیتم‌ها"""
    rows = []
    row = []
    for i, item in enumerate(items):
        row.append((item["label"], f"{prefix}:{item['id']}"))
        if len(row) == cols:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return inline_keyboard(rows)


# ─────────────────────────────────────────────
#  وضعیت کاربران (FSM - ذخیره در دیتابیس)
# ─────────────────────────────────────────────

def set_state(user_id: int, state: str, data: dict = None):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO user_states (user_id, state, data, updated_at) VALUES (?,?,?,?)"
            " ON CONFLICT(user_id) DO UPDATE SET state=excluded.state, data=excluded.data, updated_at=excluded.updated_at",
            (user_id, state, json.dumps(data or {}, ensure_ascii=False), datetime.now().isoformat())
        )
        conn.commit()


def get_state(user_id: int) -> Dict:
    with get_db() as conn:
        row = conn.execute("SELECT state, data FROM user_states WHERE user_id=?", (user_id,)).fetchone()
        if row:
            return {"state": row["state"], "data": json.loads(row["data"])}
        return {"state": None, "data": {}}


def clear_state(user_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM user_states WHERE user_id=?", (user_id,))
        conn.commit()


# ─────────────────────────────────────────────
#  بررسی مجوزها و پلن
# ─────────────────────────────────────────────
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def is_active_user(user_id: int) -> bool:
    u = get_user(user_id)
    if not u:
        return False
    return bool(u["is_active"]) and not bool(u["is_blocked"])


def check_plan_limit(user_id: int, resource: str) -> tuple:
    """بررسی آیا کاربر به محدودیت رسیده"""
    u = get_user(user_id)
    if not u:
        return False, "کاربر یافت نشد"
    plan = PLANS.get(u["plan"], PLANS["free"])

    if resource == "bots":
        max_val = plan["max_bots"]
        if max_val != -1:
            max_val += u.get("extra_bots", 0)
        with get_db() as conn:
            count = conn.execute(
                "SELECT COUNT(*) as c FROM deployed_bots WHERE user_id=? AND status='running'",
                (user_id,)
            ).fetchone()["c"]
        if max_val != -1 and count >= max_val:
            return False, f"به حداکثر تعداد ربات ({max_val}) رسیده‌اید"
        return True, count

    if resource == "libraries":
        max_val = plan["max_libraries"]
        if max_val != -1:
            max_val += u.get("extra_libraries", 0)
        with get_db() as conn:
            count = conn.execute(
                "SELECT COUNT(*) as c FROM library_installs WHERE user_id=? AND status='installed'",
                (user_id,)
            ).fetchone()["c"]
        if max_val != -1 and count >= max_val:
            return False, f"به حداکثر تعداد کتابخانه ({max_val}) رسیده‌اید"
        return True, count

    return True, None


def get_effective_plan(user_id: int) -> dict:
    u = get_user(user_id)
    if not u:
        return PLANS["free"]
    return PLANS.get(u["plan"], PLANS["free"])


# ─────────────────────────────────────────────
#  سیستم امتیاز
# ─────────────────────────────────────────────
def add_points(user_id: int, amount: int, reason: str = ""):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET points = points + ? WHERE user_id=?",
            (amount, user_id)
        )
        conn.commit()
    log.info(f"امتیاز {amount} به {user_id} داده شد: {reason}")


def get_points(user_id: int) -> int:
    u = get_user(user_id)
    return u["points"] if u else 0


def spend_points(user_id: int, amount: int) -> bool:
    u = get_user(user_id)
    if not u or u["points"] < amount:
        return False
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET points = points - ? WHERE user_id=?",
            (amount, user_id)
        )
        conn.commit()
    return True


# ─────────────────────────────────────────────
#  سیستم دعوت و فعال‌سازی
# ─────────────────────────────────────────────
def get_invite_link(user_id: int) -> str:
    return f"{INVITE_BASE}{user_id}"


_invite_lock = threading.Lock()


def process_invite(new_user_id: int, inviter_id: int):
    """پردازش دعوت جدید"""
    with _invite_lock:
        with get_db() as conn:
            u = conn.execute("SELECT invited_by FROM users WHERE user_id=?", (new_user_id,)).fetchone()
            if u and u["invited_by"]:
                return  # قبلاً دعوت شده

            conn.execute(
                "UPDATE users SET invited_by=? WHERE user_id=?",
                (inviter_id, new_user_id)
            )
            conn.execute(
                "UPDATE users SET invite_count = invite_count + 1 WHERE user_id=?",
                (inviter_id,)
            )
            conn.commit()

            # بررسی آیا دعوت‌کننده به ۵ دعوت رسیده
            inviter = conn.execute("SELECT * FROM users WHERE user_id=?", (inviter_id,)).fetchone()
            if inviter and inviter["invite_count"] >= REQUIRED_INVITES and not inviter["is_active"] and inviter["channel_joined"]:
                activate_user(inviter_id)

        # امتیاز فقط یک‌بار داده می‌شود (بیرون از if/else)
        add_points(inviter_id, 5, "دعوت موفق")


def activate_user(user_id: int):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET is_active=1 WHERE user_id=?",
            (user_id,)
        )
        conn.commit()
    send_message(user_id, "🎉 *تبریک!* ربات برای شما فعال شد!\nاکنون می‌توانید از تمام امکانات استفاده کنید.")


def check_activation(user_id: int) -> tuple:
    """بررسی شرایط فعال‌سازی، برگرداندن (ok, reason)"""
    u = get_user(user_id)
    if not u:
        return False, "not_found"
    if u["is_active"]:
        return True, "active"
    if u["invite_count"] < REQUIRED_INVITES:
        return False, f"need_invites:{REQUIRED_INVITES - u['invite_count']}"
    if not u["channel_joined"]:
        return False, "need_channel"
    return True, "ready"


# ─────────────────────────────────────────────
#  منوی اصلی
# ─────────────────────────────────────────────
def main_menu(user_id: int) -> dict:
    buttons = [
        [("🤖 مدیریت ربات‌ها", "bots_menu"), ("🚀 استقرار ربات جدید", "deploy_new")],
        [("📦 نصب کتابخانه", "install_lib"), ("🏪 فروشگاه آیتم", "shop_menu")],
        [("💳 خرید اشتراک", "sub_menu"), ("🎯 امتیازها", "points_menu")],
        [("🏆 کاربران برتر", "top_users"), ("🎟 چالش‌های کد", "challenges")],
        [("📊 آمار شخصی", "my_stats"), ("🎪 قرعه‌کشی", "lottery_menu")],
        [("🎫 تیکت پشتیبانی", "ticket_menu"), ("🔑 کتابخانه اختصاصی", "custom_lib")],
        [("🔗 لینک دعوت", "my_invite"), ("👤 پروفایل من", "my_profile")],
    ]
    if is_admin(user_id):
        buttons.append([("⚙️ پنل مدیریت", "admin_panel")])
    return inline_keyboard(buttons)


# ─────────────────────────────────────────────
#  هندلر /start
# ─────────────────────────────────────────────
def handle_start(message: dict, payload: str = ""):
    user_id = message["from"]["id"]
    username = message["from"].get("username", "")
    full_name = f"{message['from'].get('first_name','')} {message['from'].get('last_name','')}".strip()

    upsert_user(user_id, username, full_name)

    # پردازش دعوت
    if payload and payload.isdigit():
        inviter_id = int(payload)
        if inviter_id != user_id:
            process_invite(user_id, inviter_id)

    if is_admin(user_id):
        with get_db() as conn:
            conn.execute("UPDATE users SET is_active=1, channel_joined=1 WHERE user_id=?", (user_id,))
            conn.commit()
        send_message(
            user_id,
            f"👑 *خوش آمدید مدیر عزیز!*\n\n"
            f"به ربات *کدبات* خوش آمدید.\n"
            f"از منوی زیر انتخاب کنید:",
            reply_markup=main_menu(user_id)
        )
        return

    u = get_user(user_id)
    ok, reason = check_activation(user_id)

    if ok:
        send_message(
            user_id,
            f"👋 *{full_name} عزیز، خوش آمدید!*\n\n"
            f"🤖 به *کدبات* خوش آمدید.\n"
            f"از منوی زیر انتخاب کنید:",
            reply_markup=main_menu(user_id)
        )
    elif reason.startswith("need_invites"):
        needed = reason.split(":")[1]
        invite_link = get_invite_link(user_id)
        send_message(
            user_id,
            f"👋 *{full_name} عزیز، خوش آمدید!*\n\n"
            f"برای فعال‌سازی ربات، باید *{needed} نفر دیگر* را دعوت کنید.\n\n"
            f"🔗 لینک دعوت شما:\n`{invite_link}`\n\n"
            f"تعداد دعوت‌های موفق: *{u['invite_count'] if u else 0}/{REQUIRED_INVITES}*",
            reply_markup=inline_keyboard([
                [("🔗 کپی لینک دعوت", "my_invite")],
                [("✅ بررسی وضعیت", "check_activation")]
            ])
        )
    elif reason == "need_channel":
        send_message(
            user_id,
            f"👋 *{full_name} عزیز خوش آمدید!*\n\n"
            f"برای فعال‌سازی ربات، باید در کانال ما عضو شوید:",
            reply_markup=inline_keyboard([
                [("📢 عضویت در کانال", "url", f"https://ble.ai/{CHANNEL_USERNAME[1:]}")],
                [("✅ عضو شدم", "joined_channel")]
            ])
        )


# ─────────────────────────────────────────────
#  هندلر مدیریت ربات‌ها
# ─────────────────────────────────────────────
def handle_bots_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        bots = conn.execute(
            "SELECT * FROM deployed_bots WHERE user_id=? ORDER BY id DESC",
            (user_id,)
        ).fetchall()

    if not bots:
        edit_message(
            chat_id, msg_id,
            "🤖 *ربات‌های شما*\n\nهنوز هیچ ربات مستقری ندارید.",
            reply_markup=inline_keyboard([
                [("🚀 استقرار ربات جدید", "deploy_new")],
                [("🔙 بازگشت", "main_menu")]
            ])
        )
        return

    items = [{"label": f"{'🟢' if b['status']=='running' else '🔴'} {b['bot_name']}", "id": b["id"]} for b in bots]
    kb = glass_keyboard(items, "bot_info", cols=2)
    kb["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "main_menu"}])

    edit_message(
        chat_id, msg_id,
        f"🤖 *ربات‌های شما* ({len(bots)} ربات)\n\nروی نام ربات بزنید:",
        reply_markup=kb
    )


def handle_bot_info(query: dict, bot_id: int):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        bot = conn.execute(
            "SELECT * FROM deployed_bots WHERE id=? AND user_id=?",
            (bot_id, user_id)
        ).fetchone()

    if not bot:
        answer_callback(query["id"], "ربات یافت نشد!", True)
        return

    status_map = {
        "running": "🟢 در حال اجرا",
        "stopped": "🔴 متوقف",
        "pending": "🟡 در انتظار تایید",
        "rejected": "❌ رد شده"
    }
    status = status_map.get(bot["status"], bot["status"])

    edit_message(
        chat_id, msg_id,
        f"🤖 *{bot['bot_name']}*\n\n"
        f"وضعیت: {status}\n"
        f"مستقر شده: {bot['deployed_at'] or 'هنوز نه'}\n"
        f"فایل: `{Path(bot['file_path']).name if bot['file_path'] else 'ندارد'}`",
        reply_markup=inline_keyboard([
            [("🗑 حذف ربات", f"delete_bot_confirm:{bot_id}")],
            [("📋 مشاهده لاگ", f"view_log:{bot_id}"), ("⏹ توقف", f"stop_bot:{bot_id}")],
            [("▶️ راه‌اندازی مجدد", f"restart_bot:{bot_id}")],
            [("🔙 لیست ربات‌ها", "bots_menu")]
        ])
    )


def handle_delete_bot_confirm(query: dict, bot_id: int):
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        bot = conn.execute("SELECT bot_name FROM deployed_bots WHERE id=?", (bot_id,)).fetchone()
    name = bot["bot_name"] if bot else "ربات"

    edit_message(
        chat_id, msg_id,
        f"⚠️ *آیا مطمئن هستید؟*\n\nمی‌خواهید ربات *{name}* را حذف کنید؟\nاین عمل برگشت‌پذیر نیست!",
        reply_markup=inline_keyboard([
            [("✅ بله، حذف شود", f"delete_bot_final:{bot_id}")],
            [("❌ خیر، انصراف", f"bot_info:{bot_id}")]
        ])
    )


def handle_delete_bot_final(query: dict, bot_id: int):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        bot = conn.execute(
            "SELECT * FROM deployed_bots WHERE id=? AND user_id=?",
            (bot_id, user_id)
        ).fetchone()

    if not bot:
        answer_callback(query["id"], "ربات یافت نشد!", True)
        return

    # توقف پروسه
    if bot["pid"]:
        try:
            os.kill(bot["pid"], 9)
        except:
            pass

    # حذف فایل‌ها
    if bot["file_path"] and os.path.exists(bot["file_path"]):
        try:
            os.remove(bot["file_path"])
        except:
            pass

    with get_db() as conn:
        conn.execute("DELETE FROM deployed_bots WHERE id=?", (bot_id,))
        conn.commit()

    edit_message(
        chat_id, msg_id,
        f"✅ ربات *{bot['bot_name']}* با موفقیت حذف شد.",
        reply_markup=inline_keyboard([[("🔙 لیست ربات‌ها", "bots_menu")]])
    )


# ─────────────────────────────────────────────
#  استقرار ربات جدید
# ─────────────────────────────────────────────
def handle_deploy_new(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    ok, reason = check_plan_limit(user_id, "bots")
    if not ok:
        edit_message(
            chat_id, msg_id,
            f"❌ *محدودیت پلن*\n\n{reason}\n\nبرای افزایش سقف، آیتم «ربات اضافه» بخرید یا پلن ارتقا دهید.",
            reply_markup=inline_keyboard([
                [("🏪 فروشگاه آیتم", "shop_menu"), ("💳 ارتقای پلن", "sub_menu")],
                [("🔙 بازگشت", "main_menu")]
            ])
        )
        return

    set_state(user_id, "deploy_waiting_name")
    edit_message(
        chat_id, msg_id,
        "🚀 *استقرار ربات جدید*\n\n*مرحله ۱/۳:* نام ربات خود را ارسال کنید.\n\n"
        "مثال: `MyAwesomeBot`",
        reply_markup=inline_keyboard([[("❌ انصراف", "main_menu")]])
    )


def handle_deploy_name(message: dict):
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    bot_name = message.get("text", "").strip()

    if not bot_name or len(bot_name) < 2:
        send_message(chat_id, "❌ نام ربات معتبر نیست. دوباره وارد کنید:")
        return

    set_state(user_id, "deploy_waiting_file", {"bot_name": bot_name})
    send_message(
        chat_id,
        f"✅ نام ربات: *{bot_name}*\n\n"
        f"*مرحله ۲/۳:* حالا فایل پایتون ربات (`.py`) را ارسال کنید.\n\n"
        f"می‌توانید کنار فایل پایتون، فایل‌های دیگر نیز ارسال کنید.",
        reply_markup=inline_keyboard([[("❌ انصراف", "main_menu")]])
    )


def handle_deploy_file(message: dict):
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    state = get_state(user_id)

    document = message.get("document")
    if not document:
        send_message(chat_id, "❌ لطفاً یک فایل ارسال کنید.")
        return

    file_name = document.get("file_name", "")
    bot_name = state["data"].get("bot_name", "unknown_bot")

    # دانلود فایل
    file_id = document["file_id"]
    file_info = api("getFile", {"file_id": file_id})
    if not file_info.get("ok"):
        send_message(chat_id, "❌ خطا در دریافت فایل.")
        return

    file_path_remote = file_info["result"]["file_path"]
    download_url = f"https://tapi.bale.ai/file/bot{TOKEN}/{file_path_remote}"
    r = requests.get(download_url)

    # ذخیره فایل
    bot_dir = BOTS_DIR / f"{user_id}_{bot_name}"
    bot_dir.mkdir(exist_ok=True)

    local_path = bot_dir / file_name
    with open(local_path, "wb") as f:
        f.write(r.content)

    if file_name.endswith(".py"):
        # بررسی تعداد خطوط کد
        try:
            with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            lines = []

        u = get_user(user_id)
        plan = PLANS.get(u["plan"] if u else "free", PLANS["free"])
        max_lines = plan["max_code_lines"]
        if max_lines != -1 and len(lines) > max_lines:
            send_message(
                chat_id,
                f"❌ فایل شما *{len(lines)} خط* دارد.\n"
                f"محدودیت پلن شما: *{max_lines} خط*\n\n"
                f"برای پلن بالاتر یا خط کد اضافی اقدام کنید."
            )
            shutil.rmtree(bot_dir)
            return

        set_state(user_id, "deploy_confirm", {
            "bot_name": bot_name,
            "file_path": str(local_path),
            "extra_files": [],
            "bot_dir": str(bot_dir)
        })

        send_message(
            chat_id,
            f"✅ فایل دریافت شد!\n\n"
            f"*مرحله ۳/۳:* آیا می‌خواهید فایل‌های دیگری اضافه کنید؟\n"
            f"(مثلاً فایل config، requirements.txt و ...)\n\n"
            f"اگر نه، روی «ارسال درخواست» بزنید:",
            reply_markup=inline_keyboard([
                [("📤 ارسال درخواست به مدیر", "deploy_submit")],
                [("❌ انصراف", "main_menu")]
            ])
        )
    else:
        # فایل اضافی
        current_state = get_state(user_id)
        extra_files = current_state["data"].get("extra_files", [])
        extra_files.append(str(local_path))
        set_state(user_id, current_state["state"], {
            **current_state["data"],
            "extra_files": extra_files
        })
        send_message(
            chat_id,
            f"✅ فایل *{file_name}* اضافه شد.\nمی‌توانید فایل بیشتری ارسال کنید یا درخواست را ثبت کنید:",
            reply_markup=inline_keyboard([
                [("📤 ارسال درخواست به مدیر", "deploy_submit")],
                [("❌ انصراف", "main_menu")]
            ])
        )


def handle_deploy_submit(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    state = get_state(user_id)

    if state["state"] not in ("deploy_confirm", "deploy_waiting_file"):
        answer_callback(query["id"], "وضعیت نامعتبر!", True)
        return

    data = state["data"]
    bot_name = data.get("bot_name", "نامشخص")
    file_path = data.get("file_path", "")

    if not file_path:
        answer_callback(query["id"], "ابتدا فایل پایتون ارسال کنید!", True)
        return

    tracking_code = "DEP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO deployed_bots (user_id, bot_name, file_path, extra_files, status) VALUES (?,?,?,?,?)",
            (user_id, bot_name, file_path, json.dumps(data.get("extra_files", [])), "pending")
        )
        bot_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()

        # ذخیره درخواست
        conn.execute(
            "INSERT INTO pending_requests (type, user_id, data, created_at) VALUES (?,?,?,?)",
            ("deploy", user_id, json.dumps({"bot_id": bot_id, "bot_name": bot_name, "tracking": tracking_code}), datetime.now().isoformat())
        )
        req_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()

    # ارسال به مدیران
    u = get_user(user_id)
    for admin_id in ADMIN_IDS:
        res = send_message(
            admin_id,
            f"📬 *درخواست استقرار ربات جدید*\n\n"
            f"👤 کاربر: {u['full_name'] if u else user_id} (`{user_id}`)\n"
            f"🤖 نام ربات: *{bot_name}*\n"
            f"🔖 کد پیگیری: `{tracking_code}`\n"
            f"📁 فایل: `{Path(file_path).name}`",
            reply_markup=inline_keyboard([
                [("✅ تایید", f"admin_approve_deploy:{req_id}"), ("❌ رد", f"admin_reject_deploy:{req_id}")]
            ])
        )
        if res.get("ok"):
            with get_db() as conn:
                conn.execute(
                    "UPDATE pending_requests SET admin_msg_id=? WHERE id=?",
                    (res["result"]["message_id"], req_id)
                )
                conn.commit()

    clear_state(user_id)
    edit_message(
        chat_id, msg_id,
        f"✅ *درخواست استقرار ثبت شد!*\n\n"
        f"🔖 کد پیگیری: `{tracking_code}`\n\n"
        f"پس از تایید مدیر، ربات شما مستقر خواهد شد.",
        reply_markup=inline_keyboard([[("🔙 منوی اصلی", "main_menu")]])
    )


# ─────────────────────────────────────────────
#  تایید/رد استقرار توسط مدیر
# ─────────────────────────────────────────────
def handle_admin_approve_deploy(query: dict, req_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        answer_callback(query["id"], "دسترسی ندارید!", True)
        return

    with get_db() as conn:
        req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()

    if not req or req["status"] != "pending":
        answer_callback(query["id"], "این درخواست قبلاً پردازش شده!", True)
        return

    req_data = json.loads(req["data"])
    bot_id = req_data["bot_id"]
    user_id = req["user_id"]

    # آپدیت وضعیت
    with get_db() as conn:
        conn.execute(
            "UPDATE deployed_bots SET status='running', approved_by=?, deployed_at=? WHERE id=?",
            (admin_id, datetime.now().isoformat(), bot_id)
        )
        conn.execute(
            "UPDATE pending_requests SET status='approved' WHERE id=?",
            (req_id,)
        )
        conn.commit()

        bot = conn.execute("SELECT * FROM deployed_bots WHERE id=?", (bot_id,)).fetchone()

    # راه‌اندازی ربات
    log_file = start_bot_process(bot_id, bot["file_path"], bot["bot_name"], user_id)

    edit_message(
        chat_id, msg_id,
        f"✅ ربات *{bot['bot_name']}* تایید و اجرا شد.",
        reply_markup=inline_keyboard([[("✅ تایید شد", "noop")]])
    )

    # اطلاع به کاربر
    send_message(
        user_id,
        f"🎉 *ربات شما تایید شد!*\n\n"
        f"🤖 نام: *{bot['bot_name']}*\n"
        f"✅ وضعیت: در حال اجرا\n\n"
        f"اولین لاگ‌ها به زودی ارسال می‌شوند.",
        reply_markup=inline_keyboard([[("📋 مشاهده لاگ", f"view_log:{bot_id}")]])
    )

    # ارسال لاگ اولیه
    if log_file:
        threading.Thread(target=stream_logs, args=(bot_id, user_id, bot["bot_name"]), daemon=True).start()


def handle_admin_reject_deploy(query: dict, req_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        answer_callback(query["id"], "دسترسی ندارید!", True)
        return

    with get_db() as conn:
        req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()

    if not req or req["status"] != "pending":
        answer_callback(query["id"], "این درخواست قبلاً پردازش شده!", True)
        return

    set_state(admin_id, "reject_deploy_reason", {
        "req_id": req_id,
        "msg_id": msg_id,
        "chat_id": chat_id,
        "user_id": req["user_id"]
    })
    send_message(admin_id, "❓ دلیل رد درخواست را وارد کنید:")


def handle_admin_reject_lib(query: dict, req_id: int):
    """FIX: تابع رد کتابخانه که قبلاً تعریف نشده بود"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        answer_callback(query["id"], "دسترسی ندارید!", True)
        return

    with get_db() as conn:
        req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()

    if not req or req["status"] != "pending":
        answer_callback(query["id"], "این درخواست قبلاً پردازش شده!", True)
        return

    set_state(admin_id, "reject_lib_reason", {
        "req_id": req_id,
        "msg_id": msg_id,
        "chat_id": chat_id,
        "user_id": req["user_id"]
    })
    send_message(admin_id, "❓ دلیل رد درخواست کتابخانه را وارد کنید:")


# ─────────────────────────────────────────────
#  اجرا و مدیریت پروسه ربات‌ها
# ─────────────────────────────────────────────
bot_processes: Dict[int, subprocess.Popen] = {}
bot_log_msgs: Dict[int, dict] = {}  # {bot_id: {user_id, msg_id, log_lines}}


def generate_html_log(bot_name: str, log_lines: list) -> str:
    lines_html = ""
    for line in log_lines:
        ts = line.get("ts", "")
        msg = line.get("msg", "").replace("<", "&lt;").replace(">", "&gt;")
        level = line.get("level", "INFO")
        color = {
            "INFO": "#00ff88",
            "ERROR": "#ff4444",
            "WARNING": "#ffbb00",
            "SUCCESS": "#00ccff"
        }.get(level, "#ffffff")
        lines_html += f'<tr><td class="ts">{ts}</td><td class="level" style="color:{color}">{level}</td><td class="msg">{msg}</td></tr>\n'

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>لاگ ربات {bot_name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; }}
  .header {{ background: linear-gradient(135deg, #1f6feb, #388bfd); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center; }}
  .header h1 {{ font-size: 24px; color: white; }}
  .header p {{ color: rgba(255,255,255,0.8); font-size: 14px; margin-top: 5px; }}
  .stats {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
  .stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 20px; flex: 1; min-width: 120px; text-align: center; }}
  .stat-card .num {{ font-size: 24px; font-weight: bold; color: #58a6ff; }}
  .stat-card .label {{ font-size: 12px; color: #8b949e; }}
  table {{ width: 100%; border-collapse: collapse; background: #161b22; border-radius: 12px; overflow: hidden; }}
  thead {{ background: #21262d; }}
  th {{ padding: 12px 16px; text-align: right; color: #8b949e; font-size: 13px; border-bottom: 1px solid #30363d; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid #21262d; font-size: 13px; }}
  .ts {{ color: #8b949e; white-space: nowrap; }}
  .level {{ font-weight: bold; }}
  .msg {{ word-break: break-all; }}
  tr:hover {{ background: #1c2128; }}
  .footer {{ text-align: center; margin-top: 20px; color: #8b949e; font-size: 12px; }}
</style>
</head>
<body>
<div class="header">
  <h1>🤖 {bot_name}</h1>
  <p>آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
<div class="stats">
  <div class="stat-card"><div class="num">{len(log_lines)}</div><div class="label">تعداد لاگ</div></div>
  <div class="stat-card"><div class="num">{sum(1 for l in log_lines if l.get('level')=='ERROR')}</div><div class="label">خطا</div></div>
  <div class="stat-card"><div class="num">{sum(1 for l in log_lines if l.get('level')=='WARNING')}</div><div class="label">هشدار</div></div>
</div>
<table>
<thead><tr><th>زمان</th><th>سطح</th><th>پیام</th></tr></thead>
<tbody>
{lines_html}
</tbody>
</table>
<div class="footer">Poro Bot Logger &copy; {datetime.now().year}</div>
</body>
</html>"""


def start_bot_process(bot_id: int, file_path: str, bot_name: str, user_id: int) -> Optional[str]:
    try:
        log_file = LOGS_DIR / f"bot_{bot_id}.log"
        lf = open(log_file, "w")
        proc = subprocess.Popen(
            [sys.executable, file_path],
            stdout=lf,
            stderr=lf,
            cwd=str(Path(file_path).parent)
        )
        bot_processes[bot_id] = proc
        with get_db() as conn:
            conn.execute(
                "UPDATE deployed_bots SET pid=?, log_file=? WHERE id=?",
                (proc.pid, str(log_file), bot_id)
            )
            conn.commit()
        return str(log_file)
    except Exception as e:
        log.error(f"خطا در راه‌اندازی ربات {bot_id}: {e}")
        return None

def stream_logs(bot_id: int, user_id: int, bot_name: str):
        """ارسال لاگ به صورت live برای مدت یک دقیقه"""
        time.sleep(2)
        log_file = LOGS_DIR / f"bot_{bot_id}.log"
        log_lines = [{"ts": datetime.now().strftime("%H:%M:%S"), "msg": f"ربات {bot_name} با موفقیت اجرا شد ✅", "level": "SUCCESS"}]

        html_content = generate_html_log(bot_name, log_lines)
        html_path = LOGS_DIR / f"bot_{bot_id}_log.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        res = send_document(user_id, html_path, f"📋 لاگ زنده ربات *{bot_name}*")
        if not res.get("ok"):
            return

        msg_id = res["result"]["message_id"]
        bot_log_msgs[bot_id] = {"user_id": user_id, "msg_id": msg_id, "log_lines": log_lines, "html_path": str(html_path)}

        last_pos = 0
        update_interval = 5
        last_update = time.time()
        start_time = time.time() # زمان شروع لاگ‌گیری را ثبت می‌کنیم
        duration = 60 # مدت زمان به ثانیه (یک دقیقه)

        while time.time() - start_time < duration: # حلقه تا زمانی که از یک دقیقه بیشتر نشده است
            time.sleep(2)
            try:
                if not log_file.exists():
                    break
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(last_pos)
                    new_content = f.read()
                    last_pos = f.tell()

                if new_content.strip():
                    for line in new_content.strip().split("\n"):
                        if line.strip():
                            level = "INFO"
                            if "error" in line.lower():
                                level = "ERROR"
                            elif "warn" in line.lower():
                                level = "WARNING"
                            log_lines.append({
                                "ts": datetime.now().strftime("%H:%M:%S"),
                                "msg": line.strip(),
                                "level": level
                            })

                if time.time() - last_update >= update_interval:
                    # برای جلوگیری از ارسال مداوم فایل در زمان کوتاه، فقط آخرین 200 لاگ را نمایش می‌دهیم
                    html_content = generate_html_log(bot_name, log_lines[-200:])
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    # ارسال مجدد سند با همان شناسه پیام قبلی برای آپدیت
                    # اگر API تلگرام اجازه آپدیت سند را بدهد، بهتر است از editMessageMedia استفاده شود
                    # اما در اینجا فرض می‌کنیم با ارسال مجدد، کاربر پیام جدید را دریافت می‌کند
                    send_document(user_id, html_path, f"📋 لاگ زنده ربات *{bot_name}* (آپدیت شد)")
                    last_update = time.time()
            except Exception as e:
                # در صورت بروز خطا، لاگ می‌کنیم و به حلقه ادامه می‌دهیم
                print(f"خطا در حلقه لاگ‌گیری: {e}") # برای دیباگ، در نسخه نهایی شاید نیاز نباشد
                pass
        
        # پس از اتمام زمان یک دقیقه، یک پیام نهایی ارسال می‌کنیم
        final_message = f"⏱️ اتمام زمان ارسال لاگ زنده (۱ دقیقه) برای ربات *{bot_name}*."
        send_message(user_id, final_message) # فرض می‌کنیم تابع send_message وجود دارد


# ─────────────────────────────────────────────
#  نصب کتابخانه
# ─────────────────────────────────────────────
def handle_install_lib(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    ok, reason = check_plan_limit(user_id, "libraries")
    if not ok:
        edit_message(
            chat_id, msg_id,
            f"❌ *محدودیت پلن*\n\n{reason}",
            reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]])
        )
        return

    u = get_user(user_id)
    plan = PLANS.get(u["plan"] if u else "free", PLANS["free"])
    mirror_allowed = plan["personal_mirror"]

    set_state(user_id, "install_lib_name")
    buttons = [[("❌ انصراف", "main_menu")]]
    if mirror_allowed:
        buttons.insert(0, [("🌐 استفاده از میرور", "set_mirror")])

    edit_message(
        chat_id, msg_id,
        "📦 *نصب کتابخانه جدید*\n\nنام کتابخانه را ارسال کنید:\n\n"
        "مثال: `requests`, `numpy`, `flask`",
        reply_markup=inline_keyboard(buttons)
    )


def handle_install_lib_name(message: dict):
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    state = get_state(user_id)
    lib_name = message.get("text", "").strip()

    if not lib_name:
        send_message(chat_id, "❌ نام کتابخانه معتبر نیست.")
        return

    mirror = state["data"].get("mirror", None)
    tracking_code = "LIB-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO library_installs (user_id, library_name, mirror_url, status, tracking_code) VALUES (?,?,?,?,?)",
            (user_id, lib_name, mirror, "pending", tracking_code)
        )
        install_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO pending_requests (type, user_id, data, created_at) VALUES (?,?,?,?)",
            ("install_lib", user_id, json.dumps({"install_id": install_id, "lib_name": lib_name, "tracking": tracking_code, "mirror": mirror}), datetime.now().isoformat())
        )
        req_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()

    u = get_user(user_id)
    for admin_id in ADMIN_IDS:
        send_message(
            admin_id,
            f"📦 *درخواست نصب کتابخانه*\n\n"
            f"👤 کاربر: {u['full_name'] if u else user_id} (`{user_id}`)\n"
            f"📦 کتابخانه: `{lib_name}`\n"
            f"🌐 میرور: {mirror or 'پیش‌فرض (PyPI)'}\n"
            f"🔖 کد پیگیری: `{tracking_code}`",
            reply_markup=inline_keyboard([
                [("✅ تایید و نصب", f"admin_approve_lib:{req_id}"), ("❌ رد", f"admin_reject_lib:{req_id}")]
            ])
        )

    clear_state(user_id)
    send_message(
        chat_id,
        f"✅ *درخواست نصب ثبت شد!*\n\n"
        f"📦 کتابخانه: `{lib_name}`\n"
        f"🔖 کد پیگیری: `{tracking_code}`\n\n"
        f"پس از تایید مدیر نصب انجام می‌شود.",
        reply_markup=inline_keyboard([[("🔙 منوی اصلی", "main_menu")]])
    )


def handle_admin_approve_lib(query: dict, req_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        answer_callback(query["id"], "دسترسی ندارید!", True)
        return

    with get_db() as conn:
        req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()

    if not req or req["status"] != "pending":
        answer_callback(query["id"], "قبلاً پردازش شده!", True)
        return

    req_data = json.loads(req["data"])
    install_id = req_data["install_id"]
    lib_name = req_data["lib_name"]
    mirror = req_data.get("mirror")
    user_id = req["user_id"]

    edit_message(
        chat_id, msg_id,
        f"⏳ در حال نصب `{lib_name}`...",
    )

    def do_install():
        cmd = [sys.executable, "-m", "pip", "install", lib_name]
        if mirror:
            cmd.extend(["-i", mirror])
        cmd.append("--break-system-packages")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            result = type('obj', (object,), {'returncode': 1, 'stdout': '', 'stderr': 'نصب بیش از حد طول کشید.'})()

        success = result.returncode == 0
        output = (result.stdout + result.stderr)[-1500:]

        status = "installed" if success else "failed"
        with get_db() as conn:
            conn.execute(
                "UPDATE library_installs SET status=?, approved_by=?, installed_at=? WHERE id=?",
                (status, admin_id, datetime.now().isoformat(), install_id)
            )
            conn.execute("UPDATE pending_requests SET status=? WHERE id=?", (status, req_id))
            conn.commit()

        if success:
            edit_message(
                chat_id, msg_id,
                f"✅ کتابخانه `{lib_name}` با موفقیت نصب شد!\n\n"
                f"```\n{output[:500]}\n```"
            )
            send_message(
                user_id,
                f"✅ *کتابخانه نصب شد!*\n\n`{lib_name}` با موفقیت نصب شد."
            )
        else:
            edit_message(
                chat_id, msg_id,
                f"❌ خطا در نصب `{lib_name}`:\n\n```\n{output[:500]}\n```"
            )
            send_message(
                user_id,
                f"❌ نصب `{lib_name}` با خطا مواجه شد.\nدلیل: ```{output[:300]}```"
            )

    threading.Thread(target=do_install, daemon=True).start()


# ─────────────────────────────────────────────
#  فروشگاه آیتم
# ─────────────────────────────────────────────
def handle_shop_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    u = get_user(user_id)
    points = u["points"] if u else 0
    plan = u["plan"] if u else "free"

    text = f"🏪 *فروشگاه آیتم*\n\n💰 امتیاز شما: *{points}*\n\n"
    buttons = []
    for key, item in SHOP_ITEMS.items():
        cost = item["points"].get(plan)
        if cost is None:
            continue
        btn_text = f"{item['name']} - {cost} امتیاز"
        buttons.append([(btn_text, f"buy_item:{key}")])

    buttons.append([("🔙 بازگشت", "main_menu")])
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_buy_item(query: dict, item_key: str):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    u = get_user(user_id)
    plan = u["plan"] if u else "free"
    item = SHOP_ITEMS.get(item_key)

    if not item:
        answer_callback(query["id"], "آیتم یافت نشد!", True)
        return

    cost = item["points"].get(plan)
    if cost is None:
        answer_callback(query["id"], "در پلن شما این آیتم موجود نیست!", True)
        return

    if not u or u["points"] < cost:
        edit_message(
            chat_id, msg_id,
            f"❌ امتیاز کافی ندارید!\n\nنیاز: *{cost}*\nموجودی: *{u['points'] if u else 0}*",
            reply_markup=inline_keyboard([[("🔙 فروشگاه", "shop_menu")]])
        )
        return

    if not spend_points(user_id, cost):
        answer_callback(query["id"], "خطا در کسر امتیاز!", True)
        return

    # اعمال آیتم
    field_map = {
        "extra_bot": "extra_bots",
        "extra_memory": "extra_memory_mb",
        "extra_log": "extra_log_days",
        "extra_library": "extra_libraries",
        "extra_bandwidth": "extra_bandwidth_gb"
    }
    amount_map = {
        "extra_bot": 1,
        "extra_memory": 100,
        "extra_log": 7,
        "extra_library": 1,
        "extra_bandwidth": 1
    }
    db_field = field_map.get(item_key)
    amount = amount_map.get(item_key, 1)

    if db_field:
        with get_db() as conn:
            conn.execute(f"UPDATE users SET {db_field} = {db_field} + ? WHERE user_id=?", (amount, user_id))
            conn.commit()

    edit_message(
        chat_id, msg_id,
        f"✅ *آیتم خریداری شد!*\n\n{item['name']} به حساب شما اضافه شد.\n💰 امتیاز باقی‌مانده: *{get_points(user_id)}*",
        reply_markup=inline_keyboard([[("🔙 فروشگاه", "shop_menu")]])
    )


# ─────────────────────────────────────────────
#  سیستم اشتراک و پرداخت
# ─────────────────────────────────────────────
def handle_sub_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    u = get_user(user_id)
    current_plan = u["plan"] if u else "free"

    text = f"💳 *خرید اشتراک*\n\nپلن فعلی: *{PLANS[current_plan]['name']}*\n\nپلن مورد نظر را انتخاب کنید:"
    buttons = []
    for plan_key, plan_data in PLANS.items():
        if plan_key == "free":
            continue
        if plan_key == "enterprise":
            buttons.append([(f"{plan_data['name']} - مذاکره‌ای", f"view_plan:{plan_key}")])
        else:
            min_price = min(v["price"] for v in plan_data["subscriptions"].values())
            buttons.append([(f"{plan_data['name']} - از {min_price:,} تومان", f"view_plan:{plan_key}")])

    buttons.append([("🔙 بازگشت", "main_menu")])
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_view_plan(query: dict, plan_key: str):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    plan = PLANS.get(plan_key)
    if not plan:
        answer_callback(query["id"], "پلن یافت نشد!", True)
        return

    text = f"*{plan['name']}*\n\n"
    text += f"🤖 حداکثر ربات: {'نامحدود' if plan['max_bots']==-1 else plan['max_bots']}\n"
    text += f"💾 حافظه: {plan['max_memory_mb']} MB\n"
    text += f"📋 نگهداری لاگ: {plan['log_retention_days']} روز\n"
    text += f"📦 کتابخانه: {'نامحدود' if plan['max_libraries']==-1 else plan['max_libraries']}\n"
    text += f"🌐 پهنای باند: {plan['monthly_bandwidth_gb']} GB/ماه\n\n"
    text += "💰 *قیمت‌ها:*\n"

    buttons = []
    for dur, sub in plan["subscriptions"].items():
        dur_fa = {"monthly": "یک ماهه", "quarterly": "سه ماهه", "biannual": "شش ماهه", "annual": "یک ساله"}
        price = sub["price"]
        if price == -1:
            text += f"• {dur_fa.get(dur, dur)}: مذاکره‌ای\n"
        else:
            fake_price = int(price * 1.05)
            text += f"• {dur_fa.get(dur, dur)}: ~~{fake_price:,}~~ *{price:,}* تومان 🏷\n"
            buttons.append([(f"خرید {dur_fa.get(dur, dur)} - {price:,}T", f"checkout:{plan_key}:{dur}")])

    if plan_key == "enterprise":
        buttons.append([("📞 تماس با مدیر", f"enterprise_request")])

    buttons.append([("🔙 بازگشت", "sub_menu")])
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_checkout(query: dict, plan_key: str, duration: str):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    plan = PLANS.get(plan_key)
    if not plan:
        answer_callback(query["id"], "پلن یافت نشد!", True)
        return

    sub = plan["subscriptions"].get(duration)
    if not sub or sub["price"] <= 0:
        answer_callback(query["id"], "قیمت نامعتبر!", True)
        return

    dur_fa = {"monthly": "یک ماهه", "quarterly": "سه ماهه", "biannual": "شش ماهه", "annual": "یک ساله"}
    price = sub["price"]

    set_state(user_id, "awaiting_discount", {"plan": plan_key, "duration": duration, "price": price})

    edit_message(
        chat_id, msg_id,
        f"💳 *خرید اشتراک*\n\n"
        f"پلن: *{plan['name']}*\n"
        f"مدت: *{dur_fa.get(duration, duration)}*\n"
        f"قیمت: *{price:,} تومان*\n\n"
        f"آیا کد تخفیف دارید؟",
        reply_markup=inline_keyboard([
            [("🎟 وارد کردن کد تخفیف", f"enter_discount:{plan_key}:{duration}")],
            [("💰 پرداخت بدون تخفیف", f"pay_now:{plan_key}:{duration}:0")],
            [("🔙 بازگشت", f"view_plan:{plan_key}")]
        ])
    )


def handle_pay_now(query: dict, plan_key: str, duration: str, discount: int):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]

    plan = PLANS.get(plan_key)
    if not plan:
        return

    sub = plan["subscriptions"].get(duration)
    if not sub:
        return

    original_price = sub["price"]
    final_price = max(0, original_price - int(discount))
    dur_fa = {"monthly": "یک ماهه", "quarterly": "سه ماهه", "biannual": "شش ماهه", "annual": "یک ساله"}

    payload = f"sub_{plan_key}_{duration}_{user_id}_{int(time.time())}"

    send_invoice(
        chat_id,
        title=f"اشتراک {plan['name']}",
        description=f"خرید اشتراک {dur_fa.get(duration, duration)} - {plan['name']}",
        payload=payload,
        prices=[{"label": f"اشتراک {plan['name']}", "amount": final_price * 10}]
    )


def handle_pre_checkout(update: dict):
    query = update.get("pre_checkout_query", {})
    api("answerPreCheckoutQuery", {
        "pre_checkout_query_id": query["id"],
        "ok": True
    })


def handle_successful_payment(message: dict):
    user_id = message["from"]["id"]
    payment = message["successful_payment"]
    payload = payment["invoice_payload"]
    amount = payment["total_amount"] // 10

    parts = payload.split("_")
    if len(parts) >= 3 and parts[0] == "sub":
        plan_key = parts[1]
        duration = parts[2]

        dur_days = {"monthly": 30, "quarterly": 90, "biannual": 180, "annual": 365}
        days = dur_days.get(duration, 30)
        expires_at = (datetime.now() + timedelta(days=days)).isoformat()

        with get_db() as conn:
            u = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

            # بررسی خرید اجباری پلن بالاتر
            if plan_key == "basic":
                basic_count = ((u["basic_buy_count"] or 0) if u else 0) + 1
                conn.execute(
                    "UPDATE users SET plan=?, plan_expires_at=?, total_spent=total_spent+?, basic_buy_count=? WHERE user_id=?",
                    (plan_key, expires_at, amount, basic_count, user_id)
                )
                if basic_count >= 3:
                    send_message(
                        user_id,
                        "⚠️ *توجه:* شما ۳ بار اشتراک پایه خریداری کرده‌اید.\n"
                        "از این به بعد برای خرید اشتراک پایه، ابتدا باید یک بار اشتراک حرفه‌ای تهیه کنید."
                    )
            else:
                conn.execute(
                    "UPDATE users SET plan=?, plan_expires_at=?, total_spent=total_spent+? WHERE user_id=?",
                    (plan_key, expires_at, amount, user_id)
                )

            conn.execute(
                "INSERT INTO payments (user_id, plan, duration, amount, status, transaction_id, provider_id, payload, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                (user_id, plan_key, duration, amount, "paid",
                 payment.get("telegram_payment_charge_id", ""),
                 payment.get("provider_payment_charge_id", ""),
                 payload, datetime.now().isoformat())
            )
            conn.commit()

        # اضافه کردن امتیاز هدیه
        gift_points = PLANS.get(plan_key, {}).get("subscriptions", {}).get(duration, {}).get("gift_points", 0)
        if gift_points:
            add_points(user_id, gift_points, "هدیه خرید اشتراک")

        # امتیاز بر اساس خرید
        buy_points = amount // 1000
        if buy_points:
            add_points(user_id, buy_points, "امتیاز خرید")

        send_message(
            user_id,
            f"🎉 *پرداخت موفق!*\n\n"
            f"✅ اشتراک {PLANS[plan_key]['name']} فعال شد!\n"
            f"💰 مبلغ: {amount:,} تومان\n"
            f"📅 انقضا: {expires_at[:10]}\n"
            f"🎁 امتیاز هدیه: {gift_points} امتیاز",
            reply_markup=main_menu(user_id)
        )


# ─────────────────────────────────────────────
#  سیستم تخفیف
# ─────────────────────────────────────────────
def validate_discount_code(code: str, user_id: int, plan_key: str) -> tuple:
    """بررسی کد تخفیف، برگرداندن (valid, amount_off, dc_obj_or_reason)"""
    with get_db() as conn:
        dc = conn.execute("SELECT * FROM discount_codes WHERE code=?", (code,)).fetchone()

    if not dc:
        return False, 0, "کد تخفیف معتبر نیست"
    if not dc["is_active"]:
        return False, 0, "این کد تخفیف غیرفعال است"
    if dc["used_count"] >= dc["max_uses"]:
        return False, 0, "این کد تخفیف تمام شده"
    if dc["expires_at"] and datetime.now().isoformat() > dc["expires_at"]:
        return False, 0, "این کد تخفیف منقضی شده"
    if dc["plan_target"] and dc["plan_target"] != plan_key:
        return False, 0, "این کد برای پلن شما قابل استفاده نیست"

    # بررسی استفاده قبلی
    with get_db() as conn:
        used = conn.execute(
            "SELECT id FROM discount_uses WHERE code_id=? AND user_id=?",
            (dc["id"], user_id)
        ).fetchone()

    if used:
        return False, 0, "شما قبلاً از این کد استفاده کرده‌اید"

    # بررسی حداکثر کد همزمان
    u = get_user(user_id)
    plan = PLANS.get(u["plan"] if u else "free", PLANS["free"])
    max_codes = plan["max_discount_codes"]
    if max_codes == 0:
        return False, 0, "پلن شما امکان استفاده از کد تخفیف ندارد"

    return True, dc["value"], dict(dc)


def apply_discount_code(code_id: int, user_id: int):
    with get_db() as conn:
        conn.execute("UPDATE discount_codes SET used_count=used_count+1 WHERE id=?", (code_id,))
        conn.execute(
            "INSERT INTO discount_uses (code_id, user_id, used_at) VALUES (?,?,?)",
            (code_id, user_id, datetime.now().isoformat())
        )
        conn.commit()


# ─────────────────────────────────────────────
#  پنل مدیریت
# ─────────────────────────────────────────────
def handle_admin_panel(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        answer_callback(query["id"], "دسترسی ندارید!", True)
        return

    edit_message(
        chat_id, msg_id,
        "⚙️ *پنل مدیریت*\n\nانتخاب کنید:",
        reply_markup=inline_keyboard([
            [("📢 پیام همگانی", "broadcast_msg"), ("📊 آمار لحظه‌ای", "realtime_stats")],
            [("📈 آمار هفتگی", "weekly_stats"), ("✅ درخواست‌ها", "pending_requests")],
            [("💰 درآمد", "revenue_panel"), ("👥 مدیریت کاربران", "user_management")],
            [("🎟 کدهای تخفیف", "discount_panel"), ("💳 مدیریت اشتراک", "subscription_mgmt")],
            [("💳 توکن پرداخت", "payment_token_panel"), ("🎪 قرعه‌کشی", "lottery_admin")],
            [("🏆 چالش‌های کد", "challenge_admin"), ("🎫 تیکت‌ها", "tickets_admin")],
            [("⚙️ تنظیمات", "admin_settings"), ("🔙 بازگشت", "main_menu")]
        ])
    )


def handle_broadcast_msg(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        return

    set_state(user_id, "broadcast_waiting_msg")
    edit_message(
        chat_id, msg_id,
        "📢 *پیام همگانی*\n\nپیام یا محتوای مورد نظر را ارسال کنید:\n(متن، فایل، عکس، و غیره)",
        reply_markup=inline_keyboard([[("❌ انصراف", "admin_panel")]])
    )


def handle_broadcast_content(message: dict):
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]

    if not is_admin(user_id):
        return

    text = message.get("text", "")
    ok, fail = 0, 0

    with get_db() as conn:
        users = conn.execute("SELECT user_id FROM users").fetchall()

    for u in users:
        try:
            if text:
                res = send_message(u["user_id"], text)
            elif "document" in message:
                file_id = message["document"]["file_id"]
                res = api("sendDocument", {"chat_id": u["user_id"], "document": file_id})
            elif "photo" in message:
                file_id = message["photo"][-1]["file_id"]
                res = api("sendPhoto", {"chat_id": u["user_id"], "photo": file_id})
            else:
                continue
            if res.get("ok"):
                ok += 1
            else:
                fail += 1
        except:
            fail += 1
        time.sleep(0.05)

    clear_state(user_id)
    send_message(
        chat_id,
        f"✅ *پیام همگانی ارسال شد!*\n\n✅ موفق: {ok}\n❌ ناموفق: {fail}",
        reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]])
    )


def handle_realtime_stats(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        return

    with get_db() as conn:
        total_users = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        active_users = conn.execute("SELECT COUNT(*) as c FROM users WHERE is_active=1").fetchone()["c"]
        blocked_users = conn.execute("SELECT COUNT(*) as c FROM users WHERE is_blocked=1").fetchone()["c"]
        total_bots = conn.execute("SELECT COUNT(*) as c FROM deployed_bots").fetchone()["c"]
        running_bots = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE status='running'").fetchone()["c"]
        pending_reqs = conn.execute("SELECT COUNT(*) as c FROM pending_requests WHERE status='pending'").fetchone()["c"]
        total_revenue_row = conn.execute("SELECT SUM(amount) as s FROM payments WHERE status='paid'").fetchone()
        total_revenue = total_revenue_row["s"] or 0
        open_tickets = conn.execute("SELECT COUNT(*) as c FROM tickets WHERE status='open'").fetchone()["c"]

    edit_message(
        chat_id, msg_id,
        f"📊 *آمار لحظه‌ای*\n"
        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👥 کاربران: {total_users} (فعال: {active_users}, مسدود: {blocked_users})\n"
        f"🤖 ربات‌ها: {total_bots} (در حال اجرا: {running_bots})\n"
        f"⏳ درخواست‌های در انتظار: {pending_reqs}\n"
        f"🎫 تیکت‌های باز: {open_tickets}\n"
        f"💰 کل درآمد: {total_revenue:,} تومان",
        reply_markup=inline_keyboard([
            [("🔄 بروزرسانی", "realtime_stats")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def handle_weekly_stats_send(query=None):
    """ارسال آمار هفتگی - FIX: پارامتر query اختیاری شد"""
    with get_db() as conn:
        week_start = (datetime.now() - timedelta(days=7)).isoformat()

        total_users = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        new_users = conn.execute("SELECT COUNT(*) as c FROM users WHERE joined_at>=?", (week_start,)).fetchone()["c"]
        active_users = conn.execute("SELECT COUNT(*) as c FROM users WHERE last_active>=?", (week_start,)).fetchone()["c"]
        running_bots = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE status='running'").fetchone()["c"]
        stopped_bots = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE status='stopped'").fetchone()["c"]
        lib_installs = conn.execute("SELECT COUNT(*) as c FROM library_installs WHERE status='installed' AND installed_at>=?", (week_start,)).fetchone()["c"]
        top_libs = conn.execute(
            "SELECT library_name, COUNT(*) as c FROM library_installs WHERE status='installed' GROUP BY library_name ORDER BY c DESC LIMIT 3"
        ).fetchall()
        revenue_row = conn.execute("SELECT SUM(amount) as s FROM payments WHERE status='paid' AND created_at>=?", (week_start,)).fetchone()
        revenue = revenue_row["s"] or 0

        top_deployer = conn.execute(
            "SELECT u.full_name, COUNT(*) as c FROM deployed_bots b JOIN users u ON b.user_id=u.user_id WHERE b.deployed_at>=? GROUP BY b.user_id ORDER BY c DESC LIMIT 1",
            (week_start,)
        ).fetchone()
        top_installer = conn.execute(
            "SELECT u.full_name, COUNT(*) as c FROM library_installs l JOIN users u ON l.user_id=u.user_id WHERE l.installed_at>=? GROUP BY l.user_id ORDER BY c DESC LIMIT 1",
            (week_start,)
        ).fetchone()
        top_inviter = conn.execute(
            "SELECT full_name, invite_count FROM users ORDER BY invite_count DESC LIMIT 1"
        ).fetchone()

    top_libs_text = "\n".join([f"  • `{l['library_name']}` ({l['c']} بار)" for l in top_libs]) if top_libs else "  ندارد"
    week_end = datetime.now().strftime("%Y-%m-%d")
    week_start_str = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    msg = (
        f"📊 *آمار هفتگی سیستم* 📊\n\n"
        f"⏰ دوره: `{week_start_str}` تا `{week_end}`\n\n"
        f"*👥 کاربران*\n"
        f"کاربران کل: *{total_users}*\n"
        f"کاربران فعال این هفته: *{active_users}*\n"
        f"کاربران جدید: *{new_users}*\n"
        f"رشد هفتگی: *{round(new_users/max(total_users-new_users,1)*100,1)}٪*\n\n"
        f"*🤖 ربات‌ها*\n"
        f"ربات‌های فعال: *{running_bots}*\n"
        f"ربات‌های متوقف: *{stopped_bots}*\n\n"
        f"*📦 کتابخانه‌ها*\n"
        f"نصب موفق این هفته: *{lib_installs}*\n"
        f"پرکاربردترین:\n{top_libs_text}\n\n"
        f"*💰 درآمد*\n"
        f"درآمد این هفته: *{revenue:,} تومان*\n\n"
        f"*🏆 برترین‌های هفته*\n"
        f"۱. بیشترین استقرار: *{top_deployer['full_name'] if top_deployer else 'ندارد'}*\n"
        f"۲. بیشترین نصب: *{top_installer['full_name'] if top_installer else 'ندارد'}*\n"
        f"۳. بیشترین دعوت: *{top_inviter['full_name'] if top_inviter else 'ندارد'}*\n\n"
        f"*🔮 پیش‌بینی هفته آینده*\n"
        f"📈 رشد ۲۰٪ کاربران جدید\n"
        f"🤖 اضافه شدن ۵۰ ربات جدید\n"
        f"📦 نصب ۱۰۰ کتابخانه جدید\n\n"
        f"⚡ *سیستم همیشه در دسترس*\n"
        f"🛠 پشتیبانی ۲۴/۷ | 🔒 امنیت تضمینی | 🚀 سرعت بالا\n\n"
        f"🎉 *با تشکر از همراهی شما!*\n"
        f"تیم پشتیبانی 🤖"
    )

    # FIX: وقتی query وجود داره (از callback)، مستقیم برمی‌گردونه
    # وقتی query نداره (خودکار)، به مدیران می‌فرسته
    if query is None:
        for admin_id in ADMIN_IDS:
            send_message(admin_id, msg)
    else:
        return msg


# ─────────────────────────────────────────────
#  مدیریت کاربران
# ─────────────────────────────────────────────
def handle_user_management(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        return

    edit_message(
        chat_id, msg_id,
        "👥 *مدیریت کاربران*\n\nیک گزینه را انتخاب کنید:",
        reply_markup=inline_keyboard([
            [("🔍 جستجوی کاربر", "search_user_prompt"), ("📋 مشاهده کاربران", "view_users_list:0")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def handle_search_user_prompt(query: dict):
    """نمایش prompt جستجوی کاربر"""
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        return

    set_state(user_id, "admin_search_user")
    edit_message(
        chat_id, msg_id,
        "🔍 *جستجوی کاربر*\n\nآیدی عددی یا یوزرنیم کاربر مورد نظر را ارسال کنید:",
        reply_markup=inline_keyboard([[("🔙 مدیریت کاربران", "user_management")]])
    )


def handle_view_users_list(query: dict, page: int = 0):
    """نمایش لیست ۳۰ تایی کاربران با صفحه‌بندی"""
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(user_id):
        return

    page_size = 30
    offset = page * page_size

    with get_db() as conn:
        total_count = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        users_page = conn.execute(
            "SELECT user_id, username, plan, is_active, is_blocked FROM users ORDER BY user_id DESC LIMIT ? OFFSET ?",
            (page_size, offset)
        ).fetchall()

    if not users_page:
        edit_message(chat_id, msg_id, "❌ کاربری یافت نشد.",
                     reply_markup=inline_keyboard([[("🔙 مدیریت کاربران", "user_management")]]))
        return

    # ساخت دکمه‌های لیست کاربران (هر ردیف یک کاربر)
    buttons = []
    for u_row in users_page:
        status_icon = "🔴" if u_row["is_blocked"] else ("✅" if u_row["is_active"] else "⏳")
        plan_icon = {"free": "🟢", "basic": "🟡", "professional": "🔴", "enterprise": "⚫"}.get(u_row["plan"], "❓")
        uname = f"@{u_row['username']}" if u_row["username"] else "بدون یوزرنیم"
        btn_label = f"{status_icon} {u_row['user_id']} | {uname} | {plan_icon}{u_row['plan']}"
        buttons.append([(btn_label, f"admin_user_detail:{u_row['user_id']}")])

    # دکمه‌های صفحه‌بندی
    nav_buttons = []
    if page > 0:
        nav_buttons.append(("◀️ صفحه قبل", f"view_users_list:{page - 1}"))
    total_pages = (total_count + page_size - 1) // page_size
    if (page + 1) < total_pages:
        nav_buttons.append(("صفحه بعد ▶️", f"view_users_list:{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([("🔙 مدیریت کاربران", "user_management")])

    edit_message(
        chat_id, msg_id,
        f"📋 *لیست کاربران*\n\n"
        f"صفحه {page + 1} از {total_pages} | کل: {total_count} کاربر\n"
        f"(روی آیدی هر کاربر بزنید برای مدیریت)",
        reply_markup=inline_keyboard(buttons)
    )


def handle_admin_user_detail(query: dict, target_id: int):
    """نمایش اطلاعات کامل کاربر + دکمه‌های مدیریت"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        u = conn.execute("SELECT * FROM users WHERE user_id=?", (target_id,)).fetchone()
        bot_count = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE user_id=?", (target_id,)).fetchone()["c"]
        lib_count = conn.execute("SELECT COUNT(*) as c FROM library_installs WHERE user_id=? AND status='installed'", (target_id,)).fetchone()["c"]

    if not u:
        answer_callback(query["id"], "کاربر یافت نشد!", True)
        return

    u = dict(u)
    status = "✅ فعال" if u["is_active"] and not u["is_blocked"] else ("🔴 مسدود" if u["is_blocked"] else "⏳ غیرفعال")
    item_count = u.get("extra_bots", 0) + u.get("extra_libraries", 0) + u.get("extra_memory_mb", 0) // 100

    text = (
        f"👤 *{u['full_name']}*\n"
        f"آیدی عددی: `{target_id}`\n"
        f"یوزرنیم: @{u['username'] or 'ندارد'}\n"
        f"وضعیت: {status}\n"
        f"پلن: {PLANS.get(u['plan'], {}).get('name', u['plan'])}\n"
        f"امتیاز: *{u['points']}*\n"
        f"ربات‌ها: {bot_count} | کتابخانه‌ها: {lib_count}\n"
        f"دعوت‌ها: {u['invite_count']}\n"
        f"کل خرید: {u['total_spent']:,} تومان\n"
        f"عضویت: {u['joined_at'][:10] if u['joined_at'] else 'نامشخص'}"
    )

    buttons = [
        [("📩 ارسال پیام", f"admin_send_user:{target_id}"), ("🎁 هدیه امتیاز", f"admin_gift_points:{target_id}")],
        [("➖ کسر امتیاز", f"admin_deduct_points:{target_id}"), ("♻️ تغییر پلن", f"admin_change_plan:{target_id}")],
        [("🔴 مسدود کردن", f"admin_block_user:{target_id}"), ("✅ رفع مسدودی", f"admin_unblock_user:{target_id}")],
        [("🔙 لیست کاربران", "view_users_list:0"), ("🔙 مدیریت کاربران", "user_management")]
    ]
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_admin_search_user(message: dict):
    admin_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    query_text = message.get("text", "").strip()

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        if query_text.isdigit():
            u = conn.execute("SELECT * FROM users WHERE user_id=?", (int(query_text),)).fetchone()
        else:
            uname = query_text.lstrip("@")
            u = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()

    if not u:
        send_message(chat_id, "❌ کاربر یافت نشد.", reply_markup=inline_keyboard([[("🔙 مدیریت کاربران", "user_management")]]))
        return

    u = dict(u)
    uid = u["user_id"]

    with get_db() as conn:
        bot_count = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE user_id=?", (uid,)).fetchone()["c"]
        lib_count = conn.execute("SELECT COUNT(*) as c FROM library_installs WHERE user_id=? AND status='installed'", (uid,)).fetchone()["c"]

    item_count = u.get("extra_bots", 0) + u.get("extra_libraries", 0) + u.get("extra_memory_mb", 0) // 100

    status = "✅ فعال" if u["is_active"] and not u["is_blocked"] else ("🔴 مسدود" if u["is_blocked"] else "⏳ غیرفعال")

    text = (
        f"👤 *{u['full_name']}*\n"
        f"آیدی: `{uid}`\n"
        f"یوزرنیم: @{u['username'] or 'ندارد'}\n"
        f"وضعیت: {status}\n"
        f"پلن: {PLANS.get(u['plan'], {}).get('name', u['plan'])}\n"
        f"امتیاز: *{u['points']}*\n"
        f"ربات‌ها: {bot_count}\n"
        f"کتابخانه‌ها: {lib_count}\n"
        f"دعوت‌ها: {u['invite_count']}\n"
        f"آیتم‌های خریداری: {item_count}\n"
        f"کل خرید: {u['total_spent']:,} تومان\n"
        f"عضویت: {u['joined_at'][:10] if u['joined_at'] else 'نامشخص'}"
    )

    buttons = [
        [("📩 ارسال پیام", f"admin_send_user:{uid}"), ("🎁 هدیه امتیاز", f"admin_gift_points:{uid}")],
        [("➖ کسر امتیاز", f"admin_deduct_points:{uid}"), ("♻️ تغییر پلن", f"admin_change_plan:{uid}")],
        [("🔴 مسدود کردن", f"admin_block_user:{uid}"), ("✅ رفع مسدودی", f"admin_unblock_user:{uid}")],
        [("🔙 بازگشت", "user_management")]
    ]
    clear_state(admin_id)
    send_message(chat_id, text, reply_markup=inline_keyboard(buttons))


def handle_admin_block_user(query: dict, target_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    edit_message(
        chat_id, msg_id,
        f"🔴 *مسدود کردن کاربر `{target_id}`*\n\nدلیل مسدودی را انتخاب کنید:",
        reply_markup=inline_keyboard([
            [("🦠 کد مخرب", f"block_confirm:{target_id}:malicious_code")],
            [("⏰ مسدودی موقت", f"block_confirm:{target_id}:temp_block")],
            [("🚫 تخلف قوانین", f"block_confirm:{target_id}:rules_violation")],
            [("🔙 بازگشت", "admin_panel")]
        ])
    )


def handle_block_confirm(query: dict, target_id: int, reason: str):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    reason_map = {
        "malicious_code": "تلاش برای اجرای کد مخرب",
        "temp_block": "مسدودی موقت",
        "rules_violation": "نقض قوانین"
    }

    with get_db() as conn:
        conn.execute(
            "UPDATE users SET is_blocked=1, block_reason=? WHERE user_id=?",
            (reason_map.get(reason, reason), target_id)
        )
        conn.commit()

    edit_message(
        chat_id, msg_id,
        f"✅ کاربر `{target_id}` مسدود شد.\nدلیل: {reason_map.get(reason, reason)}",
        reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]])
    )
    send_message(
        target_id,
        f"❌ *حساب شما مسدود شده.*\n\nدلیل: {reason_map.get(reason, reason)}\n\nبرای رفع مسدودی با پشتیبانی تماس بگیرید."
    )


def handle_admin_change_plan(query: dict, target_id: int):
    """FIX: تابع تغییر پلن که قبلاً تعریف نشده بود"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    buttons = []
    for plan_key, plan_data in PLANS.items():
        buttons.append([(f"{plan_data['name']}", f"set_user_plan:{target_id}:{plan_key}")])
    buttons.append([("🔙 بازگشت", "user_management")])

    edit_message(
        chat_id, msg_id,
        f"♻️ *تغییر پلن کاربر `{target_id}`*\n\nپلن جدید را انتخاب کنید:",
        reply_markup=inline_keyboard(buttons)
    )


def handle_set_user_plan(query: dict, target_id: int, plan_key: str):
    """FIX: اعمال تغییر پلن"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    if plan_key not in PLANS:
        answer_callback(query["id"], "پلن نامعتبر!", True)
        return

    with get_db() as conn:
        conn.execute("UPDATE users SET plan=? WHERE user_id=?", (plan_key, target_id))
        conn.commit()

    plan_name = PLANS[plan_key]["name"]
    edit_message(
        chat_id, msg_id,
        f"✅ پلن کاربر `{target_id}` به *{plan_name}* تغییر یافت.",
        reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]])
    )
    send_message(target_id, f"♻️ پلن شما توسط مدیر به *{plan_name}* تغییر یافت.")


# ─────────────────────────────────────────────
#  سیستم تیکت
# ─────────────────────────────────────────────
def handle_ticket_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        tickets = conn.execute(
            "SELECT * FROM tickets WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
            (user_id,)
        ).fetchall()

    text = "🎫 *سیستم پشتیبانی*\n\n"
    if tickets:
        text += "تیکت‌های شما:\n"
        for t in tickets:
            status_icon = {"open": "🟡", "answered": "🟢", "closed": "⚫"}.get(t["status"], "❓")
            text += f"{status_icon} #{t['id']} - {t['subject'][:30]}\n"
    else:
        text += "هنوز تیکتی ندارید."

    edit_message(
        chat_id, msg_id,
        text,
        reply_markup=inline_keyboard([
            [("✏️ ارسال تیکت جدید", "new_ticket")],
            [("🔙 بازگشت", "main_menu")]
        ])
    )


def handle_new_ticket(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    set_state(user_id, "ticket_subject")
    edit_message(
        chat_id, msg_id,
        "🎫 *تیکت جدید*\n\nموضوع تیکت را وارد کنید:",
        reply_markup=inline_keyboard([[("❌ انصراف", "ticket_menu")]])
    )


def handle_tickets_admin(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        tickets = conn.execute(
            "SELECT t.*, u.full_name FROM tickets t JOIN users u ON t.user_id=u.user_id WHERE t.status='open' ORDER BY t.created_at DESC LIMIT 15"
        ).fetchall()

    if not tickets:
        edit_message(chat_id, msg_id, "✅ تیکت باز وجود ندارد.", reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]]))
        return

    buttons = [[(f"#{t['id']} - {t['full_name']} - {t['subject'][:20]}", f"admin_view_ticket:{t['id']}")] for t in tickets]
    buttons.append([("🔙 پنل مدیریت", "admin_panel")])
    edit_message(chat_id, msg_id, f"🎫 *تیکت‌های باز* ({len(tickets)} تیکت):", reply_markup=inline_keyboard(buttons))


def handle_admin_view_ticket(query: dict, ticket_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        t = conn.execute(
            "SELECT t.*, u.full_name, u.username FROM tickets t JOIN users u ON t.user_id=u.user_id WHERE t.id=?",
            (ticket_id,)
        ).fetchone()

    if not t:
        answer_callback(query["id"], "تیکت یافت نشد!", True)
        return

    text = (
        f"🎫 *تیکت #{t['id']}*\n\n"
        f"👤 کاربر: {t['full_name']} (@{t['username'] or 'ندارد'})\n"
        f"📌 موضوع: {t['subject']}\n"
        f"📝 پیام:\n{t['message']}\n\n"
        f"🕐 ارسال: {t['created_at'][:16] if t['created_at'] else 'نامشخص'}"
    )

    set_state(admin_id, "admin_reply_ticket", {"ticket_id": ticket_id, "user_id": t["user_id"]})
    edit_message(
        chat_id, msg_id,
        text,
        reply_markup=inline_keyboard([
            [("💬 پاسخ دادن", f"admin_reply_ticket:{ticket_id}")],
            [("✅ بستن تیکت", f"admin_close_ticket:{ticket_id}")],
            [("🔙 تیکت‌ها", "tickets_admin")]
        ])
    )


# ─────────────────────────────────────────────
#  چالش‌های کد
# ─────────────────────────────────────────────
def handle_challenges(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        challenges = conn.execute(
            "SELECT * FROM code_challenges WHERE status='active' ORDER BY created_at DESC"
        ).fetchall()

    if not challenges:
        edit_message(
            chat_id, msg_id,
            "🎯 *چالش‌های کد*\n\nهیچ چالش فعالی وجود ندارد.",
            reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]])
        )
        return

    buttons = [[(f"🏆 {c['title']}", f"view_challenge:{c['id']}")] for c in challenges]
    buttons.append([("🔙 بازگشت", "main_menu")])
    edit_message(chat_id, msg_id, "🎯 *چالش‌های کد*\n\nچالش مورد نظر را انتخاب کنید:", reply_markup=inline_keyboard(buttons))


def handle_challenge_admin(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    edit_message(
        chat_id, msg_id,
        "🏆 *مدیریت چالش‌های کد*",
        reply_markup=inline_keyboard([
            [("➕ چالش جدید", "new_challenge"), ("📋 لیست چالش‌ها", "list_challenges_admin")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def handle_list_challenges_admin(query: dict):
    """FIX: تابع لیست چالش‌ها که قبلاً تعریف نشده بود"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        challenges = conn.execute(
            "SELECT * FROM code_challenges ORDER BY created_at DESC LIMIT 20"
        ).fetchall()

    if not challenges:
        edit_message(chat_id, msg_id, "هیچ چالشی وجود ندارد.", reply_markup=inline_keyboard([[("🔙 بازگشت", "challenge_admin")]]))
        return

    text = "📋 *لیست چالش‌ها*\n\n"
    for c in challenges:
        status_icon = {"active": "🟢", "closed": "🔴", "finished": "⚫"}.get(c["status"], "❓")
        text += f"{status_icon} #{c['id']} - {c['title']}\n"

    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([[("🔙 بازگشت", "challenge_admin")]]))


# ─────────────────────────────────────────────
#  قرعه‌کشی
# ─────────────────────────────────────────────
def handle_lottery_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        lotteries = conn.execute(
            "SELECT * FROM lotteries WHERE status='active' ORDER BY created_at DESC"
        ).fetchall()

    if not lotteries:
        edit_message(
            chat_id, msg_id,
            "🎪 *قرعه‌کشی*\n\nهیچ قرعه‌کشی فعالی وجود ندارد.",
            reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]])
        )
        return

    buttons = [[(f"🎪 {l['title']} (نیاز: {l['min_points']} امتیاز)", f"join_lottery:{l['id']}")] for l in lotteries]
    buttons.append([("🔙 بازگشت", "main_menu")])
    edit_message(chat_id, msg_id, "🎪 *قرعه‌کشی‌های فعال*\n\nبرای شرکت روی نام بزنید:", reply_markup=inline_keyboard(buttons))


def handle_join_lottery(query: dict, lottery_id: int):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        lottery = conn.execute("SELECT * FROM lotteries WHERE id=? AND status='active'", (lottery_id,)).fetchone()

    if not lottery:
        answer_callback(query["id"], "قرعه‌کشی یافت نشد یا پایان یافته!", True)
        return

    points = get_points(user_id)
    if points < lottery["min_points"]:
        edit_message(
            chat_id, msg_id,
            f"❌ امتیاز کافی ندارید!\nنیاز: *{lottery['min_points']}*\nموجودی: *{points}*",
            reply_markup=inline_keyboard([[("🔙 بازگشت", "lottery_menu")]])
        )
        return

    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM lottery_entries WHERE lottery_id=? AND user_id=?",
            (lottery_id, user_id)
        ).fetchone()
        if existing:
            answer_callback(query["id"], "قبلاً ثبت‌نام کرده‌اید!", True)
            return
        conn.execute(
            "INSERT INTO lottery_entries (lottery_id, user_id, entered_at) VALUES (?,?,?)",
            (lottery_id, user_id, datetime.now().isoformat())
        )
        conn.commit()

    edit_message(
        chat_id, msg_id,
        f"✅ *ثبت‌نام در قرعه‌کشی*\n\n«{lottery['title']}» موفقیت‌آمیز بود!\n\nجایزه: {lottery['prize']}",
        reply_markup=inline_keyboard([[("🔙 بازگشت", "lottery_menu")]])
    )


def handle_lottery_admin(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    edit_message(
        chat_id, msg_id,
        "🎪 *مدیریت قرعه‌کشی*",
        reply_markup=inline_keyboard([
            [("➕ قرعه‌کشی جدید", "new_lottery"), ("🎲 انجام قرعه‌کشی", "draw_lottery")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def draw_lottery(lottery_id: int, admin_id: int):
    """انجام قرعه‌کشی"""
    with get_db() as conn:
        lottery = conn.execute("SELECT * FROM lotteries WHERE id=?", (lottery_id,)).fetchone()
        entries = conn.execute(
            "SELECT le.user_id, u.full_name FROM lottery_entries le JOIN users u ON le.user_id=u.user_id WHERE le.lottery_id=?",
            (lottery_id,)
        ).fetchall()

    if not entries:
        send_message(admin_id, "❌ هیچ شرکت‌کننده‌ای وجود ندارد!")
        return

    winners = random.sample(list(entries), min(lottery["max_winners"], len(entries)))

    with get_db() as conn:
        conn.execute(
            "UPDATE lotteries SET status='drawn', drawn_at=? WHERE id=?",
            (datetime.now().isoformat(), lottery_id)
        )
        conn.commit()

    winner_text = "\n".join([f"🏆 {w['full_name']}" for w in winners])
    msg = f"🎉 *نتایج قرعه‌کشی «{lottery['title']}»*\n\nبرندگان:\n{winner_text}"

    for aid in ADMIN_IDS:
        send_message(aid, msg)

    for winner in winners:
        add_points(winner["user_id"], 50, "برنده قرعه‌کشی")
        send_message(winner["user_id"], f"🎊 تبریک! شما در قرعه‌کشی «{lottery['title']}» برنده شدید!\nجایزه: {lottery['prize']}")


# ─────────────────────────────────────────────
#  کتابخانه اختصاصی
# ─────────────────────────────────────────────
def handle_custom_lib(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    u = get_user(user_id)
    plan = PLANS.get(u["plan"] if u else "free", PLANS["free"])

    if not plan["custom_library"]:
        edit_message(
            chat_id, msg_id,
            "❌ این قابلیت برای پلن شما فعال نیست.\nبرای دسترسی به کتابخانه اختصاصی، پلن حرفه‌ای یا بالاتر را تهیه کنید.",
            reply_markup=inline_keyboard([[("💳 ارتقای پلن", "sub_menu"), ("🔙 بازگشت", "main_menu")]])
        )
        return

    with get_db() as conn:
        libs = conn.execute("SELECT * FROM custom_libraries WHERE user_id=?", (user_id,)).fetchall()

    text = "🔑 *کتابخانه اختصاصی*\n\nدر اینجا می‌توانید متدها و کتابخانه‌های سفارشی تعریف کنید.\n"
    text += "حتی می‌توانید نام‌ها را به فارسی تغییر دهید!\n\n"

    if libs:
        text += "کتابخانه‌های شما:\n"
        for l in libs:
            text += f"📚 {l['lib_name']} (کلید: `{l['lib_key']}`)\n"

    buttons = [
        [("➕ کتابخانه جدید", "new_custom_lib"), ("🔑 استفاده از کلید", "use_lib_key")],
        [("🔙 بازگشت", "main_menu")]
    ]
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_new_custom_lib(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    set_state(user_id, "custom_lib_name")
    edit_message(
        chat_id, msg_id,
        "📚 *کتابخانه اختصاصی جدید*\n\nنام کتابخانه را وارد کنید:\n(می‌توانید فارسی باشد، مثلاً: کتابخانه_من)",
        reply_markup=inline_keyboard([[("❌ انصراف", "custom_lib")]])
    )


def process_custom_lib_code(code: str, lib_mappings: dict) -> str:
    """پردازش کد با mapping های سفارشی"""
    processed = code
    for custom_name, real_name in lib_mappings.items():
        processed = processed.replace(custom_name, real_name)
    return processed


# ─────────────────────────────────────────────
#  کاربران برتر
# ─────────────────────────────────────────────
def handle_top_users(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    with get_db() as conn:
        top_points = conn.execute(
            "SELECT full_name, points FROM users WHERE is_active=1 ORDER BY points DESC LIMIT 10"
        ).fetchall()
        top_invites = conn.execute(
            "SELECT full_name, invite_count FROM users WHERE is_active=1 ORDER BY invite_count DESC LIMIT 5"
        ).fetchall()
        top_bots = conn.execute(
            "SELECT u.full_name, COUNT(b.id) as c FROM deployed_bots b JOIN users u ON b.user_id=u.user_id GROUP BY b.user_id ORDER BY c DESC LIMIT 5"
        ).fetchall()

    text = "🏆 *کاربران برتر*\n\n"
    text += "*🥇 برترین‌ها بر اساس امتیاز:*\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, u in enumerate(top_points):
        medal = medals[i] if i < 3 else f"{i+1}."
        text += f"{medal} {u['full_name']}: *{u['points']}* امتیاز\n"

    text += "\n*👥 بیشترین دعوت:*\n"
    for i, u in enumerate(top_invites):
        text += f"{i+1}. {u['full_name']}: *{u['invite_count']}* نفر\n"

    text += "\n*🤖 بیشترین ربات:*\n"
    for i, u in enumerate(top_bots):
        text += f"{i+1}. {u['full_name']}: *{u['c']}* ربات\n"

    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]]))


# ─────────────────────────────────────────────
#  پروفایل کاربر
# ─────────────────────────────────────────────
def handle_my_profile(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    u = get_user(user_id)
    if not u:
        answer_callback(query["id"], "خطا در دریافت اطلاعات!", True)
        return

    plan = PLANS.get(u["plan"], PLANS["free"])

    with get_db() as conn:
        bot_count = conn.execute("SELECT COUNT(*) as c FROM deployed_bots WHERE user_id=?", (user_id,)).fetchone()["c"]
        lib_count = conn.execute("SELECT COUNT(*) as c FROM library_installs WHERE user_id=? AND status='installed'", (user_id,)).fetchone()["c"]

    text = (
        f"👤 *پروفایل شما*\n\n"
        f"نام: *{u['full_name']}*\n"
        f"آیدی: `{user_id}`\n"
        f"پلن: *{plan['name']}*\n"
        f"انقضای پلن: {u['plan_expires_at'][:10] if u['plan_expires_at'] else 'ندارد'}\n\n"
        f"💰 امتیاز: *{u['points']}*\n"
        f"🤖 ربات‌ها: *{bot_count}*\n"
        f"📦 کتابخانه‌ها: *{lib_count}*\n"
        f"👥 دعوت‌ها: *{u['invite_count']}*\n"
        f"💳 کل خرید: *{u['total_spent']:,}* تومان\n\n"
        f"📈 آیتم‌های اضافه:\n"
        f"• ربات: +{u['extra_bots']}\n"
        f"• حافظه: +{u['extra_memory_mb']} MB\n"
        f"• کتابخانه: +{u['extra_libraries']}\n"
    )

    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]]))


# ─────────────────────────────────────────────
#  امتیازها و پنل امتیاز
# ─────────────────────────────────────────────
def handle_points_menu(query: dict):
    user_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]
    u = get_user(user_id)

    text = (
        f"🎯 *سیستم امتیاز*\n\n"
        f"💰 امتیاز شما: *{u['points'] if u else 0}*\n\n"
        f"*روش‌های کسب امتیاز:*\n"
        f"• هر ۱۰۰۰ تومان خرید: ۱ امتیاز\n"
        f"• دعوت موفق: ۵ امتیاز\n"
        f"• برنده چالش: ۵۰ امتیاز\n"
        f"• برنده هفته (اول): ۳۰ امتیاز\n"
        f"• برنده هفته (دوم): ۲۰ امتیاز\n"
        f"• برنده هفته (سوم): ۱۰ امتیاز\n\n"
        f"*استفاده از امتیاز:*\n"
        f"• خرید آیتم از فروشگاه\n"
        f"• شرکت در قرعه‌کشی\n"
        f"• دریافت کد تخفیف یک‌بار مصرف"
    )

    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([
        [("🏪 فروشگاه آیتم", "shop_menu"), ("🎪 قرعه‌کشی", "lottery_menu")],
        [("🎟 دریافت کد تخفیف با امتیاز", "redeem_points_discount")],
        [("🔙 بازگشت", "main_menu")]
    ]))


# ─────────────────────────────────────────────
#  پنل مدیریت - تخفیف‌ها
# ─────────────────────────────────────────────
def handle_discount_panel(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    edit_message(
        chat_id, msg_id,
        "🎟 *مدیریت کدهای تخفیف*",
        reply_markup=inline_keyboard([
            [("➕ کد تخفیف ویژه", "create_discount:special")],
            [("⏰ کد تخفیف ساعتی", "create_discount:hourly")],
            [("📅 کد تخفیف مناسبتی", "create_discount:occasion")],
            [("📋 لیست کدها", "list_discounts")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def create_discount_code(
    type_: str,
    value: int,
    is_percent: bool,
    created_by: int,
    max_uses: int = 1,
    expires_at: str = None,
    plan_target: str = None
) -> str:
    code = "PORO-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    with get_db() as conn:
        conn.execute(
            "INSERT INTO discount_codes (code, type, value, is_percent, max_uses, expires_at, created_by, plan_target) VALUES (?,?,?,?,?,?,?,?)",
            (code, type_, value, 1 if is_percent else 0, max_uses, expires_at, created_by, plan_target)
        )
        conn.commit()
    return code


# ─────────────────────────────────────────────
#  پنل مدیریت - مدیریت اشتراک‌ها
# ─────────────────────────────────────────────
def handle_subscription_mgmt(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    text = "💳 *مدیریت اشتراک‌ها*\n\n"
    buttons = []
    with get_db() as conn:
        for plan_key, plan_data in PLANS.items():
            total = conn.execute("SELECT COUNT(*) as c FROM payments WHERE plan=? AND status='paid'", (plan_key,)).fetchone()["c"]
            active = conn.execute("SELECT COUNT(*) as c FROM users WHERE plan=?", (plan_key,)).fetchone()["c"]
            revenue_row = conn.execute("SELECT SUM(amount) as s FROM payments WHERE plan=? AND status='paid'", (plan_key,)).fetchone()
            revenue = revenue_row["s"] or 0
            text += f"*{plan_data['name']}*\n  خریداری شده: {total} | فعال: {active} | درآمد: {revenue:,}T\n\n"
            buttons.append([(f"👥 خریداران {plan_data['name']}", f"plan_subscribers:{plan_key}:0")])

    buttons.append([("🔙 پنل مدیریت", "admin_panel")])
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


def handle_plan_subscribers(query: dict, plan_key: str, page: int = 0):
    """نمایش لیست کاربرانی که یک پلن خاص را خریداری کرده‌اند"""
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    page_size = 20
    offset = page * page_size
    plan_name = PLANS.get(plan_key, {}).get("name", plan_key)

    with get_db() as conn:
        total_count = conn.execute(
            "SELECT COUNT(DISTINCT user_id) as c FROM payments WHERE plan=? AND status='paid'", (plan_key,)
        ).fetchone()["c"]
        subscribers = conn.execute(
            """SELECT u.user_id, u.full_name, u.username, u.plan, COUNT(p.id) as buy_count, SUM(p.amount) as total_paid
               FROM payments p JOIN users u ON p.user_id=u.user_id
               WHERE p.plan=? AND p.status='paid'
               GROUP BY p.user_id ORDER BY total_paid DESC LIMIT ? OFFSET ?""",
            (plan_key, page_size, offset)
        ).fetchall()

    if not subscribers:
        edit_message(chat_id, msg_id, f"هیچ خریداری برای پلن {plan_name} یافت نشد.",
                     reply_markup=inline_keyboard([[("🔙 مدیریت اشتراک", "subscription_mgmt")]]))
        return

    text = f"👥 *خریداران پلن {plan_name}*\n\n"
    buttons = []
    for sub in subscribers:
        uname = f"@{sub['username']}" if sub["username"] else str(sub["user_id"])
        text_btn = f"👤 {sub['full_name']} | {uname} | {sub['buy_count']}× | {(sub['total_paid'] or 0):,}T"
        buttons.append([(text_btn, f"admin_user_detail:{sub['user_id']}")])

    total_pages = (total_count + page_size - 1) // page_size
    nav = []
    if page > 0:
        nav.append(("◀️ قبل", f"plan_subscribers:{plan_key}:{page - 1}"))
    if (page + 1) < total_pages:
        nav.append(("بعد ▶️", f"plan_subscribers:{plan_key}:{page + 1}"))
    if nav:
        buttons.append(nav)

    buttons.append([("🔙 مدیریت اشتراک", "subscription_mgmt")])
    text += f"صفحه {page + 1}/{total_pages} | کل: {total_count} خریدار"
    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard(buttons))


# ─────────────────────────────────────────────
#  پنل مدیریت - درآمد
# ─────────────────────────────────────────────
def handle_revenue_panel(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        total_rev_row = conn.execute("SELECT SUM(amount) as s FROM payments WHERE status='paid'").fetchone()
        total_revenue = total_rev_row["s"] or 0
        this_month_start = datetime.now().replace(day=1).isoformat()
        month_rev_row = conn.execute(
            "SELECT SUM(amount) as s FROM payments WHERE status='paid' AND created_at>=?",
            (this_month_start,)
        ).fetchone()
        month_revenue = month_rev_row["s"] or 0
        this_week_start = (datetime.now() - timedelta(days=7)).isoformat()
        week_rev_row = conn.execute(
            "SELECT SUM(amount) as s FROM payments WHERE status='paid' AND created_at>=?",
            (this_week_start,)
        ).fetchone()
        week_revenue = week_rev_row["s"] or 0
        plan_breakdown = conn.execute(
            "SELECT plan, SUM(amount) as s, COUNT(*) as c FROM payments WHERE status='paid' GROUP BY plan"
        ).fetchall()

    text = (
        f"💰 *گزارش درآمد*\n\n"
        f"کل درآمد: *{total_revenue:,}* تومان\n"
        f"درآمد این ماه: *{month_revenue:,}* تومان\n"
        f"درآمد این هفته: *{week_revenue:,}* تومان\n\n"
        f"*جزئیات پلن‌ها:*\n"
    )
    for row in plan_breakdown:
        text += f"• {PLANS.get(row['plan'], {}).get('name', row['plan'])}: {row['s']:,}T ({row['c']} تراکنش)\n"

    edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]]))


# ─────────────────────────────────────────────
#  پنل مدیریت - توکن پرداخت
# ─────────────────────────────────────────────
def handle_payment_token_panel(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    current_token = get_setting("payment_token", PAYMENT_TOKEN)
    masked = current_token[:10] + "..." + current_token[-5:] if len(current_token) > 15 else current_token

    edit_message(
        chat_id, msg_id,
        f"💳 *توکن پرداخت*\n\nتوکن فعلی: `{masked}`",
        reply_markup=inline_keyboard([
            [("✏️ تغییر توکن", "change_payment_token")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


def handle_change_payment_token(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    set_state(admin_id, "change_payment_token")
    edit_message(
        chat_id, msg_id,
        "💳 *تغییر توکن پرداخت*\n\nتوکن جدید را ارسال کنید:",
        reply_markup=inline_keyboard([[("❌ انصراف", "payment_token_panel")]])
    )


# ─────────────────────────────────────────────
#  تنظیمات مدیر
# ─────────────────────────────────────────────
def handle_admin_settings(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    edit_message(
        chat_id, msg_id,
        "⚙️ *تنظیمات ربات*",
        reply_markup=inline_keyboard([
            [("📢 تغییر کانال", "change_channel"), ("🔗 تغییر لینک دعوت", "change_invite_base")],
            [("👥 تعداد نیاز دعوت", "change_required_invites")],
            [("💰 تغییر قیمت‌ها", "change_prices")],
            [("🔙 پنل مدیریت", "admin_panel")]
        ])
    )


# ─────────────────────────────────────────────
#  درخواست‌های در انتظار مدیر
# ─────────────────────────────────────────────
def handle_pending_requests(query: dict):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        reqs = conn.execute(
            "SELECT pr.*, u.full_name FROM pending_requests pr JOIN users u ON pr.user_id=u.user_id WHERE pr.status='pending' ORDER BY pr.created_at DESC LIMIT 20"
        ).fetchall()

    if not reqs:
        edit_message(
            chat_id, msg_id,
            "✅ هیچ درخواست در انتظاری وجود ندارد.",
            reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]])
        )
        return

    type_fa = {"deploy": "🚀 استقرار", "install_lib": "📦 نصب", "enterprise": "⚫ سازمانی"}
    buttons = [[(f"{type_fa.get(r['type'], r['type'])} - {r['full_name']}", f"view_request:{r['id']}")] for r in reqs]
    buttons.append([("🔙 پنل مدیریت", "admin_panel")])

    edit_message(
        chat_id, msg_id,
        f"⏳ *درخواست‌های در انتظار* ({len(reqs)} درخواست):",
        reply_markup=inline_keyboard(buttons)
    )


def handle_view_request(query: dict, req_id: int):
    admin_id = query["from"]["id"]
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    if not is_admin(admin_id):
        return

    with get_db() as conn:
        req = conn.execute(
            "SELECT pr.*, u.full_name FROM pending_requests pr JOIN users u ON pr.user_id=u.user_id WHERE pr.id=?",
            (req_id,)
        ).fetchone()

    if not req:
        answer_callback(query["id"], "درخواست یافت نشد!", True)
        return

    req_data = json.loads(req["data"])
    text = f"📋 *درخواست #{req_id}*\n\nنوع: {req['type']}\nکاربر: {req['full_name']} (`{req['user_id']}`)\n\n"
    for k, v in req_data.items():
        text += f"• {k}: `{v}`\n"

    type_approve_map = {
        "deploy": f"admin_approve_deploy:{req_id}",
        "install_lib": f"admin_approve_lib:{req_id}",
        "enterprise": f"admin_approve_enterprise:{req_id}"
    }
    type_reject_map = {
        "deploy": f"admin_reject_deploy:{req_id}",
        "install_lib": f"admin_reject_lib:{req_id}",
        "enterprise": f"admin_reject_enterprise:{req_id}"
    }

    edit_message(
        chat_id, msg_id,
        text,
        reply_markup=inline_keyboard([
            [("✅ تایید", type_approve_map.get(req["type"], "noop")), ("❌ رد", type_reject_map.get(req["type"], "noop"))],
            [("🔙 درخواست‌ها", "pending_requests")]
        ])
    )


# ─────────────────────────────────────────────
#  ترمینال رنگی PDF
# ─────────────────────────────────────────────
def generate_colored_terminal_pdf(bot_id: int, user_id: int):
    """تولید PDF ترمینال رنگی"""
    with get_db() as conn:
        bot = conn.execute("SELECT * FROM deployed_bots WHERE id=? AND user_id=?", (bot_id, user_id)).fetchone()

    if not bot or not bot["file_path"]:
        return

    try:
        with open(bot["file_path"], "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except:
        return

    colors = {
        "keyword": "#FF6B9D",
        "string": "#C3E88D",
        "comment": "#546E7A",
        "number": "#F78C6C",
        "function": "#82AAFF",
        "class": "#FFCB6B",
        "decorator": "#C792EA",
        "default": "#EEFFFF"
    }

    keywords = {"def", "class", "import", "from", "return", "if", "else", "elif",
                "for", "while", "try", "except", "with", "as", "in", "not", "and", "or",
                "True", "False", "None", "lambda", "yield", "async", "await", "pass", "break", "continue"}

    def colorize_line(line: str) -> str:
        line_stripped = line.strip()
        if line_stripped.startswith("#"):
            return f'<span style="color:{colors["comment"]}">{line.rstrip()}</span>'
        parts = []
        for word in re.split(r'(\s+|[().,\[\]{}:=+\-*/<>!])', line.rstrip()):
            if word in keywords:
                parts.append(f'<span style="color:{colors["keyword"]}">{word}</span>')
            elif word.startswith('"') or word.startswith("'"):
                parts.append(f'<span style="color:{colors["string"]}">{word}</span>')
            elif word.isdigit():
                parts.append(f'<span style="color:{colors["number"]}">{word}</span>')
            elif word.startswith("@"):
                parts.append(f'<span style="color:{colors["decorator"]}">{word}</span>')
            else:
                parts.append(f'<span style="color:{colors["default"]}">{word}</span>')
        return "".join(parts)

    LINES_PER_IMAGE = 10
    pages = [lines[i:i+LINES_PER_IMAGE] for i in range(0, len(lines), LINES_PER_IMAGE)]

    html_pages = ""
    for page_num, page_lines in enumerate(pages, 1):
        lines_html = ""
        for i, line in enumerate(page_lines):
            abs_line = (page_num-1)*LINES_PER_IMAGE + i + 1
            colored = colorize_line(line)
            lines_html += f'<div class="line"><span class="ln">{abs_line:3}</span>{colored}</div>\n'

        html_pages += f"""
<div class="page">
  <div class="page-header">
    <span class="bot-name">🤖 {bot['bot_name']}</span>
    <span class="page-num">صفحه {page_num} از {len(pages)}</span>
  </div>
  <div class="code-block">
    {lines_html}
  </div>
</div>
"""

    html = f"""<!DOCTYPE html>
<html dir="ltr">
<head>
<meta charset="UTF-8">
<style>
  @page {{ size: A4; margin: 15mm; }}
  * {{ box-sizing: border-box; }}
  body {{ background: #1E1E2E; font-family: 'Courier New', monospace; font-size: 11px; margin: 0; padding: 0; }}
  .page {{ page-break-after: always; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
  .page-header {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #313244; border-radius: 6px; margin-bottom: 10px; }}
  .bot-name {{ color: #CBA6F7; font-weight: bold; font-size: 13px; }}
  .page-num {{ color: #A6ADC8; font-size: 11px; }}
  .code-block {{ background: #181825; padding: 10px; border-radius: 6px; border: 1px solid #313244; }}
  .line {{ line-height: 1.7; white-space: pre; }}
  .ln {{ color: #585B70; margin-right: 12px; user-select: none; }}
</style>
</head>
<body>
{html_pages}
</body>
</html>"""

    html_path = LOGS_DIR / f"terminal_{bot_id}.html"
    pdf_path = LOGS_DIR / f"terminal_{bot_id}.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    try:
        subprocess.run(
            ["wkhtmltopdf", "--page-size", "A4", str(html_path), str(pdf_path)],
            capture_output=True, timeout=60
        )
    except FileNotFoundError:
        send_document(user_id, html_path, f"📟 ترمینال رنگی ربات *{bot['bot_name']}*")
        return
    except Exception as e:
        log.error(f"PDF error: {e}")
        return

    if pdf_path.exists():
        send_document(user_id, pdf_path, f"📟 ترمینال رنگی ربات *{bot['bot_name']}*")


# ─────────────────────────────────────────────
#  تنظیم هفتگی خودکار
# ─────────────────────────────────────────────
def weekly_scheduler():
    """ارسال خودکار آمار هفتگی"""
    while True:
        now = datetime.now()
        if now.weekday() == 5 and now.hour == 9 and now.minute == 0:
            handle_weekly_stats_send()  # بدون query → ارسال به مدیران
            announce_weekly_winners()
            time.sleep(70)
        else:
            time.sleep(30)


def announce_weekly_winners():
    """اعلان برندگان هفتگی"""
    with get_db() as conn:
        top_users = conn.execute(
            "SELECT user_id, full_name, points FROM users WHERE is_active=1 ORDER BY points DESC LIMIT 3"
        ).fetchall()

    prizes = [30, 20, 10]
    medals = ["🥇", "🥈", "🥉"]
    discounts = [30, 20, 10]

    msg = "🏆 *برندگان هفته اعلام شدند!*\n\n"
    for i, u in enumerate(top_users):
        prize_points = prizes[i]
        discount = discounts[i]
        add_points(u["user_id"], prize_points, "برنده هفته")
        dc_code = create_discount_code(
            "weekly_winner", discount, True, ADMIN_IDS[0],
            max_uses=1, plan_target=None
        )
        send_message(
            u["user_id"],
            f"🎉 {medals[i]} شما برنده هفته شدید!\n"
            f"🎁 {prize_points} امتیاز هدیه داده شد.\n"
            f"🎟 کد تخفیف {discount}٪ شما: `{dc_code}`"
        )
        msg += f"{medals[i]} {u['full_name']} (+{prize_points} امتیاز)\n"

    for admin_id in ADMIN_IDS:
        send_message(admin_id, msg)


# ─────────────────────────────────────────────
#  پردازش callback_query
# ─────────────────────────────────────────────
def handle_callback_query(update: dict):
    query = update["callback_query"]
    user_id = query["from"]["id"]
    data = query.get("data", "")
    chat_id = query["message"]["chat"]["id"]
    msg_id = query["message"]["message_id"]

    answer_callback(query["id"])

    # بررسی مسدودی
    u = get_user(user_id)
    if u and u["is_blocked"] and not is_admin(user_id):
        send_message(chat_id, f"❌ حساب شما مسدود است.\nدلیل: {u['block_reason'] or 'نامشخص'}")
        return

    # روتینگ callback
    if data == "main_menu":
        edit_message(chat_id, msg_id, "🏠 *منوی اصلی*\n\nانتخاب کنید:", reply_markup=main_menu(user_id))
    elif data == "bots_menu":
        handle_bots_menu(query)
    elif data.startswith("bot_info:"):
        handle_bot_info(query, int(data.split(":")[1]))
    elif data.startswith("delete_bot_confirm:"):
        handle_delete_bot_confirm(query, int(data.split(":")[1]))
    elif data.startswith("delete_bot_final:"):
        handle_delete_bot_final(query, int(data.split(":")[1]))
    elif data == "deploy_new":
        if not is_active_user(user_id) and not is_admin(user_id):
            answer_callback(query["id"], "ابتدا ربات را فعال کنید!", True)
            return
        handle_deploy_new(query)
    elif data == "deploy_submit":
        handle_deploy_submit(query)
    elif data == "install_lib":
        if not is_active_user(user_id) and not is_admin(user_id):
            answer_callback(query["id"], "ابتدا ربات را فعال کنید!", True)
            return
        handle_install_lib(query)
    elif data == "shop_menu":
        handle_shop_menu(query)
    elif data.startswith("buy_item:"):
        handle_buy_item(query, data.split(":")[1])
    elif data == "sub_menu":
        handle_sub_menu(query)
    elif data.startswith("view_plan:"):
        handle_view_plan(query, data.split(":")[1])
    elif data.startswith("checkout:"):
        parts = data.split(":")
        handle_checkout(query, parts[1], parts[2])
    elif data.startswith("pay_now:"):
        parts = data.split(":")
        handle_pay_now(query, parts[1], parts[2], int(parts[3]))
    elif data == "points_menu":
        handle_points_menu(query)
    elif data == "top_users":
        handle_top_users(query)
    elif data == "challenges":
        handle_challenges(query)
    elif data == "lottery_menu":
        handle_lottery_menu(query)
    elif data.startswith("join_lottery:"):
        handle_join_lottery(query, int(data.split(":")[1]))
    elif data == "ticket_menu":
        handle_ticket_menu(query)
    elif data == "new_ticket":
        handle_new_ticket(query)
    elif data == "custom_lib":
        handle_custom_lib(query)
    elif data == "new_custom_lib":
        handle_new_custom_lib(query)
    elif data == "my_invite":
        invite_count = u["invite_count"] if u else 0
        link = get_invite_link(user_id)
        edit_message(
            chat_id, msg_id,
            f"🔗 *لینک دعوت شما*\n\n`{link}`\n\n"
            f"دعوت‌های موفق: *{invite_count}*\n"
            f"امتیاز هر دعوت: *۵ امتیاز*"
        )
    elif data == "my_profile":
        handle_my_profile(query)
    elif data == "my_stats":
        handle_my_profile(query)
    elif data == "check_activation":
        ok, reason = check_activation(user_id)
        if ok:
            activate_user(user_id)
        else:
            answer_callback(query["id"], f"هنوز شرایط کامل نشده: {reason}", True)
    elif data == "joined_channel":
        with get_db() as conn:
            conn.execute("UPDATE users SET channel_joined=1 WHERE user_id=?", (user_id,))
            conn.commit()
        ok, reason = check_activation(user_id)
        if ok:
            activate_user(user_id)
        else:
            answer_callback(query["id"], "ممنون! پس از تکمیل دعوت‌ها فعال می‌شوید.", True)

    # پنل مدیریت
    elif data == "admin_panel":
        handle_admin_panel(query)
    elif data == "broadcast_msg":
        handle_broadcast_msg(query)
    elif data == "realtime_stats":
        handle_realtime_stats(query)
    elif data == "weekly_stats":
        # FIX: query رو پاس می‌دیم تا مقدار return بشه
        msg = handle_weekly_stats_send(query)
        if msg:
            edit_message(chat_id, msg_id, msg, reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]]))
    elif data == "pending_requests":
        handle_pending_requests(query)
    elif data.startswith("view_request:"):
        handle_view_request(query, int(data.split(":")[1]))
    elif data.startswith("admin_approve_deploy:"):
        handle_admin_approve_deploy(query, int(data.split(":")[1]))
    elif data.startswith("admin_reject_deploy:"):
        handle_admin_reject_deploy(query, int(data.split(":")[1]))
    elif data.startswith("admin_approve_lib:"):
        handle_admin_approve_lib(query, int(data.split(":")[1]))
    elif data.startswith("admin_reject_lib:"):
        # FIX: حالا تابع مستقل داره
        handle_admin_reject_lib(query, int(data.split(":")[1]))
    elif data == "revenue_panel":
        handle_revenue_panel(query)
    elif data == "user_management":
        handle_user_management(query)
    elif data.startswith("admin_block_user:"):
        handle_admin_block_user(query, int(data.split(":")[1]))
    elif data.startswith("block_confirm:"):
        parts = data.split(":")
        handle_block_confirm(query, int(parts[1]), parts[2])
    elif data.startswith("admin_unblock_user:"):
        target_id = int(data.split(":")[1])
        with get_db() as conn:
            conn.execute("UPDATE users SET is_blocked=0, block_reason=NULL WHERE user_id=?", (target_id,))
            conn.commit()
        answer_callback(query["id"], "✅ رفع مسدودی انجام شد.", True)
        send_message(target_id, "✅ حساب شما رفع مسدودی شد. می‌توانید از ربات استفاده کنید.")
    elif data.startswith("admin_gift_points:"):
        target_id = int(data.split(":")[1])
        set_state(user_id, "admin_gift_points", {"target_id": target_id})
        send_message(chat_id, f"🎁 تعداد امتیاز هدیه به کاربر `{target_id}` را وارد کنید:")
    elif data.startswith("admin_send_user:"):
        target_id = int(data.split(":")[1])
        set_state(user_id, "admin_send_user_msg", {"target_id": target_id})
        send_message(chat_id, f"💬 پیام برای کاربر `{target_id}` را وارد کنید:")
    elif data.startswith("admin_change_plan:"):
        # FIX: حالا تابع مستقل داره
        handle_admin_change_plan(query, int(data.split(":")[1]))
    elif data.startswith("set_user_plan:"):
        parts = data.split(":")
        handle_set_user_plan(query, int(parts[1]), parts[2])
    elif data == "discount_panel":
        handle_discount_panel(query)
    elif data.startswith("create_discount:"):
        dtype = data.split(":")[1]
        set_state(user_id, f"create_discount_{dtype}")
        prompts = {
            "special": "🎟 ایجاد کد تخفیف ویژه\n\nمقدار تخفیف (درصد) را وارد کنید:\n(مثال: 20)",
            "hourly": "⏰ ایجاد کد تخفیف ساعتی\n\nمقدار تخفیف (درصد) را وارد کنید:",
            "occasion": "📅 ایجاد کد تخفیف مناسبتی\n\nمقدار تخفیف (درصد) را وارد کنید:"
        }
        send_message(chat_id, prompts.get(dtype, "مقدار تخفیف:"))
    elif data == "subscription_mgmt":
        handle_subscription_mgmt(query)
    elif data == "payment_token_panel":
        handle_payment_token_panel(query)
    elif data == "change_payment_token":
        handle_change_payment_token(query)
    elif data == "lottery_admin":
        handle_lottery_admin(query)
    elif data == "challenge_admin":
        handle_challenge_admin(query)
    elif data == "list_challenges_admin":
        # FIX: حالا تابع مستقل داره
        handle_list_challenges_admin(query)
    elif data == "tickets_admin":
        handle_tickets_admin(query)
    elif data.startswith("admin_view_ticket:"):
        handle_admin_view_ticket(query, int(data.split(":")[1]))
    elif data.startswith("admin_reply_ticket:"):
        ticket_id = int(data.split(":")[1])
        with get_db() as conn:
            t = conn.execute("SELECT user_id FROM tickets WHERE id=?", (ticket_id,)).fetchone()
        set_state(user_id, "admin_reply_ticket", {"ticket_id": ticket_id, "user_id": t["user_id"] if t else 0})
        send_message(chat_id, "💬 پاسخ خود را وارد کنید:")
    elif data.startswith("admin_close_ticket:"):
        ticket_id = int(data.split(":")[1])
        with get_db() as conn:
            conn.execute("UPDATE tickets SET status='closed' WHERE id=?", (ticket_id,))
            conn.commit()
        answer_callback(query["id"], "✅ تیکت بسته شد.", True)
    elif data == "admin_settings":
        handle_admin_settings(query)
    elif data.startswith("view_log:"):
        bot_id = int(data.split(":")[1])
        with get_db() as conn:
            bot = conn.execute("SELECT * FROM deployed_bots WHERE id=? AND user_id=?", (bot_id, user_id)).fetchone()
        if bot and bot["log_file"] and Path(bot["log_file"]).exists():
            send_document(user_id, bot["log_file"], f"📋 لاگ ربات *{bot['bot_name']}*")
        else:
            answer_callback(query["id"], "فایل لاگ موجود نیست.", True)
    elif data.startswith("stop_bot:"):
        bot_id = int(data.split(":")[1])
        proc = bot_processes.get(bot_id)
        if proc:
            proc.terminate()
        with get_db() as conn:
            conn.execute("UPDATE deployed_bots SET status='stopped', pid=NULL WHERE id=?", (bot_id,))
            conn.commit()
        answer_callback(query["id"], "✅ ربات متوقف شد.")
    elif data.startswith("restart_bot:"):
        bot_id = int(data.split(":")[1])
        with get_db() as conn:
            bot = conn.execute("SELECT * FROM deployed_bots WHERE id=?", (bot_id,)).fetchone()
        if bot:
            old_proc = bot_processes.get(bot_id)
            if old_proc:
                old_proc.terminate()
            start_bot_process(bot_id, bot["file_path"], bot["bot_name"], user_id)
            with get_db() as conn:
                conn.execute("UPDATE deployed_bots SET status='running' WHERE id=?", (bot_id,))
                conn.commit()
            answer_callback(query["id"], "✅ ربات مجدداً راه‌اندازی شد.")
    elif data == "enterprise_request":
        with get_db() as conn:
            conn.execute(
                "INSERT INTO pending_requests (type, user_id, data, created_at) VALUES (?,?,?,?)",
                ("enterprise", user_id, json.dumps({"user_id": user_id}), datetime.now().isoformat())
            )
            conn.commit()
        for aid in ADMIN_IDS:
            send_message(aid, f"⚫ *درخواست پنل سازمانی*\n\n👤 کاربر: `{user_id}`\nبرای تماس و مذاکره درخواست داده.")
        answer_callback(query["id"], "✅ درخواست ارسال شد. به زودی با شما تماس می‌گیریم.", True)
    elif data == "new_lottery" and is_admin(user_id):
        set_state(user_id, "new_lottery_title")
        send_message(chat_id, "🎪 *قرعه‌کشی جدید*\n\nعنوان قرعه‌کشی را وارد کنید:")
    elif data == "draw_lottery" and is_admin(user_id):
        with get_db() as conn:
            lotteries = conn.execute("SELECT * FROM lotteries WHERE status='active'").fetchall()
        if not lotteries:
            answer_callback(query["id"], "قرعه‌کشی فعالی وجود ندارد!", True)
            return
        buttons = [[(f"🎪 {l['title']}", f"do_draw:{l['id']}")] for l in lotteries]
        buttons.append([("🔙 بازگشت", "lottery_admin")])
        edit_message(chat_id, msg_id, "کدام قرعه‌کشی را انجام دهم؟", reply_markup=inline_keyboard(buttons))
    elif data.startswith("do_draw:") and is_admin(user_id):
        lottery_id = int(data.split(":")[1])
        draw_lottery(lottery_id, user_id)
        answer_callback(query["id"], "✅ قرعه‌کشی انجام شد.")
    elif data == "new_challenge" and is_admin(user_id):
        set_state(user_id, "new_challenge_title")
        send_message(chat_id, "🏆 *چالش جدید*\n\nعنوان چالش را وارد کنید:")
    elif data.startswith("view_challenge:"):
        challenge_id = int(data.split(":")[1])
        with get_db() as conn:
            ch = conn.execute("SELECT * FROM code_challenges WHERE id=?", (challenge_id,)).fetchone()
        if ch:
            edit_message(
                chat_id, msg_id,
                f"🏆 *{ch['title']}*\n\n{ch['description']}\n\n⏰ مهلت: {ch['deadline'][:10] if ch['deadline'] else 'نامحدود'}",
                reply_markup=inline_keyboard([
                    [("📤 ارسال کد", f"submit_challenge:{challenge_id}")],
                    [("🔙 چالش‌ها", "challenges")]
                ])
            )
    elif data.startswith("submit_challenge:"):
        challenge_id = int(data.split(":")[1])
        set_state(user_id, "submit_challenge", {"challenge_id": challenge_id})
        edit_message(chat_id, msg_id, "📤 فایل کد پایتون خود را ارسال کنید:")
    elif data == "redeem_points_discount":
        if not u or u["points"] < 50:
            answer_callback(query["id"], "حداقل ۵۰ امتیاز نیاز است!", True)
            return
        if spend_points(user_id, 50):
            dc = create_discount_code("points_redemption", 10, True, user_id, max_uses=1)
            answer_callback(query["id"], f"✅ کد تخفیف: {dc}", True)
            send_message(chat_id, f"🎟 کد تخفیف ۱۰٪ شما:\n`{dc}`\n\nاین کد یک‌بار مصرف است.")
    elif data == "list_discounts" and is_admin(user_id):
        with get_db() as conn:
            codes = conn.execute("SELECT * FROM discount_codes ORDER BY id DESC LIMIT 20").fetchall()
        text = "🎟 *لیست کدهای تخفیف*\n\n"
        for c in codes:
            status_dc = "✅ فعال" if c["is_active"] else "❌ غیرفعال"
            text += f"`{c['code']}` - {c['value']}{'%' if c['is_percent'] else 'T'} - {status_dc} ({c['used_count']}/{c['max_uses']})\n"
        edit_message(chat_id, msg_id, text, reply_markup=inline_keyboard([[("🔙 تخفیف‌ها", "discount_panel")]]))
    elif data.startswith("enter_discount:"):
        parts = data.split(":")
        set_state(user_id, "enter_discount_code", {"plan": parts[1], "duration": parts[2]})
        edit_message(chat_id, msg_id, "🎟 کد تخفیف خود را وارد کنید:")
    elif data == "set_mirror":
        set_state(user_id, "set_mirror")
        send_message(chat_id, "🌐 آدرس میرور را وارد کنید:\n(مثال: https://pypi.tuna.tsinghua.edu.cn/simple)")
    elif data == "use_lib_key":
        set_state(user_id, "use_lib_key")
        send_message(chat_id, "🔑 کلید کتابخانه اختصاصی را وارد کنید:")
    elif data == "noop":
        pass
    else:
        log.warning(f"Unhandled callback: {data}")


# ─────────────────────────────────────────────
#  پردازش پیام‌های متنی و فایل
# ─────────────────────────────────────────────
def handle_message(update):
    message = update.get("message", {})

    # FIX: چک کردن وجود "from" در پیام
    if "from" not in message:
        return

    user = message["from"]
    user_id = user["id"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # ثبت/آپدیت کاربر
    username = message["from"].get("username", "")
    full_name = f"{message['from'].get('first_name','')} {message['from'].get('last_name','')}".strip()
    upsert_user(user_id, username, full_name)

    # بررسی مسدودی
    u = get_user(user_id)
    if u and u["is_blocked"] and not is_admin(user_id):
        send_message(chat_id, f"❌ حساب شما مسدود است.\nدلیل: {u['block_reason'] or 'نامشخص'}")
        return

    # /start
    if text.startswith("/start"):
        payload = text.split(" ")[1] if " " in text else ""
        handle_start(message, payload)
        return

    # /help
    if text == "/help":
        send_message(
            chat_id,
            "🤖 *راهنمای Poro Bot*\n\n"
            "• /start - شروع ربات\n"
            "• /menu - منوی اصلی\n"
            "• /stats - آمار شما\n"
            "• /invite - لینک دعوت\n"
            "• /support - تیکت پشتیبانی",
            reply_markup=main_menu(user_id)
        )
        return

    if text == "/menu":
        send_message(chat_id, "🏠 *منوی اصلی*", reply_markup=main_menu(user_id))
        return

    state = get_state(user_id)
    st = state["state"]

    # ─── State machine ───
    if st == "deploy_waiting_name":
        handle_deploy_name(message)

    elif st in ("deploy_waiting_file", "deploy_confirm"):
        if "document" in message:
            handle_deploy_file(message)
        elif text:
            send_message(chat_id, "لطفاً فایل .py ارسال کنید.")

    elif st == "install_lib_name":
        handle_install_lib_name(message)

    elif st == "broadcast_waiting_msg" and is_admin(user_id):
        handle_broadcast_content(message)

    elif st == "admin_search_user" and is_admin(user_id):
        handle_admin_search_user(message)

    elif st == "reject_deploy_reason" and is_admin(user_id):
        req_id = state["data"]["req_id"]
        reason = text
        target_user_id = state["data"].get("user_id", 0)
        with get_db() as conn:
            req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()
            if req:
                req_data = json.loads(req["data"])
                conn.execute(
                    "UPDATE deployed_bots SET status='rejected' WHERE id=?",
                    (req_data.get("bot_id"),)
                )
                conn.execute("UPDATE pending_requests SET status='rejected' WHERE id=?", (req_id,))
                conn.commit()
                # FIX: استفاده از user_id که در state ذخیره شده
                send_message(req["user_id"], f"❌ درخواست استقرار ربات رد شد.\nدلیل: {reason}")
        send_message(chat_id, "✅ رد درخواست ثبت شد.")
        clear_state(user_id)

    elif st == "reject_lib_reason" and is_admin(user_id):
        req_id = state["data"]["req_id"]
        reason = text
        with get_db() as conn:
            req = conn.execute("SELECT * FROM pending_requests WHERE id=?", (req_id,)).fetchone()
            if req:
                req_data = json.loads(req["data"])
                conn.execute(
                    "UPDATE library_installs SET status='rejected' WHERE id=?",
                    (req_data.get("install_id"),)
                )
                conn.execute("UPDATE pending_requests SET status='rejected' WHERE id=?", (req_id,))
                conn.commit()
                send_message(req["user_id"], f"❌ درخواست نصب کتابخانه رد شد.\nدلیل: {reason}")
        send_message(chat_id, "✅ رد ثبت شد.")
        clear_state(user_id)

    elif st == "admin_gift_points" and is_admin(user_id):
        if text.isdigit():
            target_id = state["data"]["target_id"]
            amount = int(text)
            add_points(target_id, amount, "هدیه از مدیر")
            send_message(target_id, f"🎁 {amount} امتیاز از طرف مدیر به شما هدیه داده شد!")
            send_message(chat_id, f"✅ {amount} امتیاز به کاربر `{target_id}` داده شد.")
            clear_state(user_id)
        else:
            send_message(chat_id, "❌ عدد معتبر وارد کنید.")

    elif st == "admin_send_user_msg" and is_admin(user_id):
        target_id = state["data"]["target_id"]
        send_message(target_id, f"📩 *پیام از مدیر:*\n\n{text}")
        send_message(chat_id, "✅ پیام ارسال شد.")
        clear_state(user_id)

    elif st == "change_payment_token" and is_admin(user_id):
        set_setting("payment_token", text.strip())
        send_message(chat_id, "✅ توکن پرداخت بروزرسانی شد.")
        clear_state(user_id)

    elif st == "ticket_subject":
        set_state(user_id, "ticket_message", {"subject": text})
        send_message(chat_id, f"📌 موضوع: *{text}*\n\nحالا متن تیکت را وارد کنید:")

    elif st == "ticket_message":
        subject = state["data"]["subject"]
        with get_db() as conn:
            conn.execute(
                "INSERT INTO tickets (user_id, subject, message, created_at) VALUES (?,?,?,?)",
                (user_id, subject, text, datetime.now().isoformat())
            )
            ticket_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.commit()
        # FIX: u ممکنه None باشه
        user_name = u["full_name"] if u else str(user_id)
        for admin_id in ADMIN_IDS:
            send_message(
                admin_id,
                f"🎫 *تیکت جدید #{ticket_id}*\n\n"
                f"👤 {user_name}\n📌 {subject}\n\n{text[:300]}",
                reply_markup=inline_keyboard([[("👁 مشاهده تیکت", f"admin_view_ticket:{ticket_id}")]])
            )
        send_message(chat_id, f"✅ تیکت #{ticket_id} ثبت شد. به زودی پاسخ می‌دهیم.", reply_markup=inline_keyboard([[("🔙 بازگشت", "main_menu")]]))
        clear_state(user_id)

    elif st == "admin_reply_ticket" and is_admin(user_id):
        ticket_id = state["data"]["ticket_id"]
        target_user_id = state["data"]["user_id"]
        with get_db() as conn:
            conn.execute(
                "UPDATE tickets SET reply=?, replied_by=?, replied_at=?, status='answered' WHERE id=?",
                (text, user_id, datetime.now().isoformat(), ticket_id)
            )
            conn.commit()
        send_message(target_user_id, f"💬 *پاسخ تیکت #{ticket_id}:*\n\n{text}")
        send_message(chat_id, "✅ پاسخ ارسال شد.")
        clear_state(user_id)

    elif st == "custom_lib_name":
        lib_name = text.strip()
        lib_key = "KEY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        set_state(user_id, "custom_lib_mappings", {"lib_name": lib_name, "lib_key": lib_key, "mappings": {}})
        send_message(
            chat_id,
            f"📚 کتابخانه: *{lib_name}*\n🔑 کلید: `{lib_key}`\n\n"
            f"حالا mapping ها را وارد کنید.\nهر خط یک mapping: `نام_سفارشی=نام_اصلی`\n\n"
            f"مثال:\n`درخواست=requests`\n`دریافت=get`\n`ارسال=post`\n\n"
            f"وقتی تمام شد «ذخیره» بنویسید:",
            reply_markup=inline_keyboard([[("❌ انصراف", "custom_lib")]])
        )

    elif st == "custom_lib_mappings":
        if text.strip().lower() == "ذخیره":
            lib_name = state["data"]["lib_name"]
            lib_key = state["data"]["lib_key"]
            mappings = state["data"]["mappings"]
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO custom_libraries (user_id, lib_name, lib_key, mappings, created_at) VALUES (?,?,?,?,?)",
                    (user_id, lib_name, lib_key, json.dumps(mappings, ensure_ascii=False), datetime.now().isoformat())
                )
                conn.commit()
            send_message(
                chat_id,
                f"✅ کتابخانه اختصاصی *{lib_name}* ذخیره شد!\n🔑 کلید: `{lib_key}`",
                reply_markup=inline_keyboard([[("🔑 کتابخانه اختصاصی", "custom_lib")]])
            )
            clear_state(user_id)
        elif "=" in text:
            parts_lines = text.strip().split("\n")
            mappings = state["data"]["mappings"]
            added = 0
            for line in parts_lines:
                if "=" in line:
                    k, v = line.split("=", 1)
                    mappings[k.strip()] = v.strip()
                    added += 1
            set_state(user_id, "custom_lib_mappings", {**state["data"], "mappings": mappings})
            send_message(chat_id, f"✅ {added} mapping اضافه شد.\nادامه دهید یا «ذخیره» بنویسید.")
        else:
            send_message(chat_id, "❓ mapping را به شکل `نام_سفارشی=نام_اصلی` وارد کنید یا «ذخیره» بنویسید.")

    elif st == "enter_discount_code":
        plan = state["data"]["plan"]
        duration = state["data"]["duration"]
        code = text.strip().upper()
        valid, discount_val, dc_obj = validate_discount_code(code, user_id, plan)
        if valid and isinstance(dc_obj, dict):
            apply_discount_code(dc_obj["id"], user_id)
            plan_data = PLANS[plan]
            sub = plan_data["subscriptions"][duration]
            amount_off = int(sub["price"] * discount_val / 100) if dc_obj["is_percent"] else discount_val
            final_price = max(0, sub["price"] - amount_off)
            send_message(
                chat_id,
                f"✅ کد تخفیف اعمال شد!\n\n"
                f"تخفیف: *{discount_val}{'٪' if dc_obj['is_percent'] else ' تومان'}*\n"
                f"قیمت نهایی: *{final_price:,} تومان*",
                reply_markup=inline_keyboard([
                    [("💰 پرداخت", f"pay_now:{plan}:{duration}:{amount_off}")],
                    [("❌ انصراف", f"view_plan:{plan}")]
                ])
            )
        else:
            # FIX: dc_obj اینجا رشته دلیل خطاست
            send_message(chat_id, f"❌ {dc_obj if isinstance(dc_obj, str) else 'کد نامعتبر'}")
        clear_state(user_id)

    elif st and st.startswith("create_discount_") and is_admin(user_id):
        dtype = st.replace("create_discount_", "")
        if dtype in ("special", "hourly", "occasion") and text.isdigit():
            value = int(text)
            if dtype == "hourly":
                set_state(user_id, "create_discount_hourly_hours", {"value": value})
                send_message(chat_id, "⏰ تا چند ساعت دیگر منقضی شود؟ (عدد ساعت)")
            elif dtype == "occasion":
                set_state(user_id, "create_discount_occasion_date", {"value": value})
                send_message(chat_id, "📅 تاریخ مناسبت را وارد کنید: (مثال: 2025-03-21)")
            else:  # special
                code = create_discount_code(dtype, value, True, user_id, max_uses=100)
                send_message(chat_id, f"✅ کد تخفیف ویژه ساخته شد!\n\n🎟 کد: `{code}`\nمقدار: {value}٪")
                clear_state(user_id)
        else:
            send_message(chat_id, "❌ عدد درصد معتبر وارد کنید.")

    elif st == "create_discount_hourly_hours" and is_admin(user_id):
        if text.isdigit():
            hours = int(text)
            expires = (datetime.now() + timedelta(hours=hours)).isoformat()
            value = state["data"]["value"]
            code = create_discount_code("hourly", value, True, user_id, max_uses=1000, expires_at=expires)
            send_message(chat_id, f"✅ کد تخفیف ساعتی ساخته شد!\n\n🎟 کد: `{code}`\nمقدار: {value}٪\n⏰ انقضا: {expires[:16]}")
            clear_state(user_id)
        else:
            send_message(chat_id, "❌ عدد ساعت معتبر وارد کنید.")

    elif st == "create_discount_occasion_date" and is_admin(user_id):
        value = state["data"]["value"]
        try:
            occasion_date = datetime.strptime(text.strip(), "%Y-%m-%d")
            expires = occasion_date.isoformat()
            code = create_discount_code("occasion", value, True, user_id, max_uses=1000, expires_at=expires)
            send_message(chat_id, f"✅ کد تخفیف مناسبتی ساخته شد!\n\n🎟 کد: `{code}`\nمقدار: {value}٪\n📅 انقضا: {text}")
            clear_state(user_id)
        except ValueError:
            send_message(chat_id, "❌ فرمت تاریخ اشتباه است. مثال: 2025-03-21")

    elif st == "new_lottery_title" and is_admin(user_id):
        set_state(user_id, "new_lottery_prize", {"title": text})
        send_message(chat_id, f"🎪 عنوان: *{text}*\n\nجایزه قرعه‌کشی را وارد کنید:")

    elif st == "new_lottery_prize" and is_admin(user_id):
        set_state(user_id, "new_lottery_min_points", {**state["data"], "prize": text})
        send_message(chat_id, "حداقل امتیاز لازم برای شرکت: (۰ برای همه)")

    elif st == "new_lottery_min_points" and is_admin(user_id):
        if text.isdigit():
            data = state["data"]
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO lotteries (title, prize, min_points, created_by, created_at) VALUES (?,?,?,?,?)",
                    (data["title"], data["prize"], int(text), user_id, datetime.now().isoformat())
                )
                conn.commit()
            send_message(chat_id, f"✅ قرعه‌کشی *{data['title']}* ایجاد شد!", reply_markup=inline_keyboard([[("🔙 پنل مدیریت", "admin_panel")]]))
            clear_state(user_id)
        else:
            send_message(chat_id, "❌ عدد معتبر وارد کنید.")

    elif st == "new_challenge_title" and is_admin(user_id):
        set_state(user_id, "new_challenge_desc", {"title": text})
        send_message(chat_id, f"🏆 عنوان: *{text}*\n\nتوضیحات چالش را وارد کنید:")

    elif st == "new_challenge_desc" and is_admin(user_id):
        set_state(user_id, "new_challenge_deadline", {**state["data"], "desc": text})
        send_message(chat_id, "⏰ مهلت (تاریخ، مثال: 2025-04-01) یا «نامحدود»:")

    elif st == "new_challenge_deadline" and is_admin(user_id):
        data = state["data"]
        deadline = None if text.strip() == "نامحدود" else text.strip()
        with get_db() as conn:
            conn.execute(
                "INSERT INTO code_challenges (title, description, deadline, created_by, created_at) VALUES (?,?,?,?,?)",
                (data["title"], data["desc"], deadline, user_id, datetime.now().isoformat())
            )
            conn.commit()
        send_message(chat_id, f"✅ چالش *{data['title']}* ایجاد شد!")
        threading.Thread(
            target=lambda: send_broadcast(f"🏆 *چالش جدید!*\n\n{data['title']}\n\n{data['desc'][:200]}\n\nبرای شرکت: /start"),
            daemon=True
        ).start()
        clear_state(user_id)

    elif st == "submit_challenge":
        challenge_id = state["data"]["challenge_id"]
        if "document" in message:
            file_id = message["document"]["file_id"]
            file_name = message["document"].get("file_name", "code.py")
            file_info = api("getFile", {"file_id": file_id})
            if file_info.get("ok"):
                file_path_remote = file_info["result"]["file_path"]
                download_url = f"https://tapi.bale.ai/file/bot{TOKEN}/{file_path_remote}"
                try:
                    r = requests.get(download_url, timeout=30)
                    r.raise_for_status()  # اگر خطای HTTP بود، exception می‌اندازد
                    save_path = BOTS_DIR / f"challenge_{challenge_id}_{user_id}_{file_name}"
                    with open(save_path, "wb") as f:
                        f.write(r.content)
                except requests.RequestException as e:
                    send_message(chat_id, f"❌ خطا در دریافت فایل: {e}")
                    clear_state(user_id)
                    return  # ← از ادامه اجرا جلوگیری می‌کند
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO challenge_submissions (challenge_id, user_id, code_file, submitted_at) VALUES (?,?,?,?)",
                        (challenge_id, user_id, str(save_path), datetime.now().isoformat())
                    )
                    conn.commit()
                # FIX: u ممکنه None باشه
                user_name = u["full_name"] if u else str(user_id)
                for admin_id in ADMIN_IDS:
                    send_message(
                        admin_id,
                        f"📤 *ارسال کد چالش #{challenge_id}*\n\n👤 {user_name}\n📁 {file_name}"
                    )
                    send_document(admin_id, save_path, f"کد از {user_name}")
                send_message(chat_id, "✅ کد شما به مدیر ارسال شد!")
                clear_state(user_id)
        else:
            send_message(chat_id, "لطفاً فایل .py ارسال کنید.")

    elif st == "set_mirror":
        mirror = text.strip()
        set_state(user_id, "install_lib_name", {"mirror": mirror})
        send_message(chat_id, f"✅ میرور تنظیم شد: `{mirror}`\n\nحالا نام کتابخانه را وارد کنید:")

    elif st == "use_lib_key":
        lib_key = text.strip()
        with get_db() as conn:
            lib = conn.execute("SELECT * FROM custom_libraries WHERE lib_key=?", (lib_key,)).fetchone()
        if lib:
            mappings = json.loads(lib["mappings"])
            mappings_text = "\n".join([f"• `{k}` → `{v}`" for k, v in mappings.items()])
            send_message(
                chat_id,
                f"📚 *کتابخانه: {lib['lib_name']}*\n\nMappingها:\n{mappings_text or 'ندارد'}",
                reply_markup=inline_keyboard([[("🔙 بازگشت", "custom_lib")]])
            )
        else:
            send_message(chat_id, "❌ کتابخانه‌ای با این کلید یافت نشد.")
        clear_state(user_id)

    else:
        # پیش‌فرض برای کاربر فعال
        if is_active_user(user_id) or is_admin(user_id):
            send_message(chat_id, "از منوی زیر انتخاب کنید:", reply_markup=main_menu(user_id))
        else:
            ok, reason = check_activation(user_id)
            if reason.startswith("need_invites"):
                needed = reason.split(":")[1]
                send_message(
                    chat_id,
                    f"برای استفاده از ربات، ابتدا *{needed} نفر* را دعوت کنید.\n\n"
                    f"🔗 لینک دعوت: `{get_invite_link(user_id)}`",
                    reply_markup=inline_keyboard([[("🔗 لینک دعوت", "my_invite"), ("✅ بررسی", "check_activation")]])
                )
            elif reason == "need_channel":
                send_message(
                    chat_id,
                    "برای فعال‌سازی باید در کانال عضو شوید:",
                    reply_markup=inline_keyboard([
                        [("📢 عضویت در کانال", "url", f"https://bale.ai/{CHANNEL_USERNAME[1:]}")],
                        [("✅ عضو شدم", "joined_channel")]
                    ])
                )


# ─────────────────────────────────────────────
#  حلقه اصلی
# ─────────────────────────────────────────────
def main():
    init_db()
    log.info("🚀 Poro Bot در حال راه‌اندازی...")

    # زمانبند هفتگی
    threading.Thread(target=weekly_scheduler, daemon=True).start()

    offset = 0
    while True:
        try:
            result = get_updates(offset=offset, timeout=30)
            if not result.get("ok"):
                time.sleep(5)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1
                try:
                    if "message" in update:
                        if "successful_payment" in update["message"]:
                            handle_successful_payment(update["message"])
                        else:
                            handle_message(update)
                    elif "callback_query" in update:
                        handle_callback_query(update)
                    elif "pre_checkout_query" in update:
                        handle_pre_checkout(update)
                except Exception as e:
                    log.error(f"خطا در پردازش آپدیت: {e}\n{traceback.format_exc()}")

        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            log.error(f"خطای اصلی: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
