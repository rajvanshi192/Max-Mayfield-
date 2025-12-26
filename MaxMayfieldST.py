import telebot
from telebot import types
import time
import random
import yt_dlp
import math
import re
from datetime import datetime, timedelta
from telebot.types import ChatPermissions

BOT_TOKEN = "8311020581:AAHBNHz1A9QiXXjhXDiIr4AQcxQMKRaBFP4"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

OWNER_ID = 8211318304  # change your id if needed

# ===========================
# 📌 USER MEMORY STORAGE
# ===========================

# Stores warnings per user
user_warnings = {}
daily_luck = {}
daily_mood = {}
daily_rankme = {}
quizzes = []      
quiz_add_state = {} 
quiz_drop_rate = {}          # chat_id -> message limit
group_message_count = {}     # chat_id -> current count
active_quiz = {}             # chat_id -> active quiz
user_xp = {}                 # user_id -> xp
user_quiz_stats = {}   # user_id -> {"attempts": 0, "correct": 0, "wrong": 0, "difficulty": {"Easy":0,...}}'
bot_admins = set()  # store user IDs of bot admins
quiz_edit_state = {}
# -----------------------------
# Global variables
# -----------------------------
BOT_VERSION = "v1.0"
START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - START_TIME)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

# -----------------------------
# /start command
# -----------------------------
@bot.message_handler(commands=['start'])
def start_command(message):
    if message.chat.type in ["group", "supergroup"]:
        bot.reply_to(
            message,
            "✨ʏᴏᴜ ᴄᴀɴ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴠɪᴛʏ ɪɴ (@MaxMayfieldSTBot) ᴅᴍ!!"
        )
        return

    user_mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
    text = (
        f"ʜᴇʏ {user_mention} 💠\n\n"
        "<b>ɪ ᴀᴍ ᴍᴀx ᴍᴀʏꜰɪᴇʟᴅ, ʏᴏᴜʀ ᴇꜰꜰɪᴄɪᴇɴᴛ ᴄᴏɴᴠᴇɴɪᴇɴᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ</b>, "
        "ᴅᴇꜱɪɢɴᴇᴅ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴀᴋᴇ ᴄᴏɴᴛʀᴏʟ ᴏꜰ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴇᴀꜱᴇ "
        "ᴜꜱɪɴɢ ᴛʜᴇ ᴘᴏᴡᴇʀꜰᴜʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴏꜰ ʙᴏᴛ..!!\n\n"
        "⚡ <b>Qᴜɪᴄᴋ ꜱᴛᴀʀᴛ:</b>\n"
        "✦︎ 🔄 /ꜱᴛᴀʀᴛ - ᴄᴀʟʟ ᴍᴀx / ᴍᴀxɪɴᴇ 😍\n"
        "✦︎ 📋 /ʜᴇʟᴘ - ᴠɪᴇᴡ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ\n"
        "✦︎ 🎯 /ᴀʟɪᴠᴇ - ᴄʜᴇᴄᴋ ɪ'ᴍ ᴀʟɪᴠᴇ ᴏʀ ɴᴏᴛ ✨\n\n"
        "<b>📚 ɴᴇᴇᴅ ʜᴇʟᴘ?</b>\n"
        "✨ᴄʟɪᴄᴋ ᴏɴ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ✨"
    )

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("📞𝑪𝒐𝒏𝒕𝒂𝒄𝒕 𝑶𝒘𝒏𝒆ʀ", url="https://t.me/OptusPerth100")
    markup.add(button)

    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://t.me/LogsOfBotHub/27",
        caption=text,
        reply_markup=markup,
        parse_mode="HTML"
    )

# -----------------------------
# /alive command
# -----------------------------
@bot.message_handler(commands=['alive'])
def alive_command(message):
    # Send temporary "fetching" message
    temp_msg = bot.send_message(message.chat.id, "ꜰᴇᴛᴄʜɪɴɢ ᴀʟɪᴠᴇ ɪɴꜰᴏ 💮")
    
    start_ping = time.time()
    time.sleep(0.5)  # simulate processing/ping measurement
    end_ping = time.time()
    ping_ms = int((end_ping - start_ping) * 1000)

    # Delete temporary message
    bot.delete_message(chat_id=message.chat.id, message_id=temp_msg.message_id)

    # Bot mention
    bot_mention = f"<a href='tg://user?id={bot.get_me().id}'>𝐌𝐚𝐱 𝐌𝐚𝐲𝐟𝐢𝐞𝐥𝐝</a>"

#    # Alive message
    text = (
    f"<b>『 {bot_mention} ɪꜱ ᴀʟɪᴠᴇ ʙᴀʙʏ 🐾🐾 』</b>\n\n"
    f"<b>✦︎ ᴜᴘᴛɪᴍᴇ:</b> <b>{get_uptime()}</b>\n"
    f"<b>✦︎ ᴠᴇʀꜱɪᴏɴ:</b> <b>{BOT_VERSION}</b>\n"
    f"<b>✦︎ ʙᴏᴛ ᴘɪɴɢ:</b> <b>{ping_ms} ms</b>\n\n"
    f"<b>📌 ɴᴏᴛᴇ:</b>\n"
    f"<b>• ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ ᴇꜰꜰᴇᴄᴛɪᴠᴇʟʏ!</b>\n"
    f"<b>• ᴜꜱᴇ /ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴍʏ ꜰᴇᴀᴛᴜʀᴇꜱ!!</b>"
)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ✨", url="https://t.me/RajSupportGroup"))
    markup.add(types.InlineKeyboardButton("ᴄʀɪᴄᴋᴇᴛ ᴄʜᴀɴɴᴇʟ✨", url="https://t.me/TheCricketLedger"))

    # Send alive photo with caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://t.me/LogsOfBotHub/28",
        caption=text,
        reply_markup=markup,
        parse_mode="HTML"
    )

@bot.message_handler(commands=['wish'])
def wish_command(message):
    # Split command and fetch wish text
    args = message.text.split(" ", 1)

    # If no wish written → Wrong usage
    if len(args) == 1:
        bot.reply_to(
            message,
            "<b>ᴘʟᴇᴀꜱᴇ ᴛᴇʟʟ ᴍᴇ ʏᴏᴜʀ ᴡɪꜱʜ ʙʏ ᴜꜱɪɴɢ ᴛʜᴇ ꜰᴏʀᴍᴀᴛ</b>\n"
            "<b>/ᴡɪꜱʜ『 ʏᴏᴜʀ ᴡɪꜱʜ 』</b>",
            parse_mode="HTML"
        )
        return

    # Extract wish text
    wish_text = args[1]

    # Random possibility %
    chance = random.randint(1, 100)

    # User mention
    user_first = message.from_user.first_name

    # Make final message
    text = (
        f"<b>❄️ 𝖧ᴇʏ! {user_first}, ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ</b>\n\n"
        f"<b>✨ ʏᴏᴜʀ ᴡɪꜱʜ :</b> <b>{wish_text}</b>\n"
        f"<b>🫧 ᴘᴏssɪʙɪʟɪᴛɪᴇs :</b> <b>{chance}%</b>"
    )

    # Reply with video + caption
    bot.reply_to(
        message,
        "ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ᴡɪꜱʜ ʀᴇꜱᴜʟᴛ...✨",
        parse_mode="HTML"
    )

    bot.send_video(
        chat_id=message.chat.id,
        video="https://t.me/LogsOfBotHub/29",
        caption=text,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )

