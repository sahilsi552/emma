from pyrogram import filters
from pymongo import MongoClient

from MukeshRobot import pbot as app, MONGO_DB_URI

# Setup MongoDB
client = MongoClient(MONGO_DB_URI)
db = client['tagalert_db']
tagalert_collection = db['tagalert_collection']

# Tagalert command
@app.on_message(filters.command("tagalert") & filters.private)
async def tagalert_command(client, message):
    args = message.text.split()[1:]
    
    if len(args) == 0:
        await message.reply_text("Please provide either 'on' or 'off'")
        return
    
    status = args[0].lower()
    if status not in ['on', 'off']:
        await message.reply_text("Invalid status. Please provide either 'on' or 'off'")
        return
    
    # Update tagalert status in the database
    user_id = message.from_user.id
    tagalert_collection.update_one({"user_id": user_id}, {"$set": {"status": status}}, upsert=True)
    
    await message.reply_text(f"Tagalert notifications {'enabled' if status == 'on' else 'disabled'} successfully!")


@app.on_message(filters.group,group=10)
async def handle_mentions(client, message):
        
    try:
        user_id = message.reply_to_message.reply_to_message.from_user.id 
        print("user id",user_id)
        tagalert_status = tagalert_collection.find_one({"user_id": user_id})["status"]
        print(tagalert_status)
        tagalert_user=tagalert_collection.find_one({"user_id":user_id})["user_id"]
        print("tag user ",tagalert_user)
        if tagalert_status == 'on':
            group_title = message.chat.title
            print(group_title)
            sender_name = message.from_user.first_name
            tagged_message = message.text
            print(tagged_message)
            await client.send_message(tagalert_user, f"You were mentioned in group {group_title} by {sender_name}:\n{tagged_message}")
    except Exception as e:
        print(e)
        
__mod_name__= "Tᴀɢᴀʟᴇʀᴛ"

__help__ = """
──「 Help of Tagalert ‼️ 」── 

Too many mentions.. Cant you manage them all alone..

Commands (only work on bot inbox)
/tagalert <on/off> - to Enable Notifications For Tags Where Patricia Is

Example:
If you are mentioned in a group Merissa will tell you who mentioned you, message that you are tagged in and which group is that"""