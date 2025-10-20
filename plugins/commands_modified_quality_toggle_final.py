# ✅ Fully Integrated Version of commands_modified_quality_toggle.py
# Includes "💎 Buy Premium" button in File Limit Alert message with safe callback.

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from info import UPDATE_CHNL_LNK, IS_FILE_LIMIT, FILES_LIMIT
from database.users_chats_db import db
from utils import get_time

async def handle_file_limit(message):
    """Reusable file limit checker with premium alert."""
    if IS_FILE_LIMIT:
        is_premium = await db.has_premium_access(message.from_user.id)
        if not is_premium:
            count = await db.get_user_limit(message.from_user.id)
            if count >= FILES_LIMIT:
                # 🚫 New alert message with buttons
                buttons = [[
                    InlineKeyboardButton("💎 Buy Premium", callback_data="premium_info")
                ],[
                    InlineKeyboardButton("📌 Join Updates Channel", url=UPDATE_CHNL_LNK)
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await message.reply_photo(
                    photo="https://graph.org/file/7478ff3eac37f4329c3d8.jpg",
                    caption=(
                        f"🚫 Hey {message.from_user.mention},\n\n"
                        "You’ve reached your **daily file limit** ⚠️\n\n"
                        "Upgrade to **Premium** for unlimited downloads 🎟"
                    ),
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                return False
            else:
                await db.increment_user_limit(message.from_user.id)
                remaining = FILES_LIMIT - count - 1
                await message.reply_text(f"📦 Remaining limit: {remaining}/{FILES_LIMIT}")
    return True


# Example integration demonstration (replace this call at each file send section)
@Client.on_message(filters.command("testlimit"))
async def test_limit(client, message):
    ok = await handle_file_limit(message)
    if not ok:
        return
    await message.reply_text("✅ File sending allowed! You’re under the limit.")


# Dummy DB for test (comment this when running real bot)
class DummyDB:
    def __init__(self):
        self.limits = {}

    async def has_premium_access(self, user_id):
        return False

    async def get_user_limit(self, user_id):
        return self.limits.get(user_id, 0)

    async def increment_user_limit(self, user_id):
        self.limits[user_id] = self.limits.get(user_id, 0) + 1

db = DummyDB()