@bot.message_handler(commands=['calculate'])
def calculate_cmd(message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) < 2:
            bot.reply_to(
                message,
                "<b>ᴘʟᴇᴀꜱᴇ ɢɪᴠᴇ ᴍᴇ ᴀɴʏ ᴍᴀᴛʜ ᴘʀᴏʙʟᴇᴍ ᴛᴏ ᴄᴀʟᴄᴜʟᴀᴛᴇ!\n\nᴜꜱᴀɢᴇ ➜ /ᴄᴀʟᴄᴜʟᴀᴛᴇ 2+2 • ꜱɪɴ(30) • ꜱǫʀᴛ(49)</b>",
                parse_mode="HTML",
            )
            return

        expr = parts[1].strip()

        # Allowed safe functions
        allowed = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expr, {"__builtins__": None}, allowed)

        bot.reply_to(
            message,
            f"<b>📘 ᴍᴀᴛʜ ᴄᴀʟᴄᴜʟᴀᴛᴇᴅ {message.from_user.first_name}!\n\n✨ ᴇxᴘʀᴇꜱꜱɪᴏɴ ➜ {expr}\n📏 ʀᴇꜱᴜʟᴛ ➜ {result}</b>",
            parse_mode="HTML",
        )

    except Exception:
        bot.reply_to(
            message,
            "<b>⚠️ ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇꜱꜱɪᴏɴ!\nᴛʀʏ ᴇxᴀᴍᴘʟᴇꜱ:\n• ꜱɪɴ(30)\n• 5*5\n• ꜱǫʀᴛ(49)\n• ʟᴏɢ(100)</b>",
            parse_mode="HTML",
        )
@bot.message_handler(commands=['clean'])
def clean_cmd(message):
    chat_id = message.chat.id

    try:
        parts = message.text.split()

        # -------------------------------
        # Case 1: /clean <number>
        # -------------------------------
        if len(parts) == 2 and parts[1].isdigit():
            count = int(parts[1])
            if count <= 0:
                raise ValueError

            deleted = 0
            for msg_id in range(message.message_id, message.message_id - count, -1):
                try:
                    bot.delete_message(chat_id, msg_id)
                    deleted += 1
                except:
                    pass

            bot.send_message(
                chat_id,
                f"<b>🧹 {deleted} ᴍᴇꜱꜱᴀɢᴇꜱ ᴄʟᴇᴀɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b>",
                reply_to_message_id=message.message_id,
                parse_mode="HTML"
            )
            return

        # -------------------------------
        # Case 2: Reply + /clean
        # -------------------------------
        if message.reply_to_message:
            start_msg = message.reply_to_message.message_id
            end_msg = message.message_id

            deleted = 0
            for msg_id in range(end_msg, start_msg, -1):
                try:
                    bot.delete_message(chat_id, msg_id)
                    deleted += 1
                except:
                    pass

            bot.send_message(
                chat_id,
                f"<b>🧹 {deleted} ᴍᴇꜱꜱᴀɢᴇꜱ ᴄʟᴇᴀɴᴇᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ!</b>",
                reply_to_message_id=start_msg,
                parse_mode="HTML"
            )
            return

        # -------------------------------
        # Case 3: Wrong Usage
        # -------------------------------
        bot.reply_to(
            message,
            "<b>⚠️ ᴘʀᴏᴘᴇʀ ᴜꜱᴀɢᴇ:\n\n• ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ + /ᴄʟᴇᴀɴ\n• /ᴄʟᴇᴀɴ 20</b>",
            parse_mode="HTML"
        )

    except Exception:
        bot.reply_to(
            message,
            "<b>⚠️ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴄʟᴇᴀɴɪɴɢ!</b>",
            parse_mode="HTML"
        )



# -------------------------
# helper: check if user is admin
# -------------------------
def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

# -------------------------
# helper: resolve target user id from reply / @username / id
# -------------------------
def resolve_target_id(message):
    # 1) If replied → target is replied user
    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    # 2) Else take second argument
    parts = message.text.split()
    if len(parts) < 2:
        return None

    target = parts[1].strip()

    # numeric id
    if target.isdigit():
        return int(target)

    # username (starts with @)
    if target.startswith("@"):
        try:
            chat = bot.get_chat(target)  # returns Chat object for username
            return chat.id
        except:
            return None

    return None


