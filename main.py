from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import re

api_id = 22707838
api_hash = '7822c50291a41745fa5e0d63f21bbfb6'
session_name = "my_session"
bot_username = "teacher_ichancy_bot"

allowed_chat_ids = [7577774656]
monitor_enabled = True

app = Client(session_name, api_id=api_id, api_hash=api_hash)


@app.on_message(filters.private & filters.command(["enable", "disable"]))
async def toggle_monitoring(client, message: Message):
    global monitor_enabled
    if message.from_user.id in allowed_chat_ids:
        if message.text == "/enable":
            monitor_enabled = True
            await message.reply("تم تفعيل مراقبة الأكواد.")
        else:
            monitor_enabled = False
            await message.reply("تم إيقاف مراقبة الأكواد.")
    else:
        await message.reply("ليس لديك صلاحية التحكم بالبوت.")

@app.on_message(filters.private & filters.text & filters.from_user(bot_username))
async def handle_message(client: Client, message: Message):
    if not monitor_enabled:
        return

    code = extract_gift_code(message.text)
    if code:
        print(f"تم استخراج الكود: {code}")

        await client.send_message(bot_username, "/start")
        await asyncio.sleep(2)

        last_msg = (await client.get_history(bot_username, limit=1))[0]
        if last_msg.reply_markup:
            for row in last_msg.reply_markup.inline_keyboard:
                for button in row:
                    if "كود" in button.text:
                        await button.click()
                        await asyncio.sleep(2)
                        await client.send_message(bot_username, code)
                        print("تم إرسال الكود")
                        return

def extract_gift_code(text):
    lines = text.splitlines()
    for line in lines:
        if re.fullmatch(r"[A-Za-z0-9]{6,}", line.strip()):
            return line.strip()
    return None

app.run()