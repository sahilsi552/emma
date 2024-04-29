#DevanshXBots.t.me
from pyrogram import *
import requests as re
from MukeshRobot import pbot, config
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import wget
import os 

buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('Gᴇɴᴇʀᴀᴛᴇ ᴛᴇᴍᴘᴍᴀɪʟ', callback_data='generate'),
                             ],
                             [
            InlineKeyboardButton('ʀᴇғʀᴇsʜ', callback_data='refresh'),
            InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close')
                   ] 
                             ])

msg_buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ', callback_data='view_msg'),
            InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close')
                   ] 
                             ])


email=''
@pbot.on_message(filters.command('tempmail'))
async def start_msg(client,message):
    await message.reply("**Gᴇɴᴇʀᴀᴛᴇ ᴀ Eᴍᴀɪʟ Nᴏᴡ❕**",
                        reply_markup=buttons)
@pbot.on_callback_query()
async def mailbox(client,message):
    response=message.data
    if response == 'close':
        await message.edit_message_text('Sᴇssɪᴏɴ Cʟᴏsᴇᴅ 📪')
    elif response == 'generate':
        global email
        email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
        await message.edit_message_text(
            f'__**Yᴏᴜʀ Tᴇᴍᴘᴏʀᴀʀʏ E-ᴍᴀɪʟ: **__`{str(email)}`',
            reply_markup=buttons,
        )
        print(email)
    elif response == 'refresh':
        print(email)
        try:
            if email=='':
                await message.edit_message_text('Gᴇɴᴇʀᴀᴛᴇ ᴀɴ Eᴍᴀɪʟ',reply_markup=buttons)
            else: 
                getmsg_endp =  "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum=str(ref_response[0]['id'])
                from_msg=ref_response[0]['from']
                subject=ref_response[0]['subject']
                refreshrply = f'You a message from {from_msg}' + '\n\nSubject : ' + subject
                await message.edit_message_text(refreshrply,
                                                reply_markup=msg_buttons)
        except Exception:
            await message.answer('Nᴏ ᴍᴇssᴀɢᴇs ᴡᴇʀᴇ ʀᴇᴄᴇɪᴠᴇᴅ..\nɪɴ ʏᴏᴜʀ Mᴀɪʟʙᴏx'+email)
    elif response == 'view_msg':
        msg =re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail=msg['from']
        date=msg['date']
        subjectt=msg['subject']
        try:
            attachments=msg['attachments'][0]
        except Exception:
            pass
        body=msg['body']
        mailbox_view = (
            f'ID No : {idnum}'
            + '\nFrom : '
            + from_mail
            + '\nDate : '
            + date
            + '\nSubject : '
            + subjectt
            + '\nmessage : \n'
            + body
        )
        await message.edit_message_text(mailbox_view,reply_markup=buttons)
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        if attachments == "[]":
            await message.edit_message_text(mailbox_view,reply_markup=buttons)
            await message.answer("Nᴏ ᴍᴇssᴀɢᴇs ᴡᴇʀᴇ ʀᴇᴄɪᴇᴠᴇᴅ.", show_alert=True)
        else:
            dlattach=attachments['filename']
            attc="https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum+"&file="+dlattach
            print(attc)
            mailbox_vieww='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body+'\n\n'+'[Download]('+attc+') Attachments'
            filedl=wget.download(attc)
            await message.edit_message_text(mailbox_vieww,reply_markup=buttons)
            os.remove(dlattach)

__mod_name__ = "TᴇᴍᴘMᴀɪʟ📩"

__help__ = """
──「 Hᴇʟᴘ ᴏғ TᴇᴍᴘMᴀɪʟ 📩 」── 

Yᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ Tᴇᴍᴘ-Mᴀɪʟ ғʀᴏᴍ Bᴏᴀ Hᴀɴᴄᴏᴄᴋ
 ❍ /tempmail : Tᴏ ɢᴇᴛ Rᴀɴᴅᴏᴍ Tᴇᴍᴘ-Mᴀɪʟ.
 """

