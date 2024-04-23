import requests
from telegram import Update
from telegram.ext import CallbackContext

from MukeshRobot import dispatcher
from MukeshRobot.modules.disable import DisableAbleCommandHandler


def truth(update: Update, context: CallbackContext):
    truth = requests.get("https://mukesh-api.vercel.app/truth").json()["results"]
    update.effective_message.reply_text(truth)


def dare(update: Update, context: CallbackContext):
    dare = requests.get("https://mukesh-api.vercel.app/dare").json()["results"]
    update.effective_message.reply_text(dare)

TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth, run_async=True)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare, run_async=True)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)

__help__ = """
*ᴛʀᴜᴛʜ & ᴅᴀʀᴇ*
 ❍ /truth  *:* sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴛʀᴜᴛʜ sᴛʀɪɴɢ.
 ❍ /dare  *:* sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴅᴀʀᴇ sᴛʀɪɴɢ.
"""
__mod_name__ = "Tʀᴜᴛʜ-Dᴀʀᴇ 🌵"
