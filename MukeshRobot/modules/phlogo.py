import os
from MukeshRobot import telethn as tbot
from MukeshRobot.events import register
from telethon import events
from PIL import Image, ImageDraw, ImageFont

# generate function
def generate(text1, text2):
    ImageDraw.Draw(Image.new("RGBA",(font.getsize(text2)[0]+20,140),color=(240, 152, 0))).text((10,int((Image.new("RGBA",(font.getsize(text2)[0]+20,140),color=(240, 152, 0)).height-font.getsize(text2)[1])/2)-10),text2, (0,0,0),font=font)
    return Gabung([Image.new("RGBA",(font.getsize(text2)[0]+20,140),color=(240, 152, 0)), text1])


@register(pattern="^[!/.]phlogo ?(.*)")
async def ph(event):
    query = event.pattern_match.group(1)
    await event.message.delete()
    if query == "":
        await event.reply("ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ʙʀᴜʜ, ᴇ.ɢ.: `/phlogo porn hub`")
        return
    try:
        input_str = "".join(event.text.split(maxsplit=1)[1:])
        p = query.split(" ", 1)[0]
        h = query.split(" ", 1)[1]
    except:
        await event.reply("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴛʀʏ ɢɪᴠɪɴɢ ᴛᴡᴏ ᴡᴏʀᴅs. ᴇ.ɢ.: `/phlogo porn hub`")
    return
    result = generate(f"{p}",f"{h}")
    pic = "ph.png"
    result.save(pic, "png")
    await tbot.send_file(event.chat_id, pic, reply_to=event.reply_to_msg_id, forcedocument=False)
    os.remove(pic)


@register(pattern="^[!/.]phst ?(.*)")
async def ph(event):
    query = event.pattern_match.group(1)
    try:
        await event.message.delete()
    except:
        pass
    if query == "":
        await event.reply("ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ʙʀᴜʜ, ᴇ.ɢ.: `/phst Razer Bot`")
        return
    try:
        input_str = "".join(e.text.split(maxsplit=1)[1:])
        p = query.split(" ", 1)[0]
        h = query.split(" ", 1)[1]
    except:
        await event.reply("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴛʀʏ ɢɪᴠɪɴɢ ᴛᴡᴏ ᴡᴏʀᴅs. ᴇ.ɢ.: `/phst porn hub`")
        return
    result = generate(f"{p}",f"{h}")
    stc = "ph.webp"
    result.save(stc, "webp")
    await tbot.send_file(event.chat_id, stc, reply_to=event.reply_to_msg_id, forcedocument=False)
    os.remove(stc)
