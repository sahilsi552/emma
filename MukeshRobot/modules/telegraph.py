import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from MukeshRobot import telethn as tbot
from MukeshRobot.events import register
TMP_DOWNLOAD_DIRECTORY = "./"
telegraph = Telegraph(domain="graph.org")
r = telegraph.create_account(short_name="Controller")
auth_url = r["auth_url"]


@register(pattern="^/tg(m|t) ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "m":
            downloaded_file_name = await tbot.download_media(
                r_message, TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply(f"Downloaded to {downloaded_file_name} in {ms} seconds.")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit(f"ERROR: {str(exc)}")
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit(
                    f"Uploaded to https://graph.org{media_urls[0]})",
                    link_preview=True,
                )
        elif input_str == "t":
            user_object = await tbot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tbot.download_media(
                    r_message, TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            await event.reply(
                f'Pasted to https://graph.org/{response["path"]} in {ms} seconds.',
                link_preview=True,
            )
    else:
        await event.reply("Reply to a message to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


__help__ = """
ɪ ᴄᴀɴ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ
 ❍ /tgm :ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ
 ❍ /tgt :ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ
 ❍ /tgt [ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ]: ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ.
"""

__mod_name__ = "T-Gʀᴀᴘʜ📱"
