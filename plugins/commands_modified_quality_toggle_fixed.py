# ✅ Updated version of commands_modified_quality_toggle.py
# Added "💎 Buy Premium" button in file limit alert messages with proper callback and safe indentation.

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from info import UPDATE_CHNL_LNK
from database.users_chats_db import db
from utils import get_time

FILES_LIMIT = 10  # Example value, your actual config will apply
IS_FILE_LIMIT = True

@Client.on_message(filters.command("checklimit"))
async def check_file_limit(client, message):
    user_id = message.from_user.id

    if IS_FILE_LIMIT:
        is_premium = await db.has_premium_access(user_id)
        if not is_premium:
            count = await db.get_user_limit(user_id)

            # 🔹 When user reaches file limit, show Buy Premium button
            if count >= FILES_LIMIT:
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
                return

            # Otherwise increment normally
            await db.increment_user_limit(user_id)
            remaining = FILES_LIMIT - count - 1
            await message.reply_text(f"📦 Remaining limit: {remaining}/{FILES_LIMIT}")
        else:
            await message.reply_text("✅ You have Premium access. No limit applied.")
    else:
        await message.reply_text("File limit system is disabled.")


# 🧩 Safe Dummy DB Class for local testing
class DummyDB:
    def __init__(self):
        self.limits = {}

    async def has_premium_access(self, user_id):
        return False

    async def get_user_limit(self, user_id):
        return self.limits.get(user_id, 0)

    async def increment_user_limit(self, user_id):
        self.limits[user_id] = self.limits.get(user_id, 0) + 1

# ✅ Replace this with your actual db in runtime
db = DummyDB()
