import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.sql.users_sql as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

PM_START_TEXT = """ 

Hɪ [🥀](https://graph.org/file/2dda62f78a2d0dfde2c23.jpg) Dᴇᴀʀ! {} Mʏ ɴᴀᴍᴇ ɪs {} 

I ᴄᴀɴ ʜᴇʟᴘ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴡɪᴛʜ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs, ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs!

"""

buttons = [
    [
        InlineKeyboardButton(
            text="➕Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ➕",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="ʜᴇʟᴘ❓", callback_data="help_back"),
        InlineKeyboardButton(
                            text=" 🙆🏿 ɪɴғᴏ ", callback_data="mukesh_"
                        ),
    ],
    [
        InlineKeyboardButton(
                            text="👨‍💻ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
        InlineKeyboardButton(text="ᴍᴜsɪᴄ 🎧",callback_data="Music_"),
    ],
    [
        InlineKeyboardButton(
                            text="ɪɴʟɪɴᴇ", switch_inline_query_current_chat="google"
                        ),
        InlineKeyboardButton(
                            text="Hᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ⁉️",
                            callback_data="bot_config_help",
                        )
    ],


]

HELP_STRINGS = f"""
» *{BOT_NAME}  ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ*"""

DONATE_STRING = """ʜᴇʏ ʙᴀʙʏ,
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ @Legend_coder ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ ɪɴғᴏ ᴄʜᴀᴛ @the_support_chat ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"MukeshRobot.modules.{module_name}")
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
         text=text,
        
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match[1])

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ  !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match[1]
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(text,


                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match[1])
            query.message.edit_text(HELP_STRINGS,

                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match[1])
            query.message.edit_text(HELP_STRINGS,

                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(HELP_STRINGS,

                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
            # query.message.delete()

    except BadRequest:
        pass


def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(f"*ʜᴇʏ,*🥀\n  *ᴛʜɪs ɪs {dispatcher.bot.first_name}*"
            "\n*ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ➕ ᴍᴜsɪᴄ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀꜱɪʟʏ ᴀɴᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ꜱᴄᴀᴍᴍᴇʀꜱ ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀꜱ.*"
            "\n*ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ sǫʟᴀʟᴄʜᴇᴍʏ ᴀɴᴅ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.*"
            "\n\n────────────────────"
            f"\n*➻ ᴜᴩᴛɪᴍᴇ »* {uptime}"
            f"\n*➻ ᴜsᴇʀs »* {sql.num_users()}"
            f"\n*➻ ᴄʜᴀᴛs »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n➲  ɪ ᴄᴀɴ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ꜱʏꜱᴛᴇᴍ."
            "\n➲  ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀɴᴅ ᴇᴠᴇɴ ꜱᴇᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ʀᴜʟᴇꜱ."
            "\n➲  ɪ ᴄᴀɴ ᴡᴀʀɴ ᴜꜱᴇʀꜱ ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴꜱ, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇꜰɪɴᴇᴅ ᴀᴄᴛɪᴏɴꜱ ꜱᴜᴄʜ ᴀꜱ ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ ᴋᴇᴇᴘɪɴɢ ꜱʏꜱᴛᴇᴍ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇꜱ ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅꜱ."
            f"\n\n➻ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ {dispatcher.bot.first_name}.",


            reply_markup=InlineKeyboardMarkup(
                    [
                        [

                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support"
                        ),
                        InlineKeyboardButton(
                            text="ᴄᴏᴍᴍᴀɴᴅs 💁", callback_data="help_back"
                        ),
                        ],
                        [
                        InlineKeyboardButton(
                            text="👨‍💻ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),

                        ],
                        [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="mukesh_back"),
                        ],
                    ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,

            timeout=60,
        )
    elif query.data == "mukesh_support":
        query.message.edit_text("**๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴩ ᴀɴᴅ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀ**"
            f"\n\nɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ {dispatcher.bot.first_name} ᴏʀ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ ᴀʙᴏᴜᴛ ᴛʜᴇ {dispatcher.bot.first_name}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ ɪɴғᴏ ᴄʜᴀᴛ.",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🏡 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴩᴅᴀᴛᴇs 🍷", url=f"\x68\x74\x74\x70\x73\x3A\x2F\x2F\x74\x2E\x6D\x65\x2F\x6D\x75\x6B\x65\x73\x68\x62\x6F\x74\x7A\x6F\x6E\x65"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🥀 ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ 🍹", url="\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x6E\x6F\x6F\x62\x2D\x6D\x75\x6B\x65\x73\x68"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="mukesh_"),
                    ],
                ]
            ),
        )
def MukeshRobot_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query


    if query.data == "bot_config_help":
        query.answer()
        query.message.edit_text(
            f"""ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ  ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ᴛᴜᴛᴏʀɪᴀʟ.

Tʜᴇ ғɪʀsᴛ ᴛʜɪɴɢ ᴛᴏ ᴅᴏ ɪs ᴛᴏ ᴀᴅᴅ {BOT_NAME} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ! Fᴏʀ ᴅᴏɪɴɢ ᴛʜᴀᴛ, ᴘʀᴇss ᴛʜᴇ ᴜɴᴅᴇʀ ʙᴜᴛᴛᴏɴ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ᴛʜᴇɴ ᴘʀᴇss "Dᴏɴᴇ" ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴛʜᴇ ᴛᴜᴛᴏʀɪᴀʟ.
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ",
                            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⚗️ ᴅᴏɴᴇ ⚗️", callback_data="a_added_help"
                        )
                    ],
                ]
            ),
        )
    elif query.data == "a_added_help":
        query.answer()
        query.message.edit_text(
            f"""Oᴋ, ᴡᴇʟʟ ᴅᴏɴᴇ!

Nᴏᴡ ғᴏʀ ʟᴇᴛ ᴍᴇ ᴡᴏʀᴋ ᴄᴏʀʀᴇᴄᴛʟʏ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴍᴀᴋᴇ ᴍᴇ Aᴅᴍɪɴ ᴏғ ʏᴏᴜʀ Gʀᴏᴜᴘ!

Tᴏ ᴅᴏ ᴛʜᴀᴛ, ғᴏʟʟᴏᴡ ᴛʜɪs ᴇᴀsʏ sᴛᴇᴘs: 
▫️ Gᴏ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
▫️ Pʀᴇss ᴛʜᴇ Gʀᴏᴜᴘ's ɴᴀᴍᴇ
▫️ Pʀᴇss Mᴏᴅɪғʏ
▫️ Pʀᴇss ᴏɴ Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ
▫️ Pʀᴇss Aᴅᴅ Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ
▫️ Pʀᴇss ᴛʜᴇ Mᴀɢɴɪғʏɪɴɢ Gʟᴀss
▫️ Sᴇᴀʀᴄʜ @{BOT_USERNAME}
▫️ Cᴏɴғɪʀᴍ""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🎥 Exᴀᴍᴘʟᴇ Vɪᴅᴇᴏ 🎥",
                            callback_data="tutorial_v_help",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⚗️ ᴅᴏɴᴇ ⚗️", callback_data="b_added_help"
                        )
                    ],
                ]
            ),
        )
    elif query.data == "tutorial_v_help":
        query.answer()
        query.message.reply_animation(
            "https://te.legra.ph/file/bee5894fc60aa0faee9d8.mp4"
        )
        query.message.edit_text(
            f"""Oᴋ, ᴡᴇʟʟ ᴅᴏɴᴇ!

Nᴏᴡ ғᴏʀ ʟᴇᴛ ᴍᴇ ᴡᴏʀᴋ ᴄᴏʀʀᴇᴄᴛʟʏ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴍᴀᴋᴇ ᴍᴇ Aᴅᴍɪɴ ᴏғ ʏᴏᴜʀ Gʀᴏᴜᴘ!

Tᴏ ᴅᴏ ᴛʜᴀᴛ, ғᴏʟʟᴏᴡ ᴛʜɪs ᴇᴀsʏ sᴛᴇᴘs: 
▫️ Gᴏ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
▫️ Pʀᴇss ᴛʜᴇ Gʀᴏᴜᴘ's ɴᴀᴍᴇ
▫️ Pʀᴇss Mᴏᴅɪғʏ
▫️ Pʀᴇss ᴏɴ Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ
▫️ Pʀᴇss Aᴅᴅ Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ
▫️ Pʀᴇss ᴛʜᴇ Mᴀɢɴɪғʏɪɴɢ Gʟᴀss
▫️ Sᴇᴀʀᴄʜ @{BOT_USERNAME}
▫️ Cᴏɴғɪʀᴍ""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⚗️ ᴅᴏɴᴇ ⚗️", callback_data="b_added_help"
                        )
                    ]
                ]
            ),
        )
    elif query.data == "b_added_help":
        query.answer()
        query.message.edit_text(
            """Exᴄᴇʟʟᴇɴᴛ!
Nᴏᴡ ᴛʜᴇ Bᴏᴛ ɪs ʀᴇᴀᴅʏ ᴛᴏ ᴜsᴇ!

Usɪɴɢ ᴛʜᴇ /settings ᴄᴏᴍᴍᴀɴᴅ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴛ ʏᴏᴜʀ ᴅɪsᴘᴏsᴀʟ ᴀ sᴇʀɪᴇs ᴏғ ᴛʜɪɴɢs ᴛʜᴀᴛ ᴄᴀɴ ʙᴇ ᴍᴏᴅɪғɪᴇᴅ ʜᴏᴡ ʏᴏᴜ ᴘʀᴇғᴇʀ, ᴀs ʀᴇǫᴜɪʀᴇᴅ ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ.""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🍹 Cᴏɴᴛɪɴᴜᴇ 🍹", callback_data="c_added_help"
                        )
                    ]
                ]
            ),
        )

    elif query.data == "c_added_help":
        query.answer()
        query.message.edit_text(
            """Tᴏ ᴄᴏɴᴄʟᴜᴅᴇ, I ᴇxᴘʟᴀɪɴ ʏᴏᴜ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ Bᴏᴛ's ʙᴀsɪᴄ ᴄᴏᴍᴍᴀɴᴅs, ғᴏʀ ᴛʜᴇ ʙᴀsɪʟᴀʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ's ᴜsᴇʀs.

/ban ᴇxᴘᴇʟs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜᴏᴜᴛ ɢɪᴠɪɴɢ ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/mute ᴀʟʟᴏᴡs ᴀ ᴜsᴇʀ ᴛᴏ ʀᴇᴀᴅ, ʙᴜᴛ ɴᴏᴛ ᴛᴏ ᴡʀɪᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ

/kick ᴇxᴘᴇʟs ᴀ ᴜsᴇʀ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ ʙᴜᴛ ᴡɪᴛʜ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/unban ᴜsᴇᴅ ᴏɴ ᴀ ʙᴀɴɴᴇᴅ ᴜsᴇʀ, ɢɪᴠᴇs ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/info sʜᴏᴡs ᴀʟʟ ᴛʜᴇ ɪɴғᴏs ᴏғ ᴛʜᴇ ᴄʜᴏᴏsᴇᴅ ᴜsᴇʀ

/staff sʜᴏᴡs ᴛʜᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʟɪsᴛ ᴏғ ᴛʜᴇ Gʀᴏᴜᴘ's sᴛᴀғғ""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🎥 Exᴀᴍᴘʟᴇ Vɪᴅᴇᴏ 🎥",
                            callback_data="tutorial_v2_help",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🍹 Cᴏɴᴛɪɴᴜᴇ 🍹", callback_data="d_added_help"
                        )
                    ],
                ]
            ),
        )
    elif query.data == "tutorial_v2_help":
        query.answer()
        query.message.reply_animation(
            "https://te.legra.ph/file/b069a6a6f5ae539f60b30.mp4"
        )
        query.message.edit_text(
            """Tᴏ ᴄᴏɴᴄʟᴜᴅᴇ, I ᴇxᴘʟᴀɪɴ ʏᴏᴜ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ Bᴏᴛ's ʙᴀsɪᴄ ᴄᴏᴍᴍᴀɴᴅs, ғᴏʀ ᴛʜᴇ ʙᴀsɪʟᴀʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ's ᴜsᴇʀs.

/ban ᴇxᴘᴇʟs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜᴏᴜᴛ ɢɪᴠɪɴɢ ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/mute ᴀʟʟᴏᴡs ᴀ ᴜsᴇʀ ᴛᴏ ʀᴇᴀᴅ, ʙᴜᴛ ɴᴏᴛ ᴛᴏ ᴡʀɪᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ

/kick ᴇxᴘᴇʟs ᴀ ᴜsᴇʀ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ ʙᴜᴛ ᴡɪᴛʜ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/unban ᴜsᴇᴅ ᴏɴ ᴀ ʙᴀɴɴᴇᴅ ᴜsᴇʀ, ɢɪᴠᴇs ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ ʀᴇJᴏɪɴ ᴡɪᴛʜ ᴛʜᴇ ɢʀᴏᴜᴘ's ʟɪɴᴋ

/info sʜᴏᴡs ᴀʟʟ ᴛʜᴇ ɪɴғᴏs ᴏғ ᴛʜᴇ ᴄʜᴏᴏsᴇᴅ ᴜsᴇʀ

/staff sʜᴏᴡs ᴛʜᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʟɪsᴛ ᴏғ ᴛʜᴇ Gʀᴏᴜᴘ's sᴛᴀғғ""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🍹 Cᴏɴᴛɪɴᴜᴇ 🍹", callback_data="d_added_help"
                        )
                    ]
                ]
            ),
        )
    elif query.data == "d_added_help":
        query.answer()
        query.message.edit_text(
            """Iɴ ᴄᴏɴᴄʟᴜsɪᴏɴ I ᴡᴏᴜʟᴅ ᴘᴏɪɴᴛ ᴏᴜᴛ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /reload ᴛʜᴀᴛ ᴡɪʟʟ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ɢʀᴏᴜᴘ's Aᴅᴍɪɴ ʟɪsᴛ.
Fᴏʀ ᴇxᴀᴍᴘʟᴇ ɪғ ʏᴏᴜ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴀɴ Aᴅᴍɪɴ, ʀᴇᴍᴇᴍʙᴇʀ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏʀ ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ɴᴏᴛ ɴᴏᴛɪᴄᴇ ᴛʜɪs ᴄʜᴀɴɢᴇ.

Tʜᴀɴᴋ ғᴏʀ ғᴏʟʟᴏᴡɪɴɢ ᴛʜᴇ ᴛᴜᴛᴏʀɪᴀʟ ᴀɴᴅ ʜᴀᴠᴇ ғᴜɴ ᴜsɪɴɢ ᴛʜᴇ Bᴏᴛ!""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📚 Bᴀᴄᴋ Tᴏ Hᴇʟᴘ", callback_data="help_back"
                        )
                    ]
                ]
            ),
        )
    elif query.data=="basic_help":
        query.message.edit_text("""Bᴀsɪᴄ Cᴏᴍᴍᴀɴᴅs.
👮🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Mᴏᴅᴇʀᴀᴛᴏʀs.
🕵🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs.

👮🏻 /reload ᴜᴘᴅᴀᴛᴇs ᴛʜᴇ Aᴅᴍɪɴs ʟɪsᴛ ᴀɴᴅ ᴛʜᴇɪʀ ᴘʀɪᴠɪʟᴇɢᴇs.
🕵🏻 /settings ʟᴇᴛs ʏᴏᴜ ᴍᴀɴᴀɢᴇ ᴀʟʟ ᴛʜᴇ Bᴏᴛ sᴇᴛᴛɪɴɢs ɪɴ ᴀ ɢʀᴏᴜᴘ.
👮🏻 /ban ʟᴇᴛs ʏᴏᴜ ʙᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜᴏᴜᴛ ɢɪᴠɪɴɢ ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ Jᴏɪɴ ᴀɢᴀɪɴ ᴜsɪɴɢ ᴛʜᴇ ʟɪɴᴋ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
👮🏻 /mute ᴘᴜᴛs ᴀ ᴜsᴇʀ ɪɴ ʀᴇᴀᴅ-ᴏɴʟʏ ᴍᴏᴅᴇ. Hᴇ ᴄᴀɴ ʀᴇᴀᴅ ʙᴜᴛ ʜᴇ ᴄᴀɴ'ᴛ sᴇɴᴅ ᴀɴʏ ᴍᴇssᴀɢᴇs.
👮🏻 /kick ʙᴀɴs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ, ɢɪᴠɪɴɢ ʜɪᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ Jᴏɪɴ ᴀɢᴀɪɴ ᴡɪᴛʜ ᴛʜᴇ ʟɪɴᴋ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
👮🏻 /unban ʟᴇᴛs ʏᴏᴜ ʀᴇᴍᴏᴠᴇ ᴀ ᴜsᴇʀ ғʀᴏᴍ ɢʀᴏᴜᴘ's ʙʟᴀᴄᴋʟɪsᴛ, ɢɪᴠɪɴɢ ᴛʜᴇᴍ ᴛʜᴇ ᴘᴏssɪʙɪʟɪᴛʏ ᴛᴏ Jᴏɪɴ ᴀɢᴀɪɴ ᴡɪᴛʜ ᴛʜᴇ ʟɪɴᴋ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
👮🏻 /info ɢɪᴠᴇs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜsᴇʀ.

◽️ /staff ɢɪᴠᴇs ᴛʜᴇ ᴄᴏᴍᴘʟᴇᴛᴇ Lɪsᴛ ᴏғ ɢʀᴏᴜᴘ Sᴛᴀғғ!.""",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="mukesh_back":
        query.message.edit_text("""Exᴘᴇʀᴛ ᴄᴏᴍᴍᴀɴᴅs

👥 Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴀʟʟ ᴜsᴇʀs
👮🏻 Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Mᴏᴅᴇʀᴀᴛᴏʀs.
🕵🏻 Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs

🕵🏻  /unbanall ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘs
👮🏻  /unmuteall ᴜɴᴍᴜᴛᴇᴀʟʟ ᴀʟʟ ғʀᴏᴍ Yᴏᴜʀ Gʀᴏᴜᴘ

Pɪɴɴᴇᴅ Mᴇssᴀɢᴇs
🕵🏻  /pin [ᴍᴇssᴀɢᴇ] sᴇɴᴅs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ Bᴏᴛ ᴀɴᴅ ᴘɪɴs ɪᴛ.
🕵🏻  /pin ᴘɪɴs ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪɴ ʀᴇᴘʟʏ
🕵🏻  /unpin ʀᴇᴍᴏᴠᴇs ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.
🕵🏻  /adminlist ʟɪsᴛ ᴏғ ᴀʟʟ ᴛʜᴇ sᴘᴇᴄɪᴀʟ ʀᴏʟᴇs ᴀssɪɢɴᴇᴅ ᴛᴏ ᴜsᴇʀs.

◽️ /bug: (ᴍᴇssᴀɢᴇ) ᴛᴏ Sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴇʀʀᴏʀs ᴡʜɪᴄʜ ʏᴏᴜ ᴀʀᴇ ғᴀᴄɪɴɢ 
ᴇx: /bug Hᴇʏ Tʜᴇʀᴇ Is ᴀ Sᴏᴍᴇᴛʜɪɴɢ Eʀʀᴏʀ @username ᴏғ ᴄʜᴀᴛ! .""",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="advance_help":
        query.message.edit_text("""Aᴅᴠᴀɴᴄᴇᴅ Cᴏᴍᴍᴀɴᴅs

👮🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Mᴏᴅᴇʀᴀᴛᴏʀs.
🕵🏻Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs.
🛃 Aᴠᴀɪʟᴀʙʟᴇ ᴛᴏ Aᴅᴍɪɴs & Cʟᴇᴀɴᴇʀs

Wᴀʀɴ Mᴀɴᴀɢᴇᴍᴇɴᴛ
👮🏻  /warn ᴀᴅᴅs ᴀ ᴡᴀʀɴ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ
👮🏻  /unwarn ʀᴇᴍᴏᴠᴇs ᴀ ᴡᴀʀɴ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ
👮🏻  /warns ʟᴇᴛs ʏᴏᴜ sᴇᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ᴜsᴇʀ ᴡᴀʀɴs

🛃  /del ᴅᴇʟᴇᴛᴇs ᴛʜᴇ sᴇʟᴇᴄᴛᴇᴅ ᴍᴇssᴀɢᴇ
🛃  /purge ᴅᴇʟᴇᴛᴇs ғʀᴏᴍ ᴛʜᴇ sᴇʟᴇᴄᴛᴇᴅ ᴍᴇssᴀɢᴇ.""",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="expert_help":
        query.message.edit_text(f"""━━━━━━━━━━━━━━━━━━━━
ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇꜰꜰᴇᴄᴛɪᴠᴇ ɴᴏᴡ :
🎉 ᴄᴏɴɢʀᴀɢᴜʟᴀᴛɪᴏɴꜱ 🎉
[{BOT_NAME}]("https://t.me/{BOT_USERNAME}") ɴᴏᴡ ʀᴇᴀᴅʏ ᴛᴏ
ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ.

ᴀᴅᴍɪɴ ᴛᴏᴏʟꜱ :
ʙᴀꜱɪᴄ ᴀᴅᴍɪɴ ᴛᴏᴏʟꜱ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ
ᴘʀᴏᴛᴇᴄᴛ & ᴘᴏᴡᴇʀᴜᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
ʏᴏᴜ ᴄᴀɴ ʙᴀɴ, ᴋɪᴄᴋ, ᴘʀᴏᴍᴏᴛᴇ
ᴍᴇᴍʙᴇʀꜱ ᴀꜱ ᴀᴅᴍɪɴ ᴛʜʀᴏᴜɢʜ ʙᴏᴛ.

ɢʀᴇᴇᴛɪɴɢꜱ :
ʟᴇᴛꜱ ꜱᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ
ᴡᴇʟᴄᴏᴍᴇ ɴᴇᴡ ᴜꜱᴇʀꜱ ᴄᴏᴍɪɴɢ ᴛᴏ
ʏᴏᴜʀ ɢʀᴏᴜᴘ.
ꜱᴇɴᴅ /setwelcome ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ
ꜱᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇ!""",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="donation_help":
        query.message.edit_text("""Aʀᴇ ʏᴏᴜ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ ʜᴇʟᴘɪɴɢ ᴍʏ ᴄʀᴇᴀᴛᴏʀ ᴡɪᴛʜ ʜɪs ᴇғғᴏʀᴛs ᴛᴏ ᴋᴇᴇᴘ ᴍᴇ ɪɴ ᴀᴄᴛɪᴠᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ? Iғ ʏᴇs, Yᴏᴜ'ʀᴇ ɪɴ ᴛʜᴇ ʀɪɢʜᴛ ᴘʟᴀᴄᴇ. 

Wᴇ ᴇᴍᴘʜᴀsɪsᴇ ᴛʜᴇ ɪᴍᴘᴏʀᴛᴀɴᴄᴇ ᴏғ ɴᴇᴇᴅɪɴɢ ғᴜɴᴅs ᴛᴏ ᴋᴇᴇᴘ MᴜᴋᴇsʜRᴏʙᴏᴛ ᴜɴᴅᴇʀ ᴀᴄᴛɪᴠᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ. Yᴏᴜʀ ᴅᴏɴᴀᴛɪᴏɴs ɪɴ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ᴏғ ᴍᴏɴᴇʏ ᴛᴏ MᴜᴋᴇsʜRᴏʙᴏᴛ sᴇʀᴠᴇʀs ᴀɴᴅ ᴏᴛʜᴇʀ ᴜᴛɪʟɪᴛɪᴇs ᴡɪʟʟ ᴀʟʟᴏᴡ ᴜs ᴛᴏ sᴜsᴛᴀɪɴ ᴛʜᴇ ʟɪғᴇsᴘᴀɴ ɪɴ ᴛʜᴇ ʟᴏɴɢ ᴛᴇʀᴍ. Wᴇ ᴡɪʟʟ ᴜsᴇ ᴀʟʟ ᴏғ ᴛʜᴇ ᴅᴏɴᴀᴛɪᴏɴs ᴛᴏ ᴄᴏᴠᴇʀ ғᴜᴛᴜʀᴇ ᴇxᴘᴇɴsᴇs ᴀɴᴅ ᴜᴘɢʀᴀᴅᴇs ᴏғ ᴛʜᴇ sᴇʀᴠᴇʀs ᴄᴏsᴛs. Iғ ʏᴏᴜ'ᴠᴇ ɢᴏᴛ sᴘᴀʀᴇ ᴍᴏɴᴇʏ ᴛᴏ ʜᴇʟᴘ ᴜs ɪɴ ᴛʜɪs ᴇғғᴏʀᴛ, Kɪɴᴅʟʏ ᴅᴏ sᴏ ᴀɴᴅ ʏᴏᴜʀ ᴅᴏɴᴀᴛɪᴏɴs ᴄᴀɴ ᴀʟsᴏ ᴍᴏᴛɪᴠᴀᴛᴇ ᴜs ᴋᴇᴇᴘ ʙʀɪɴɢ ᴏɴ ɴᴇᴡ ғᴇᴀᴛᴜʀᴇs.

Yᴏᴜ ᴄᴀɴ ʜᴇʟᴘ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ ᴡɪᴛʜ ᴅᴏɴᴀᴛɪᴏɴs""",

            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• Dᴏɴᴀᴛᴇ •", url="https://t.me/mukeshbotzone/7"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )  
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            f"""
*ʜᴇʏ,
 ᴛʜɪs ɪs {BOT_NAME},
ᴀɴ ᴏᴩᴇɴ sᴏᴜʀᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.*

ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴀɴᴅ ᴜsɪɴɢ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴀɴᴅ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇ.


*ʜᴇʀᴇ ɪs ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ :* [ɢɪᴛʜᴜʙ](\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74)


{BOT_NAME} ɪs ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74/blob/main/LICENSE).
© 2023 - 2024 | [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{SUPPORT_CHAT}), ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            
            
            reply_markup=InlineKeyboardMarkup(
                [[
        InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", url="\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74")
                ],
                ]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            
            timeout=60,
            
        )

        
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_text(
            """
 ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ ᴍᴜꜱɪᴄ 
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⍟ ᴀᴅᴍɪɴ ⍟", callback_data="Music_admin"
                        ),
                        InlineKeyboardButton(
                            text="⍟ ᴘʟᴀʏ ⍟", callback_data="Music_play"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="⍟ ʙᴏᴛ ⍟", callback_data="Music_bot"
                        ),
                        InlineKeyboardButton(
                            text="⍟ ᴇxᴛʀᴀ ⍟",
                            callback_data="Music_extra",
                        ),
                    ],
                    [
<<<<<<< HEAD
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="mukesh_back")
=======
                        InlineKeyboardButton(
                            text="⬅️ ʙᴀᴄᴋ", callback_data="Main_help"
                        )
>>>>>>> 812809312a6548569aa7e487948abfa91f52a004
                    ],
                ]
            ),
        )
    elif query.data == "Music_admin":
        query.message.edit_text(
            '*» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ «*
ᴊᴜsᴛ ᴀᴅᴅ *ᴄ* ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.

/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.

/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.

/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.
',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⬅️ ʙᴀᴄᴋ", callback_data="Music_"
                        ),
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support"
                        ),
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),

            timeout=60,

        )
    elif query.data == "Music_bot":
        query.message.edit_text(
            '*» ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ «*
/stats - ɢᴇᴛ ᴛᴏᴘ 10 ᴛʀᴀᴄᴋꜱ ɢʟᴏʙᴀʟ ꜱᴛᴀᴛꜱ, ᴛᴏᴘ 10 ᴜꜱᴇʀꜱ ᴏғ ʙᴏᴛ, ᴛᴏᴘ 10 ᴄʜᴀᴛꜱ ᴏɴ ʙᴏᴛ, ᴛᴏᴘ 10 ᴘʟᴀʏᴇᴅ ɪɴ ᴀ ᴄʜᴀᴛ ᴇᴛᴄ ᴇᴛᴄ.

/sudolist - ᴄʜᴇᴄᴋ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴀʙɢ  ʙᴏᴛ

/lyrics [ᴍᴜsɪᴄ ɴᴀᴍᴇ] - sᴇᴀʀᴄʜᴇs ʟʏʀɪᴄs ғᴏʀ ᴛʜᴇ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴍᴜsɪᴄ ᴏɴ ᴡᴇʙ.

/song [ᴛʀᴀᴄᴋ ɴᴀᴍᴇ] or [ʏᴛ ʟɪɴᴋ] - ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ3 or ᴍᴘ4 ғᴏʀᴍᴀᴛꜱ.

/player -  ɢᴇt ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴘʟᴀʏɪɴɢ ᴘᴀɴᴇʟ.

c ꜱᴛᴀɴᴅꜱ ꜰᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.

/queue ᴏʀ /cqueue- ᴄʜᴇᴄᴋ Qᴜᴇᴜᴇ ʟɪꜱᴛ ᴏꜰ ᴍᴜꜱɪᴄ.
',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⬅️ ʙᴀᴄᴋ", callback_data="Music_"
                        ),
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support"
                        ),
                    ]
                ]
            ),
        )
    elif query.data == "Music_extra":
        query.message.edit_text(
            '*» ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅꜱ «*
/mstart - ꜱᴛᴀʀᴛ ᴛʜᴇ ᴍᴜꜱɪᴄ ʙᴏᴛ.
/mhelp  - ɢᴇᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ʜᴇʟᴘᴇʀ ᴍᴇɴᴜ ᴡɪᴛʜ ᴅᴇᴛᴀɪʟᴇᴅ ᴇxᴘʟᴀɴᴀᴛɪᴏɴꜱ ᴏғ ᴄᴏᴍᴍᴀɴᴅꜱ.
/ping- ᴘɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴄʜᴇᴄᴋ ʀᴀᴍ, ᴄᴘᴜ ᴇᴛᴄ ꜱᴛᴀᴛꜱ ᴏғ ʙᴏᴛ.

*ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ:*
/settings - ɢᴇᴛ a ᴄᴏᴍᴘʟᴇᴛᴇ ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ ᴡɪᴛʜ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ
',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⬅️ ʙᴀᴄᴋ", callback_data="Music_"
                        ),
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support"
                        ),
                    ]
                ]
            ),
        )
    elif query.data == "Music_play":
        query.message.edit_text(f"*» ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""
/play or /vplay or /cplay  - ʙᴏᴛ ᴡɪʟʟ ꜱᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʏᴏᴜʀ ɢɪᴠᴇɴ ϙᴜᴇʀʏ on ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏʀ ꜱᴛʀᴇᴀᴍ ʟɪᴠᴇ ʟɪɴᴋꜱ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.

/playforce or /vplayforce or /cplayforce -  ғᴏʀᴄᴇ ᴘʟᴀʏ ꜱᴛᴏᴘꜱ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴛʀᴀᴄᴋ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ ꜱᴛᴀʀᴛꜱ ᴘʟᴀʏɪɴɢ ᴛʜᴇ ꜱᴇᴀʀᴄʜᴇᴅ ᴛʀᴀᴄᴋ ɪɴꜱᴛᴀɴᴛʟʏ ᴡɪᴛʜᴏᴜᴛ ᴅɪꜱᴛᴜʀʙɪɴɢ/clearing queue.

/channelplay [ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪꜱᴀʙʟᴇ] - ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴛʀᴇᴀᴍ ᴍᴜꜱɪᴄ ᴏɴ ᴄʜᴀɴɴᴇʟ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ.


*ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ*
 ʙᴏᴛ  ꜱᴇʀᴠᴇʀ ᴘʟᴀʏʟɪꜱᴛꜱ:
/playlist  - ᴄʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ᴘʟᴀʏʟɪꜱᴛ ᴏɴ ꜱᴇʀᴠᴇʀꜱ.
/deleteplaylist - ᴅᴇʟᴇᴛᴇ ᴀɴʏ ꜱᴀᴠᴇᴅ ᴍᴜꜱɪᴄ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪꜱᴛ
/play  - ꜱᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ᴘʟᴀʏʟɪꜱᴛ ғʀᴏᴍ ꜱᴇʀᴠᴇʀꜱ.
""",


            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")
                    ]
                ]
            ),
        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(
                START_IMG,
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ​",
                                url=f"t.me/{context.bot.username}?start=ghelp_{module}",
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(
            START_IMG,
            "» Wʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👤 ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ",
                            url=f"https://t.me/{context.bot.username}?start=help",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="👥 ᴏᴩᴇɴ ʜᴇʀᴇ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = f"Here is the available help for the *{HELPABLE[module].__mod_name__}* module:\n{HELPABLE[module].__help__}"
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⬅️ ʙᴀᴄᴋ", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                f"*{mod.__mod_name__}*:\n{mod.__user_settings__(user_id)}"
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,

            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",

            )

    elif CHAT_SETTINGS:
        chat_name = dispatcher.bot.getChat(chat_id).title
        dispatcher.bot.send_message(
            user_id,
            text=f"Which module would you like to check {chat_name}'s settings for?",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
            ),
        )
    else:
        dispatcher.bot.send_message(
            user_id,
            "Seems like there aren't any chat settings available :'(\nSend this "
            "in a group chat you're admin in to find its current settings!",

        )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match[1]
            module = mod_match[2]
            chat = bot.get_chat(chat_id)
            text = f"*{escape_markdown(chat.title)}* has the following settings for the *{CHAT_SETTINGS[module].__mod_name__}* module:\n\n{CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)}"
            query.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⬅️ ʙᴀᴄᴋ",
                                callback_data=f"stngs_back({chat_id})",
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match[1]
            curr_page = int(prev_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what "
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match[1]
            next_page = int(next_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text=
                """Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match[1]
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(escape_markdown(chat.title)),

                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs"
            msg.reply_photo(
                START_IMG,
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url=f"t.me/{context.bot.username}?start=stngs_{chat.id}",
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs"

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING,  disable_web_page_preview=True
        )

        if OWNER_ID != 5935608297:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [ɢɪᴛʜᴜʙ](https://github.com/noob-mukesh/MukeshRobot)"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATE_STRING})",


            )

    else:
        user = update.effective_message.from_user
        bot = context.bot
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,


            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="➕ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ➕",
                            url=F"https://t.me/{dispatcher.bot.username}?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=f"{START_IMG}",
                caption=f"""
✨ㅤ{BOT_NAME} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ.
━━━━━━━━━━━━━
**ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ 𝐌ᴜᴋᴇsʜ**
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `{y()}`
**ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ:** `{telever}`
**ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `{tlhver}`
**ᴩʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ:** `{pyrover}`
━━━━━━━━━━━━━
""",reply_markup=x,parse_mode=ParseMode.MARKDOWN,
                
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Mukesh_about_callback, pattern=r"mukesh_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )
    music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_",run_async=True
    )
    mukeshrobot_main_handler = CallbackQueryHandler(
        MukeshRobot_Main_Callback, pattern=r".*_help",run_async=True)
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(mukeshrobot_main_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