# -------------------------
# /mute
# Usage: reply to user with /mute OR /mute @username OR /mute user_id
# -------------------------
@bot.message_handler(commands=['mute'])
def cmd_mute(message):
    chat_id = message.chat.id
    admin_id = message.from_user.id

    if not is_admin(chat_id, admin_id):
        return bot.reply_to(message, "<b>✦ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴍᴜᴛᴇ ᴜꜱᴇʀꜱ ❗</b>", parse_mode="HTML")

    target_id = resolve_target_id(message)
    if not target_id:
        return bot.reply_to(message, "<b>✦ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴏʀ ᴘʀᴏᴠɪᴅᴇ @username ᴏʀ user_id</b>", parse_mode="HTML")

    try:
        bot.restrict_chat_member(
            chat_id,
            target_id,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
        bot.reply_to(
            message,
            f"<b>🔇 ᴜꜱᴇʀ ᴍᴜᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ 🔇\n\n✦ ᴛᴀʀɢᴇᴛ:</b> <b>{target_id}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")


# -------------------------
# /unmute
# Usage: reply to user with /unmute OR /unmute @username OR /unmute user_id
# -------------------------
@bot.message_handler(commands=['unmute'])
def cmd_unmute(message):
    chat_id = message.chat.id
    admin_id = message.from_user.id

    if not is_admin(chat_id, admin_id):
        return bot.reply_to(message, "<b>✦ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜɴᴍᴜᴛᴇ ❗</b>", parse_mode="HTML")

    target_id = resolve_target_id(message)
    if not target_id:
        return bot.reply_to(message, "<b>✦ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴏʀ ᴘʀᴏᴠɪᴅᴇ @username ᴏʀ user_id</b>", parse_mode="HTML")

    try:
        # restore common permissions
        bot.restrict_chat_member(
            chat_id,
            target_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        bot.reply_to(
            message,
            f"<b>🔊 ᴜꜱᴇʀ ᴜɴᴍᴜᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ 🔊\n\n✦ ᴛᴀʀɢᴇᴛ:</b> <b>{target_id}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")


# -------------------------
# /tmute
# Usage: reply to user with /tmute 10m OR /tmute @username 2h OR /tmute user_id 1d
# format for time: <number><s/m/h/d> (e.g. 30s, 10m, 2h, 1d)
# -------------------------
def parse_duration(token: str):
    m = re.match(r"^(\d+)([smhd])$", token)
    if not m:
        return None
    val = int(m.group(1))
    unit = m.group(2)
    if unit == "s":
        return timedelta(seconds=val)
    if unit == "m":
        return timedelta(minutes=val)
    if unit == "h":
        return timedelta(hours=val)
    if unit == "d":
        return timedelta(days=val)
    return None


@bot.message_handler(commands=['tmute'])
def cmd_tmute(message):
    chat_id = message.chat.id
    admin_id = message.from_user.id

    if not is_admin(chat_id, admin_id):
        return bot.reply_to(message, "<b>✦ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴛᴇᴍᴘ ᴍᴜᴛᴇ ❗</b>", parse_mode="HTML")

    parts = message.text.split()
    # If reply: parts may be like ['/tmute', '10m'] or ['/tmute', '@user', '10m']
    # Determine which token is duration
    duration_token = None
    if message.reply_to_message:
        # if reply, duration should be the next token
        if len(parts) >= 2:
            duration_token = parts[1]
        else:
            return bot.reply_to(message, "<b>✦ ᴜꜱᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ + /tmute 10m</b>", parse_mode="HTML")
    else:
        # not reply: expect /tmute target duration
        if len(parts) >= 3:
            duration_token = parts[2]
        else:
            return bot.reply_to(message, "<b>✦ ᴜꜱᴀɢᴇ: /tmute @user 10m  — ᴏʀ ʀᴇᴘʟʏ + /tmute 10m</b>", parse_mode="HTML")

    duration = parse_duration(duration_token)
    if not duration:
        return bot.reply_to(message, "<b>✦ ɪɴᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ! ᴜsᴇ: 30s / 10m / 2h / 1d</b>", parse_mode="HTML")

    # resolve target
    target_id = resolve_target_id(message)
    if not target_id:
        return bot.reply_to(message, "<b>✦ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛᴀʀɢᴇᴛ (reply / @username / id)</b>", parse_mode="HTML")

    until = datetime.utcnow() + duration

    try:
        bot.restrict_chat_member(
            chat_id,
            target_id,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            until_date=until
        )
        bot.reply_to(
            message,
            f"<b>⏳ ᴛᴇᴍᴘ-ᴍᴜᴛᴇ ᴀᴘᴘʟɪᴇᴅ ⏳\n\n✦ ᴛᴀʀɢᴇᴛ:</b> <b>{target_id}</b>\n<b>✦ ᴅᴜʀᴀᴛɪᴏɴ:</b> <b>{duration_token}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")
        
@bot.message_handler(commands=['ban'])
def cmd_ban(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ʙᴀɴ ᴍᴇᴍʙᴇʀꜱ ❗</b>", parse_mode="HTML")

    target = resolve_target_id(message)
    if not target:
        return bot.reply_to(message, "<b>✦ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴏʀ ɢɪᴠᴇ @username / id</b>", parse_mode="HTML")

    try:
        bot.ban_chat_member(chat_id, target)
        bot.reply_to(
            message,
            f"<b>🔥 ᴜꜱᴇʀ ʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ 🔥</b>\n"
            f"<b>✦ ᴜꜱᴇʀ:</b> <b>{target}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")
        
@bot.message_handler(commands=['unban'])
def cmd_unban(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜɴʙᴀɴ ᴜꜱᴇʀꜱ ❗</b>", parse_mode="HTML")

    target = resolve_target_id(message)
    if not target:
        return bot.reply_to(message, "<b>✦ ᴘʀᴏᴠɪᴅᴇ @username / id</b>", parse_mode="HTML")

    try:
        bot.unban_chat_member(chat_id, target)
        bot.reply_to(
            message,
            f"<b>✨ ᴜꜱᴇʀ ᴜɴʙᴀɴɴᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✨</b>\n"
            f"<b>✦ ᴜꜱᴇʀ:</b> <b>{target}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")
     
@bot.message_handler(commands=['kick'])
def cmd_kick(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ ❗</b>", parse_mode="HTML")

    target = resolve_target_id(message)
    if not target:
        return bot.reply_to(message, "<b>✦ ʀᴇᴘʟʏ ᴏʀ ɢɪᴠᴇ @username / id</b>", parse_mode="HTML")

    try:
        bot.ban_chat_member(chat_id, target)
        bot.unban_chat_member(chat_id, target)

        bot.reply_to(
            message,
            f"<b>💥 ᴜꜱᴇʀ ᴋɪᴄᴋᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ 💥</b>\n"
            f"<b>✦ ᴜꜱᴇʀ:</b> <b>{target}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"<b>✦ ᴇʀʀᴏʀ:</b> <b>{e}</b>", parse_mode="HTML")

@bot.message_handler(commands=['warn'])
def cmd_warn(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ ❗</b>", parse_mode="HTML")

    target = resolve_target_id(message)
    if not target:
        return bot.reply_to(message, "<b>✦ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴡᴀʀɴ</b>", parse_mode="HTML")

    user_warnings[target] = user_warnings.get(target, 0) + 1
    warns = user_warnings[target]

    if warns >= 3:
        bot.ban_chat_member(chat_id, target)
        user_warnings[target] = 0
        return bot.reply_to(
            message,
            f"<b>💀 ᴜꜱᴇʀ ʙᴀɴɴᴇᴅ — 3 ᴡᴀʀɴꜱ ʀᴇᴀᴄʜᴇᴅ 💀</b>\n"
            f"<b>✦ ᴜꜱᴇʀ:</b> <b>{target}</b>",
            parse_mode="HTML"
        )

    bot.reply_to(
        message,
        f"<b>⚠️ ᴡᴀʀɴɪɴɢ ɪꜱꜱᴜᴇᴅ ⚠️</b>\n"
        f"<b>✦ ᴜꜱᴇʀ:</b> <b>{target}</b>\n"
        f"<b>✦ ᴛᴏᴛᴀʟ ᴡᴀʀɴꜱ:</b> <b>{warns}/3</b>",
        parse_mode="HTML"
    )
    
@bot.message_handler(commands=['kickme'])
def cmd_kickme(message):
    chat_id = message.chat.id
    user = message.from_user.id

    try:
        bot.ban_chat_member(chat_id, user)
        bot.unban_chat_member(chat_id, user)
        bot.reply_to(message, "<b>👋 ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴋɪᴄᴋᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ!</b>", parse_mode="HTML")
    except:
        bot.reply_to(message, "<b>✦ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ʏᴏᴜ ❗</b>", parse_mode="HTML")
        
welcome_text = "<b>👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ!</b>"

@bot.message_handler(commands=['setwelcome'])
def cmd_setwelcome(message):
    global welcome_text
    admin = message.from_user.id
    chat_id = message.chat.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ ❗</b>", parse_mode="HTML")

    txt = message.text.replace("/setwelcome", "").strip()
    if not txt:
        return bot.reply_to(message, "<b>✦ ᴀᴅᴅ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ</b>", parse_mode="HTML")

    welcome_text = txt
    bot.reply_to(message, "<b>✨ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴜᴘᴅᴀᴛᴇᴅ ✨</b>", parse_mode="HTML")


@bot.message_handler(commands=['welcome'])
def cmd_welcome(message):
    bot.reply_to(message, welcome_text, parse_mode="HTML")

@bot.message_handler(commands=['lock'])
def cmd_lock(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ ❗</b>", parse_mode="HTML")

    perms = ChatPermissions(
        can_send_messages=False
    )
    bot.set_chat_permissions(chat_id, perms)

    bot.reply_to(message, "<b>🔒 ᴄʜᴀᴛ ʟᴏᴄᴋᴇᴅ</b>", parse_mode="HTML")


@bot.message_handler(commands=['unlock'])
def cmd_unlock(message):
    chat_id = message.chat.id
    admin = message.from_user.id

    if not is_admin(chat_id, admin):
        return bot.reply_to(message, "<b>✦ ᴀᴅᴍɪɴꜱ ᴏɴʟʏ ❗</b>", parse_mode="HTML")

    perms = ChatPermissions(
        can_send_messages=True
    )
    bot.set_chat_permissions(chat_id, perms)

    bot.reply_to(message, "<b>🔓 ᴄʜᴀᴛ ᴜɴʟᴏᴄᴋᴇᴅ</b>", parse_mode="HTML")
    
@bot.message_handler(commands=['tagall'])
def tag_all(message):
    chat_id = message.chat.id

    # reply to user message
    reply_id = message.message_id

    # Fetch all members
    try:
        members = bot.get_chat_administrators(chat_id)
        all_members = bot.get_chat(chat_id)
    except Exception as e:
        bot.reply_to(message, "<b>⚠️ ᴇʀʀᴏʀ ꜰᴇᴛᴄʜɪɴɢ ᴍᴇᴍʙᴇʀꜱ!</b>")
        return

    # Get full list of users (bot API limitation → we use get_chat_members_count)
    total_members = bot.get_chat_members_count(chat_id)

    # Tag list (safe method — tag admins + sender + extra text)
    text = "<b>✨ ᴛᴀɢɢɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ✨</b>\n\n"

    # Telegram does NOT allow fetching all usernames, so we tag via loop from admin & sender  
    admins = bot.get_chat_administrators(chat_id)

    for admin in admins:
        user = admin.user
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        text += f"{mention} "

    # Add sender
    sender = message.from_user
    text += f"<a href=\"tg://user?id={sender.id}\">{sender.first_name}</a> "

    # Add note
    text += "\n\n<b>ᴍᴏʀᴇ ᴍᴇᴍʙᴇʀꜱ ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴛᴀɢɢᴇᴅ ᴅᴜᴇ ᴛᴏ ᴛɢ ʟɪᴍɪᴛꜱ.</b>"

    bot.send_message(
        chat_id,
        text,
        parse_mode="HTML",
        reply_to_message_id=reply_id
    )
   
@bot.message_handler(commands=['admintag'])
def admin_tag(message):
    chat_id = message.chat.id
    reply_id = message.message_id

    try:
        admins = bot.get_chat_administrators(chat_id)
    except Exception as e:
        bot.reply_to(message, "<b>⚠️ ᴇʀʀᴏʀ ꜰᴇᴛᴄʜɪɴɢ ᴀᴅᴍɪɴꜱ!</b>")
        return

    if not admins:
        bot.reply_to(message, "<b>⚠️ ɴᴏ ᴀᴅᴍɪɴꜱ ꜰᴏᴜɴᴅ!</b>")
        return

    text = "<b>✨ ᴛᴀɢɢɪɴɢ ᴀʟʟ ᴀᴅᴍɪɴꜱ ✨</b>\n\n"
    for admin in admins:
        user = admin.user
        mention = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
        text += f"{mention} "

    bot.send_message(
        chat_id,
        text,
        parse_mode="HTML",
        reply_to_message_id=reply_id
    )

# Help pages content
HELP_PAGES = [
    {
        "title": "𝘽𝙖𝙨𝙞𝙘 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨",
        "text": """▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝘽𝙖𝙨𝙞𝙘 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱

1) <b>ꜱᴛᴀʀᴛ</b> - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✨
2) <b>ʜᴇʟᴘ</b> - ᴠɪᴇᴡ ᴀʟʟ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅꜱ 🚨
3) <b>ᴀʟɪᴠᴇ</b> - ᴄʜᴇᴄᴋ ɪꜰ ɪ ᴀᴍ ᴀʟɪᴠᴇ ᴏʀ ɴᴏᴛ 💠

▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝙀𝙣𝙙 𝙊𝙛 𝙏𝙝𝙚 𝙇𝙞𝙨𝙩</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱"""
    },
    {
        "title": "𝙁𝙪𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨",
        "text": """▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝙁𝙪𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱

1) <b>ᴡɪꜱʜ</b> - ᴡʀɪᴛᴇ ʏᴏᴜʀ ᴡɪꜱʜ ✍🏻
2) <b>ʀᴀɴᴋᴍᴇ</b> - ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴛᴏᴅᴀʏ ʀᴀɴᴋ ᴄᴀʀᴅ 💠
3) <b>ᴄᴏᴜᴘʟᴇ</b> - ᴇʟᴇᴄᴛ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ
4) <b>ᴡᴀɪꜰᴜ</b> - ɢᴇᴛ ʀᴀɴᴅᴏᴍʟʏ ᴡᴀɪꜰᴜ ᴏꜰ ᴛʜᴇ ᴅᴀʏ ❤️‍🩹
5) <b>ᴍᴏᴏᴅ</b> - ᴄʜᴇᴄᴋ ᴛᴏᴅᴀʏ'ꜱ ᴍᴏᴏᴅ 📌
6) <b>ʟᴜᴄᴋ</b> - ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴛᴏᴅᴀʏ ʟᴜᴄᴋ ʟᴇᴠᴇʟ

▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝙀𝙣𝙙 𝙊𝙛 𝙏𝙝𝙚 𝙇𝙞𝙨𝙩</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱"""
    },
    {
        "title": "𝐆𝐫𝐨𝐮𝐩 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬",
        "text": """▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝐆𝐫𝐨𝐮𝐩 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱

1) <b>Mute</b> - Mute Anyone
2) <b>Unmute</b> - Unmute The User
3) <b>Tmute</b> - Timer Mute Any User
4) <b>Ban</b> - Ban Any User
5) <b>Unban</b> - Unban The Banned User
6) <b>Kick</b> - Kick The User
7) <b>Promote</b> - Promote Anyone To Admin
8) <b>Demote</b> - Demote Admins

▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
<b>𝐄𝐧𝐝 𝐨𝐟 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭</b>
▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱"""
    }
]

# /help command with Close button
@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id

    # Inline buttons for first page
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Next ➡️", callback_data="help_1"),
        types.InlineKeyboardButton("❌ Close", callback_data="help_close")
    )

    bot.send_message(chat_id, HELP_PAGES[0]["text"], parse_mode="HTML", reply_to_message_id=message.message_id, reply_markup=markup)


# Callback query for pagination
@bot.callback_query_handler(func=lambda call: call.data.startswith("help_"))
def help_pagination(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "help_close":
        bot.delete_message(chat_id, msg_id)
        return

    index = int(call.data.split("_")[1])

    markup = types.InlineKeyboardMarkup()
    if index == 0:
        markup.row(
            types.InlineKeyboardButton("Next ➡️", callback_data=f"help_{index+1}"),
            types.InlineKeyboardButton("❌ Close", callback_data="help_close")
        )
    elif index == len(HELP_PAGES) - 1:
        markup.row(
            types.InlineKeyboardButton("⬅️ Previous", callback_data=f"help_{index-1}"),
            types.InlineKeyboardButton("❌ Close", callback_data="help_close")
        )
    else:
        markup.row(
            types.InlineKeyboardButton("⬅️ Previous", callback_data=f"help_{index-1}"),
            types.InlineKeyboardButton("Next ➡️", callback_data=f"help_{index+1}"),
            types.InlineKeyboardButton("❌ Close", callback_data="help_close")
        )

    bot.edit_message_text(chat_id=chat_id, message_id=msg_id,
                          text=HELP_PAGES[index]["text"],
                          parse_mode="HTML",
                          reply_markup=markup)

@bot.message_handler(commands=['luck'])
def luck(message):
    # IST = UTC + 5:30
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today = ist_now.date()
    user_id = message.from_user.id

    # Reset if date changed
    if user_id in daily_luck and daily_luck[user_id]["date"] != today:
        del daily_luck[user_id]

    # Generate luck if not exists
    if user_id not in daily_luck:
        luck_percent = random.randint(1, 100)
        daily_luck[user_id] = {
            "luck": luck_percent,
            "date": today
        }
    else:
        luck_percent = daily_luck[user_id]["luck"]

    user_tag = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"

    text = (
        f"🍀 <b>{user_tag}'ꜱ ᴛᴏᴅᴀʏ'ꜱ ʟᴜᴄᴋ</b> 🍀\n"
        f"╭──────────────\n"
        f"┊•➢ <b>ʟᴜᴄᴋ ʟᴇᴠᴇʟ:</b> {luck_percent}% ✨\n"
        f"┊•➢ <b>ᴅᴀᴛᴇ:</b> {today.strftime('%d %b %Y')} \n"
        f"╰───•➢♡"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )
 
@bot.message_handler(commands=['mood'])
def mood(message):
    # IST = UTC + 5:30
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today = ist_now.date()
    user_id = message.from_user.id

    # Reset if date changed
    if user_id in daily_mood and daily_mood[user_id]["date"] != today:
        del daily_mood[user_id]

    # Mood list
    moods = [
        "😄 ʜᴀᴘᴘʏ",
        "🥰 ʟᴏᴠɪɴɢ",
        "😌 ᴄᴀʟᴍ",
        "😎 ᴄᴏᴏʟ",
        "🤩 ᴇɴᴇʀɢᴇᴛɪᴄ",
        "😴 ꜱʟᴇᴇᴘʏ",
        "😤 ᴀɴɴᴏʏᴇᴅ",
        "🥺 ᴇᴍᴏᴛɪᴏɴᴀʟ",
        "😐 ɴᴏʀᴍᴀʟ",
        "🔥 ꜰɪʀᴇ"
    ]

    # Generate mood if not exists
    if user_id not in daily_mood:
        today_mood = random.choice(moods)
        daily_mood[user_id] = {
            "mood": today_mood,
            "date": today
        }
    else:
        today_mood = daily_mood[user_id]["mood"]

    user_tag = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"

    text = (
        f"🧠 <b>{user_tag}'ꜱ ᴛᴏᴅᴀʏ'ꜱ ᴍᴏᴏᴅ</b> 🧠\n"
        f"╭──────────────\n"
        f"┊•➢ <b>ᴍᴏᴏᴅ:</b> {today_mood}\n"
        f"┊•➢ <b>ᴅᴀᴛᴇ:</b> {today.strftime('%d %b %Y')} 🇮🇳\n"
        f"╰───•➢♡"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )
    
@bot.message_handler(commands=['rankme'])
def rankme(message):
    # IST time (UTC + 5:30) — no pytz
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today = ist_now.date()
    user_id = message.from_user.id

    # Reset daily data
    if user_id in daily_rankme and daily_rankme[user_id]["date"] != today:
        del daily_rankme[user_id]

    # Generate new rank card if not exists
    if user_id not in daily_rankme:
        looks = random.randint(60, 100)
        intelligence = random.randint(60, 100)
        personality = random.randint(60, 100)
        vibe = random.randint(70, 100)

        daily_rankme[user_id] = {
            "looks": looks,
            "intelligence": intelligence,
            "personality": personality,
            "vibe": vibe,
            "date": today
        }

    data = daily_rankme[user_id]

    user_name = message.from_user.first_name.upper()

    text = (
        f"💠 <b>ʀᴀɴᴋ ᴄᴀʀᴅ ꜰᴏʀ {user_name}✨</b> 💠\n\n"
        f"😎 <b>ʟᴏᴏᴋꜱ:</b> {data['looks']}/100\n"
        f"🧠 <b>ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ:</b> {data['intelligence']}/100\n"
        f"💬 <b>ᴘᴇʀꜱᴏɴᴀʟɪᴛʏ:</b> {data['personality']}/100\n"
        f"🔥 <b>ᴏᴠᴇʀᴀʟʟ ᴠɪʙᴇ:</b> {data['vibe']}/100 💫\n\n"
        f"🌙 <b>ᴜᴘᴅᴀᴛᴇꜱ ᴇᴠᴇʀʏ 24ʜ</b>"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )
 
@bot.message_handler(commands=['check'])
def check_quiz(message):
    # Owner only
    if message.from_user.id != OWNER_ID:
        bot.reply_to(
            message,
            "<b>❌ ᴏɴʟʏ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ</b>",
            parse_mode="HTML"
        )
        return

    args = message.text.split()

    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(
            message,
            "<b>⚠️ ᴜꜱᴀɢᴇ:</b>\n"
            "<code>/check 1</code>",
            parse_mode="HTML"
        )
        return

    quiz_id = int(args[1])

    # Find quiz
    quiz = next((q for q in quizzes if q["id"] == quiz_id), None)

    if not quiz:
        bot.reply_to(
            message,
            "<b>❌ ǫᴜɪᴢ ɴᴏᴛ ꜰᴏᴜɴᴅ</b>",
            parse_mode="HTML"
        )
        return

    # Prepare message
    text = (
        f"🧠 <b>ǫᴜɪᴢ ᴅᴇᴛᴀɪʟꜱ</b>\n"
        f"╭──────────────\n"
        f"🆔 <b>ǫᴜɪᴢ ɪᴅ:</b> {quiz['id']}\n\n"
        f"❓ <b>ǫᴜᴇꜱᴛɪᴏɴ:</b>\n"
        f"{quiz['question']}\n\n"
        f"① {quiz['options'][0]}\n"
        f"② {quiz['options'][1]}\n"
        f"③ {quiz['options'][2]}\n"
        f"④ {quiz['options'][3]}\n\n"
        f"⚙️ <b>ᴅɪꜰꜰɪᴄᴜʟᴛʏ:</b> {quiz['difficulty']}\n\n"
        f"🥇 <b>1ꜱᴛ:</b> {quiz['xp'][1]} XP\n"
        f"🥈 <b>2ɴᴅ:</b> {quiz['xp'][2]} XP\n"
        f"🥉 <b>3ʀᴅ:</b> {quiz['xp'][3]} XP\n"
        f"╰──────────────"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )

# =====================================================
# 🛠 /QUIZDRATE → Set after how many messages quiz drops (Owner only)
# =====================================================
@bot.message_handler(commands=['quizdrate'])
def set_quiz_rate(message):
    user_id = message.from_user.id

    # Only bot owner can set
    if user_id != OWNER_ID:
        return bot.reply_to(message, "<b>❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴛʜᴇ ᴏᴡɴᴇʀ</b>", parse_mode="HTML")

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        return bot.reply_to(
            message,
            "<b>❌ ᴜꜱᴀɢᴇ:</b> /quizdrate <number_of_messages>",
            parse_mode="HTML"
        )

    rate = int(args[1])
    quiz_drop_rate[message.chat.id] = rate

    bot.reply_to(
        message,
        f"<b>✅ ǫᴜɪᴢ ᴅʀᴏᴘ ʀᴀᴛᴇ ꜱᴇᴛ:</b> {rate} ᴍᴇꜱꜱᴀɢᴇꜱ",
        parse_mode="HTML"
    )

# =====================================================
# 👀 /VIEWQUIZRATE → View current quiz drop rate
# =====================================================
@bot.message_handler(commands=['viewquizrate'])
def view_quiz_rate(message):
    rate = quiz_drop_rate.get(message.chat.id)
    if not rate:
        return bot.reply_to(
            message,
            "<b>⚠️ ɴᴏ ǫᴜɪᴢ ᴅʀᴏᴘ ʀᴀᴛᴇ ꜱᴇᴛ ʏᴇᴛ</b>",
            parse_mode="HTML"
        )

    bot.reply_to(
        message,
        f"<b>👀 ᴄᴜʀʀᴇɴᴛ ǫᴜɪᴢ ᴅʀᴏᴘ ʀᴀᴛᴇ:</b> Every {rate} ᴍᴇꜱꜱᴀɢᴇꜱ",
        parse_mode="HTML"
    )
    
 # =====================================================
# 📊 /MYXP → View your total XP
# =====================================================
@bot.message_handler(commands=['myxp'])
def my_xp(message):
    user_id = message.from_user.id
    xp = user_xp.get(user_id, 0)  # Default to 0 if not yet earned

    bot.reply_to(
        message,
        f"💠 <b>ʏᴏᴜʀ ᴛᴏᴛᴀʟ ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴘᴏɪɴᴛꜱ (XP)</b> 💠\n\n"
        f"✨ <b>ᴛᴏᴛᴀʟ XP:</b> {xp} 💫",
        parse_mode="HTML"
    )
 
# =====================================================
# 📊 /QUIZSTATS → View detailed quiz stats
# =====================================================
@bot.message_handler(commands=['quizstats'])
def quiz_stats(message):
    user_id = message.from_user.id

    # Initialize if no stats
    stats = user_quiz_stats.get(user_id, {
        "attempts": 0,
        "correct": 0,
        "wrong": 0,
        "difficulty": {diff: 0 for diff in XP_TABLE.keys()}
    })
    total_xp = user_xp.get(user_id, 0)

    # Accuracy
    if stats["attempts"] > 0:
        accuracy = (stats["correct"] / stats["attempts"]) * 100
    else:
        accuracy = 0

    # Global XP ranking
    sorted_users = sorted(user_xp.items(), key=lambda x: x[1], reverse=True)
    position = next((i+1 for i, (uid, xp) in enumerate(sorted_users) if uid == user_id), "-")

    # Prepare stats text
    text = (
        f"💠 <b>ǫᴜɪᴢ ꜱᴛᴀᴛꜱ ꜰᴏʀ {message.from_user.first_name} 💠</b>\n\n"
        f"📝 <b>ᴛᴏᴛᴀʟ ᴀᴛᴛᴇᴍᴘᴛꜱ:</b> {stats['attempts']}\n"
        f"✅ <b>ᴄᴏʀʀᴇᴄᴛ:</b> {stats['correct']}\n"
        f"❌ <b>ᴡʀᴏɴɢ:</b> {stats['wrong']}\n"
        f"🎯 <b>ᴀᴄᴄᴜʀᴀᴄʏ:</b> {accuracy:.2f}%\n\n"
        f"⚙️ <b>ᴄᴏʀʀᴇᴄᴛ ʙʏ ᴅɪꜰꜰɪᴄᴜʟᴛʏ:</b>\n"
    )
    for diff, val in stats["difficulty"].items():
        text += f"• {diff}: {val}\n"

    text += (
        f"\n✨ <b>ᴛᴏᴛᴀʟ XP:</b> {total_xp}\n"
        f"🏆 <b>ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ ᴘᴏꜱɪᴛɪᴏɴ:</b> {position}"
    )

    bot.reply_to(
        message,
        text,
        parse_mode="HTML"
    )
    
# =====================================================
# 🏆 /QUIZTOP → Top 10 users by correct answers
# =====================================================
@bot.message_handler(commands=['quiztop'])
def quiz_top(message):
    # Sort users by correct answers, descending
    sorted_users = sorted(
        user_quiz_stats.items(),
        key=lambda x: x[1].get("correct", 0),
        reverse=True
    )

    # Take top 10
    top_10 = sorted_users[:10]

    if not top_10:
        bot.reply_to(
            message,
            "<b>⚠️ No quiz data available yet!</b>",
            parse_mode="HTML"
        )
        return

    text = "💠 <b>ǫᴜɪᴢ ᴛᴏᴘ 10 ᴜꜱᴇʀꜱ 💠</b>\n\n"
    for i, (user_id, stats) in enumerate(top_10, start=1):
        correct = stats.get("correct", 0)
        text += f"🏅 <b>{i}.</b> {correct} ✅\n"

    bot.reply_to(
        message,
        text,
        parse_mode="HTML"
    )
    
@bot.message_handler(commands=['makeadmin'])
def make_admin(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b>❌ ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ!</b>", parse_mode="HTML")
        return

    try:
        target_user = message.reply_to_message.from_user
    except:
        bot.reply_to(message, "<b>❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ!</b>", parse_mode="HTML")
        return

    if target_user.id in bot_admins:
        bot.reply_to(message, f"<b>⚠️ {target_user.first_name} ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ!</b>", parse_mode="HTML")
        return

    bot_admins.add(target_user.id)
    bot.reply_to(message, f"💠 <b>{target_user.first_name} ʜᴀꜱ ʙᴇᴇɴ ᴘʀᴏᴍᴏᴛᴇᴅ ᴛᴏ ᴀᴅᴍɪɴ!</b>", parse_mode="HTML")
    
@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b>❌ ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ!</b>", parse_mode="HTML")
        return

    try:
        target_user = message.reply_to_message.from_user
    except:
        bot.reply_to(message, "<b>❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ'ꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴛʜᴇᴍ!</b>", parse_mode="HTML")
        return

    if target_user.id not in bot_admins:
        bot.reply_to(message, f"<b>⚠️ {target_user.first_name} ɪꜱ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!</b>", parse_mode="HTML")
        return

    bot_admins.remove(target_user.id)
    bot.reply_to(message, f"💠 <b>{target_user.first_name} ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴅᴍɪɴ!</b>", parse_mode="HTML")
# ================== QUIZ SYSTEM STORAGE ==================
quiz_counter = 0           # ✅ Quiz ID counter
quizzes = []               # ✅ List of all quizzes
quiz_add_state = {}        # ✅ Temp storage for adding quizzes
active_quiz = {}           # ✅ Current active quiz in group
group_message_count = {}   # ✅ Message counter per group
quiz_drop_rate = {}        # ✅ Messages after which quiz drops
user_xp = {}               # ✅ XP per user

# ================== XP TABLE ==================
XP_TABLE = {
    "Easy": {1: 15, 2: 10, 3: 5},
    "Medium": {1: 20, 2: 15, 3: 10},
    "Hard": {1: 30, 2: 20, 3: 10},
    "Expert": {1: 50, 2: 30, 3: 20},
    "Legendary": {1: 100, 2: 70, 3: 50}
}

DIFFICULTY_WEIGHTS = {
    "Easy": 50,
    "Medium": 30,
    "Hard": 15,
    "Expert": 4,
    "Legendary": 1
}

# ================== /ADDQUIZ COMMAND (Owner + Admins) ==================
@bot.message_handler(commands=['addquiz'])
def addquiz(message):
    user_id = message.from_user.id

    # ✅ Only Owner or Admins
    if user_id != OWNER_ID and user_id not in bot_admins:
        bot.reply_to(
            message,
            "<b>❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ!</b>",
            parse_mode="HTML"
        )
        return

    quiz_add_state[user_id] = {
        "step": "question",
        "data": {}
    }

    bot.send_message(
        message.chat.id,
        "<b>🧠 ǫᴜɪᴢ ᴀᴅᴅɪɴɢ ꜱᴛᴀʀᴛᴇᴅ</b>\n\n"
        "✦ ꜱᴇɴᴅ ᴛʜᴇ <b>ǫᴜᴇꜱᴛɪᴏɴ</b> 📝",
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )

# ================== QUIZ ADD FLOW ==================
@bot.message_handler(func=lambda m: m.from_user.id in quiz_add_state)
def quiz_add_flow(message):
    global quiz_counter
    user_id = message.from_user.id

    if user_id not in quiz_add_state:
        return

    state = quiz_add_state[user_id]
    step = state["step"]

    # STEP 1 — QUESTION
    if step == "question":
        state["data"]["question"] = message.text
        state["step"] = "opt1"
        bot.send_message(message.chat.id, "<b>① ꜱᴇɴᴅ ᴏᴘᴛɪᴏɴ 1</b>", parse_mode="HTML")
        return

    # STEP 2 — OPTION 1
    if step == "opt1":
        state["data"]["opt1"] = message.text
        state["step"] = "opt2"
        bot.send_message(message.chat.id, "<b>② ꜱᴇɴᴅ ᴏᴘᴛɪᴏɴ 2</b>", parse_mode="HTML")
        return

    # STEP 3 — OPTION 2
    if step == "opt2":
        state["data"]["opt2"] = message.text
        state["step"] = "opt3"
        bot.send_message(message.chat.id, "<b>③ ꜱᴇɴᴅ ᴏᴘᴛɪᴏɴ 3</b>", parse_mode="HTML")
        return

    # STEP 4 — OPTION 3
    if step == "opt3":
        state["data"]["opt3"] = message.text
        state["step"] = "opt4"
        bot.send_message(message.chat.id, "<b>④ ꜱᴇɴᴅ ᴏᴘᴛɪᴏɴ 4</b>", parse_mode="HTML")
        return

    # STEP 5 — OPTION 4
    if step == "opt4":
        state["data"]["opt4"] = message.text
        state["step"] = "difficulty"
        bot.send_message(
            message.chat.id,
            "<b>⚙️ ꜱᴇʟᴇᴄᴛ ᴅɪꜰꜰɪᴄᴜʟᴛʏ</b>\n\n"
            "🟢 Easy\n"
            "🟡 Medium\n"
            "🔴 Hard\n"
            "🔵 Expert\n"
            "🟣 Legendary\n\n"
            "✦ ꜱᴇɴᴅ ᴅɪꜰꜰɪᴄᴜʟᴛʏ ɴᴀᴍᴇ",
            parse_mode="HTML"
        )
        return

    # STEP 6 — DIFFICULTY
    if step == "difficulty":
        diff = message.text.capitalize()
        if diff not in XP_TABLE:
            bot.send_message(message.chat.id,
                "<b>❌ ɪɴᴠᴀʟɪᴅ ᴅɪꜰꜰɪᴄᴜʟᴛʏ</b>\nUse: Easy / Medium / Hard / Expert / Legendary",
                parse_mode="HTML"
            )
            return

        state["data"]["difficulty"] = diff
        state["step"] = "answer"
        bot.send_message(message.chat.id,
            "<b>✔ Send the number of the correct answer (1-4)</b>", parse_mode="HTML")
        return

    # STEP 7 — CORRECT ANSWER
    if step == "answer":
        try:
            correct_index = int(message.text) - 1
            if correct_index not in [0,1,2,3]:
                raise ValueError
        except:
            bot.send_message(message.chat.id, "❌ Invalid. Send 1, 2, 3, or 4.", parse_mode="HTML")
            return

        state["data"]["answer"] = correct_index
        quiz_counter += 1

        quiz = {
            "id": quiz_counter,
            "question": state["data"]["question"],
            "options": [
                state["data"]["opt1"],
                state["data"]["opt2"],
                state["data"]["opt3"],
                state["data"]["opt4"]
            ],
            "difficulty": state["data"]["difficulty"],
            "xp": XP_TABLE[state["data"]["difficulty"]],
            "answer": state["data"]["answer"]
        }

        quizzes.append(quiz)
        del quiz_add_state[user_id]

        bot.send_message(
            message.chat.id,
            f"<b>✅ ǫᴜɪᴢ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ</b>\n"
            f"🆔 <b>ID:</b> {quiz_counter}\n"
            f"⚙ <b>Difficulty:</b> {quiz['difficulty']}\n"
            f"🥇 1st: {XP_TABLE[quiz['difficulty']][1]} XP\n"
            f"🥈 2nd: {XP_TABLE[quiz['difficulty']][2]} XP\n"
            f"🥉 3rd: {XP_TABLE[quiz['difficulty']][3]} XP",
            parse_mode="HTML"
        )
        
# ================== /EDITQUIZ COMMAND ==================
@bot.message_handler(commands=['editquiz'])
def editquiz(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # ✅ Only Owner or Admins
    if user_id != OWNER_ID and user_id not in bot_admins:
        bot.reply_to(
            message,
            "<b>❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ!</b>",
            parse_mode="HTML"
        )
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(
            message,
            "<b>❌ ᴜꜱᴀɢᴇ:</b> /editquiz <b>quiz_ID</b>",
            parse_mode="HTML"
        )
        return

    try:
        quiz_id = int(args[1])
    except:
        bot.reply_to(
            message,
            "<b>❌ ɪɴᴠᴀʟɪᴅ ǫᴜɪᴢ ɪᴅ</b>",
            parse_mode="HTML"
        )
        return

    # Find quiz
    quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
    if not quiz:
        bot.reply_to(
            message,
            f"<b>❌ ɴᴏ ǫᴜɪᴢ ᴡɪᴛʜ ɪᴅ {quiz_id}</b>",
            parse_mode="HTML"
        )
        return

    # Set edit state
    quiz_edit_state[user_id] = {
        "step": "question",
        "quiz_id": quiz_id,
        "data": {}
    }

    bot.reply_to(
        message,
        f"<b>✏️ ᴇᴅɪᴛɪɴɢ ǫᴜɪᴢ ᴡɪᴛʜ ɪᴅ {quiz_id}</b>\n\n"
        "✦ ꜱᴇɴᴅ ɴᴇᴡ <b>ǫᴜᴇꜱᴛɪᴏɴ</b> 📝",
        parse_mode="HTML"
    )

# ================== QUIZ EDIT FLOW ==================
@bot.message_handler(func=lambda m: m.from_user.id in quiz_edit_state)
def quiz_edit_flow(message):
    user_id = message.from_user.id
    state = quiz_edit_state[user_id]
    step = state["step"]
    quiz_id = state["quiz_id"]

    quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
    if not quiz:
        del quiz_edit_state[user_id]
        bot.reply_to(message, "<b>❌ ǫᴜɪᴢ ɴᴏ ʟᴏɴɢᴇʀ ᴇxɪꜱᴛꜱ</b>", parse_mode="HTML")
        return

    # STEP 1 — QUESTION
    if step == "question":
        state["data"]["question"] = message.text
        state["step"] = "opt1"
        bot.reply_to(message, "<b>① ꜱᴇɴᴅ ɴᴇᴡ ᴏᴘᴛɪᴏɴ 1</b>", parse_mode="HTML")
        return

    # STEP 2 — OPTION 1
    if step == "opt1":
        state["data"]["opt1"] = message.text
        state["step"] = "opt2"
        bot.reply_to(message, "<b>② ꜱᴇɴᴅ ɴᴇᴡ ᴏᴘᴛɪᴏɴ 2</b>", parse_mode="HTML")
        return

    # STEP 3 — OPTION 2
    if step == "opt2":
        state["data"]["opt2"] = message.text
        state["step"] = "opt3"
        bot.reply_to(message, "<b>③ ꜱᴇɴᴅ ɴᴇᴡ ᴏᴘᴛɪᴏɴ 3</b>", parse_mode="HTML")
        return

    # STEP 4 — OPTION 3
    if step == "opt3":
        state["data"]["opt3"] = message.text
        state["step"] = "opt4"
        bot.reply_to(message, "<b>④ ꜱᴇɴᴅ ɴᴇᴡ ᴏᴘᴛɪᴏɴ 4</b>", parse_mode="HTML")
        return

    # STEP 5 — OPTION 4
    if step == "opt4":
        state["data"]["opt4"] = message.text
        state["step"] = "difficulty"
        bot.reply_to(
            message,
            "<b>⚙️ ꜱᴇʟᴇᴄᴛ ɴᴇᴡ ᴅɪꜰꜰɪᴄᴜʟᴛʏ</b>\n\n"
            "🟢 Easy\n"
            "🟡 Medium\n"
            "🔴 Hard\n"
            "🔵 Expert\n"
            "🟣 Legendary\n\n"
            "✦ ꜱᴇɴᴅ ɴᴇᴡ ᴅɪꜰꜰɪᴄᴜʟᴛʏ ɴᴀᴍᴇ",
            parse_mode="HTML"
        )
        return

    # STEP 6 — DIFFICULTY
    if step == "difficulty":
        diff = message.text.capitalize()
        if diff not in XP_TABLE:
            bot.reply_to(
                message,
                "<b>❌ ɪɴᴠᴀʟɪᴅ ᴅɪꜰꜰɪᴄᴜʟᴛʏ</b>\nUse: Easy / Medium / Hard / Expert / Legendary",
                parse_mode="HTML"
            )
            return
        state["data"]["difficulty"] = diff
        state["step"] = "answer"
        bot.reply_to(message, "<b>✔ Send the number of the correct answer (1-4)</b>", parse_mode="HTML")
        return

    # STEP 7 — CORRECT ANSWER
    if step == "answer":
        try:
            correct_index = int(message.text) - 1
            if correct_index not in [0,1,2,3]:
                raise ValueError
        except:
            bot.reply_to(message, "<b>❌ Invalid. Send 1, 2, 3, or 4.</b>", parse_mode="HTML")
            return

        state["data"]["answer"] = correct_index

        # Update the quiz
        quiz["question"] = state["data"]["question"]
        quiz["options"] = [
            state["data"]["opt1"],
            state["data"]["opt2"],
            state["data"]["opt3"],
            state["data"]["opt4"]
        ]
        quiz["difficulty"] = state["data"]["difficulty"]
        quiz["xp"] = XP_TABLE[state["data"]["difficulty"]]
        quiz["answer"] = state["data"]["answer"]

        del quiz_edit_state[user_id]

        bot.reply_to(
            message,
            f"<b>✅ ǫᴜɪᴢ ᴇᴅɪᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ</b>\n"
            f"🆔 <b>ID:</b> {quiz_id}\n"
            f"⚙ <b>Difficulty:</b> {quiz['difficulty']}\n"
            f"🥇 1st: {XP_TABLE[quiz['difficulty']][1]} XP\n"
            f"🥈 2nd: {XP_TABLE[quiz['difficulty']][2]} XP\n"
            f"🥉 3rd: {XP_TABLE[quiz['difficulty']][3]} XP",
            parse_mode="HTML"
        )
        
# =====================================================
# 📩 MESSAGE COUNTER → AUTO QUIZ DROP (ALL MESSAGE TYPES)
# =====================================================

@bot.message_handler(
    func=lambda m: m.chat.type in ["group", "supergroup"],
    content_types=['text', 'sticker', 'photo', 'video', 'voice', 'document', 'animation', 'audio', 'video_note', 'contact', 'location', 'dice', 'poll']
)
def group_message_counter(message):
    chat_id = message.chat.id

    # Check if group has quiz drop rate set
    if chat_id not in quiz_drop_rate:
        return

    # If quiz already active, skip counting
    if chat_id in active_quiz:
        return

    # Increment message count
    group_message_count[chat_id] = group_message_count.get(chat_id, 0) + 1

    # If message count reaches drop rate, drop a quiz
    if group_message_count[chat_id] >= quiz_drop_rate[chat_id]:
        group_message_count[chat_id] = 0
        drop_quiz(chat_id)

# =====================================================
# 🎯 QUIZ DROP FUNCTION
# =====================================================
def drop_quiz(chat_id):
    if not quizzes:
        return

    # Choose difficulty based on weights
    difficulty = random.choices(
        list(DIFFICULTY_WEIGHTS.keys()),
        weights=DIFFICULTY_WEIGHTS.values(),
        k=1
    )[0]

    # Filter quizzes of that difficulty
    available = [q for q in quizzes if q["difficulty"] == difficulty]
    if not available:
        return

    quiz = random.choice(available)

    # Mark quiz as active in this group
    active_quiz[chat_id] = {
        "quiz": quiz,
        "answered": [],
        "position": 0
    }

    # Prepare inline buttons for options
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i, option in enumerate(quiz["options"]):
        markup.add(
            types.InlineKeyboardButton(
                option,
                callback_data=f"quiz|{chat_id}|{quiz['id']}|{i}"
            )
        )

    # Send quiz in your style
    bot.send_message(
        chat_id,
        f"🧠 <b>ǫᴜɪᴢ ᴛɪᴍᴇ!</b>\n"
        f"╭──────────────\n"
        f"❓ {quiz['question']}\n"
        f"⚙️ <b>ᴅɪꜰꜰɪᴄᴜʟᴛʏ:</b> {difficulty}\n"
        f"╰──────────────",
        parse_mode="HTML",
        reply_markup=markup
    )

# =====================================================
# ✅ ANSWER CALLBACK HANDLER
# =====================================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("quiz|"))
def quiz_callback(call):
    _, chat_id, quiz_id, option = call.data.split("|")
    chat_id = int(chat_id)
    quiz_id = int(quiz_id)
    option = int(option)

    if chat_id not in active_quiz:
        return

    quiz_data = active_quiz[chat_id]
    quiz = quiz_data["quiz"]

    # Already answered
    if call.from_user.id in quiz_data["answered"]:
        bot.answer_callback_query(call.id, "❌ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴀɴꜱᴡᴇʀᴇᴅ")
        return

    # Wrong answer
    if option != quiz["answer"]:
        bot.answer_callback_query(
            call.id,
            f"❌ ᴡʀᴏɴɢ! ᴄᴏʀʀᴇᴄᴛ: {quiz['answer']+1}",
            show_alert=True
        )
        return

    # Correct answer
    quiz_data["position"] += 1
    pos = quiz_data["position"]
    quiz_data["answered"].append(call.from_user.id)

    if pos <= 3:
        xp = XP_TABLE[quiz["difficulty"]][pos]
        user_xp[call.from_user.id] = user_xp.get(call.from_user.id, 0) + xp

        bot.answer_callback_query(
            call.id,
            f"✅ ᴄᴏʀʀᴇᴄᴛ!\n🏆 {pos}ꜱᴛ ᴡɪɴɴᴇʀ\n✨ +{xp} XP",
            show_alert=True
        )

    # Remove quiz after top 3 answered
    if pos >= 3:
        del active_quiz[chat_id]
# -----------------------------
# Run the bot
# -----------------------------
bot.polling()