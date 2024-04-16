from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
import requests,json
from pyrogram.enums import  ParseMode
from bs4 import BeautifulSoup
from .. import pbot as Mukesh,BOT_USERNAME

keywords_list = ["google", "pypi", "github","whisper"]
PRVT_MSGS = {}
@Mukesh.on_inline_query()
async def inline_menu(c: Mukesh, inline_query: InlineQuery):
    if inline_query.query.strip().lower().strip() == "":
        buttons =[]
        buttons.add(
            *[
                (InlineKeyboardButton(text=i, switch_inline_query_current_chat=i))
                for i in keywords_list
            ]
        )
        answerss = [
            InlineQueryResultArticle(
                title="ɪɴʟɪɴᴇ ᴄᴏᴍᴍᴀɴᴅꜱ",
                description="ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ɪɴʟɪɴᴇ ᴜꜱᴀɢᴇ.",
                input_message_content=InputTextMessageContent(
                    "ᴄʟɪᴄᴋ ᴀ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ"
                ),
                thumb_url="https://hamker.me/cy00x5x.png",
                reply_markup=buttons,
            )
        ]
        await inline_query.answer(results=answerss)
    elif inline_query.query.strip().lower().split()[0] == "google":
        if len(inline_query.query.strip().lower().split()) < 2:
            return await inline_query.answer(
                results=[],
                switch_pm_text="ɢᴏᴏɢʟᴇ ꜱᴇᴀʀᴄʜ | ɢᴏᴏɢʟᴇ [Qᴜᴇʀʏ]",
                switch_pm_parameter="inline",
            )
        judul = inline_query.query.split(None, 1)[1].strip()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42"
        }
        search_results = requests.get(
            f"https://www.google.com/search?q={judul}&num=20", headers=headers
        )
        soup = BeautifulSoup(search_results.text, "lxml")
        data = []
        for result in soup.find_all("div", class_="kvH3mc BToiNc UK95Uc"):
            link = result.find("div", class_="yuRUbf").find("a").get("href")
            title = result.find("div", class_="yuRUbf").find("h3").get_text()
            try:
                snippet = result.find(
                    "div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"
                ).get_text()
            except Exception:
                snippet = "-"
            message_text = f"ᴛɪᴛʟᴇ:  {title}\n ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ : {snippet}"
            data.append(
                InlineQueryResultArticle(
                    title=f"{title}",
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=False,
                    ),
                    url=link,
                    description=snippet,
                    thumb_url="https://te.legra.ph/file/ed8ea62ae636793000bb4.jpg",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(text="ᴏᴘᴇɴ ᴡᴇʙꜱɪᴛᴇ", url=link),
                                InlineKeyboardButton(text="sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", switch_inline_query_current_chat="google")
                            ]
                        ]
                    ),
                )
            )
        await inline_query.answer(
            results=data,
            is_gallery=False,
            is_personal=False,
            next_offset="",
            switch_pm_text=f"​ғᴏᴜɴᴅ ​{len(data)} ʀᴇꜱᴜʟᴛꜱ",
            switch_pm_parameter="google",
        )
    elif inline_query.query.strip().lower().split()[0] == "pypi":
        if len(inline_query.query.strip().lower().split()) < 2:
            return await inline_query.answer(
                results=[],
                switch_pm_text="ᴘʏᴘɪ ꜱᴇᴀʀᴄʜ | ᴘʏᴘɪ [Qᴜᴇʀʏ]",
                switch_pm_parameter="inline",
            )
        query = inline_query.query.split(None, 1)[1].strip()
        search_results = requests.get(f"https://yasirapi.eu.org/pypi?q={query}")
        srch_results = search_results.json()
        data = []
        for sraeo in srch_results["result"]:
            title = sraeo.get("name")
            link = sraeo.get("url")
            deskripsi = sraeo.get("description")
            version = sraeo.get("version")
            created = sraeo.get("created")
            message_text = f"ᴛɪᴛʟᴇ : {title}\n ᴠᴇʀꜱɪᴏɴ : {version}\n ᴄʀᴇᴀᴛᴇᴅ: {created}\nᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ : {deskripsi}"
            data.append(
                InlineQueryResultArticle(
                    title=f"{title}",
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=False,
                    ),
                    url=link,
                    description=deskripsi,
                    thumb_url="https://raw.githubusercontent.com/github/explore/666de02829613e0244e9441b114edb85781e972c/topics/pip/pip.png",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ʟɪɴᴋ", url=link),
                                InlineKeyboardButton(text="sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", switch_inline_query_current_chat="pypi")
                            ]
                        ]
                    ),
                )
            )
        await inline_query.answer(
            results=data,
            is_gallery=False,
            is_personal=False,
            next_offset="",
            switch_pm_text=f"​ғᴏᴜɴᴅ​ {len(data)} ʀᴇꜱᴜʟᴛꜱ",
            switch_pm_parameter="pypi",
        )
    elif inline_query.query.strip().lower().split()[0] == "whisper":
        if len(inline_query.query.strip().lower().split()) < 3:
            return await inline_query.answer(
                results=[],
                switch_pm_text="SecretMsg | secretmsg [USERNAME/ID] [MESSAGE]",
                switch_pm_parameter="inline",
            )
        _id = inline_query.query.split()[1]
        msg = inline_query.query.split(None, 2)[2].strip()

        if not msg or not msg.endswith(":"):
            inline_query.stop_propagation()

        try:
            penerima = await Mukesh.get_users(_id.strip())
        except Exception:  # pylint: disable=broad-except
            inline_query.stop_propagation()
            return

        PRVT_MSGS[inline_query.id] = (
            penerima.id,
            penerima.first_name,
            inline_query.from_user.id,
            msg.strip(": "),
        )
        prvte_msg = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Show Message 🔐", callback_data=f"prvtmsg({inline_query.id})"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Destroy☠️ this msg",
                        callback_data=f"destroy({inline_query.id})",
                    )
                ],
            ]
        )
        mention = (
            f"@{penerima.username}"
            if penerima.username
            else f"<a href='tg://user?id={penerima.id}'>{penerima.first_name}</a>"
        )
        msg_c = (
            f"🔒 A <b>private message</b> to {mention} [<code>{penerima.id}</code>], "
        )
        msg_c += "Only he/she can open it."
        results = [
            InlineQueryResultArticle(
                title=f"A Private Msg to {penerima.first_name}",
                input_message_content=InputTextMessageContent(msg_c),
                description="Only he/she can open it",
                thumb_url="https://te.legra.ph/file/16133ab3297b3f73c8da5.png",
                reply_markup=prvte_msg,
            )
        ]
        await inline_query.answer(
            results=results, 
            is_gallery=False,
            is_personal=False,
            next_offset="",
            switch_pm_parameter="whisper"
        )
    elif inline_query.query.strip().lower().split()[0] == "github":
        if len(inline_query.query.strip().lower().split()) < 2:
            return await inline_query.answer(
                results=[],
                switch_pm_text="​ɢɪᴛʜᴜʙ ɢɪᴛ |ɢɪᴛ | ǫᴜᴇʀʏ​ ",
                switch_pm_parameter="inline",
            )
        query = inline_query.query.split(None, 1)[1].strip()
        search_results = requests.get(
            f"https://api.github.com/search/repositories?q={query}"
        ).json()
        item = search_results.get("items")
        data = []
        for sraeo in item:
            title = sraeo.get("full_name")
            link = sraeo.get("html_url")
            deskripsi = sraeo.get("description")
            lang = sraeo.get("language")

            size = sraeo.get("size")
            message_text = f":ᴛɪᴛʟᴇ : {title}\n\n│🍴ꜰᴏʀᴋꜱ : {sraeo.get('forks')}   ┃┃    🌟ꜱᴛᴀʀꜱ : {sraeo.get('stargazers_count')}\n\n"

            message_text += f"ʟᴀɴɢᴜᴀɢᴇ:  {lang}  ┃┃   ꜱɪᴢᴇ : {round(size/1024,2)} ᴍʙ\n\nᴄʀᴇᴀᴛᴇᴅ ᴀᴛ :  {sraeo.get('created_at')}\nʟᴀꜱᴛ ᴜᴘᴅᴀᴛᴇ : {sraeo.get('updated_at')}\n"
            message_text += f"ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ : {deskripsi}"
            data.append(
                InlineQueryResultArticle(
                    title=f"{title}",
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    ),
                    url=link,
                    description=deskripsi,
                    thumb_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="ᴏᴘᴇɴ ɢɪᴛʜᴜʙ ʟɪɴᴋ", url=link),
                         InlineKeyboardButton(text="sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", switch_inline_query_current_chat="github")]]
                    ),
                )
            )
        await inline_query.answer(
            results=data,
            is_gallery=False,
            is_personal=False,
            next_offset="",
            switch_pm_text=f"​ғᴏᴜɴᴅ​ {len(data)} ʀᴇꜱᴜʟᴛꜱ",
            switch_pm_parameter="github",
        )
__help__=f"""ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ, ᴊᴜsᴛ ᴛʏᴘᴇ ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ [@{BOT_USERNAME}] ᴡɪᴛʜ ғᴏʟʟᴏᴡɪɴɢ ᴀʀɢs ʙᴇʟᴏᴡ.
~ pypi [query] - sᴇᴀʀᴄʜ ᴘᴀᴄᴋᴀɢᴇ ғʀᴏᴍ ᴘʏᴘɪ.
~ github [query] - sᴇᴀʀᴄʜ ɪɴ ɢɪᴛ.
~ google [ǫᴜᴇʀʏ] - sᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ."""
__mod_name__ = "ɪɴʟɪɴᴇ"
