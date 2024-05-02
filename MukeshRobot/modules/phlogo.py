import os
from MukeshRobot import telethn as tbot
from MukeshRobot.events import register
from telethon import events
from PIL import Image, ImageDraw, ImageFont

font=ImageFont.truetype("expressway rg.ttf",110)
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im
def Gabung(fun):
    def gabung(arg):
        im,text1=add_corners(arg[0], 17),arg[1]
        op=Image.new("RGB",(40,20),color=(0,0,0))
        draw=ImageDraw.Draw(op)
        size=font.getlength(text1)
        baru=Image.new("RGB",(im.width+size+210+20+130,600), color=(0,0,0))
        draw=ImageDraw.Draw(baru)
        draw.text((150,250), text1,(255,255,255),font=font)
        baru.paste(im, (150+size+20,230+10), im.convert("RGBA"))
        return baru
    return gabung(fun)
def generate(text1, text2):
    panjangTextBbox=font.getbbox(text2)
    panjangTextLength=font.getlength(text2)
    panjangTextHeight=pajangTextBbox[3]-pajanjTextBbox[1]
    oren=Image.new("RGBA",(panjangTextLength+20,140),color=(240, 152, 0))
    draw=ImageDraw.Draw(oren)
    draw.text((10,int((oren.height-panjangTextHeight)/2)-10),text2, (0,0,0),font=font)
    return Gabung([oren, text1])

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
