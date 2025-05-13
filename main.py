import asyncio
from telethon import TelegramClient, events, Button
from aiohttp import web
import time

api_id = 22707838
api_hash = '7822c50291a41745fa5e0d63f21bbfb6'
session_name = 'my_session'

admin_chat_id = 7577774656
target_bot = 'teacher_ichancy_bot'

monitoring_enabled = True
copied_code = ""
last_start_time = 0  # لتتبع آخر مرة أرسل فيها /start

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=admin_chat_id, pattern=r'/monitor (on|off)'))
async def toggle_monitor(event):
    global monitoring_enabled
    state = event.pattern_match.group(1)
    monitoring_enabled = (state == 'on')
    await event.reply(f"Monitoring is now {'enabled' if monitoring_enabled else 'disabled'}.")

@client.on(events.NewMessage(from_users=target_bot))
async def handle_bot_message(event):
    global copied_code, last_start_time

    if not monitoring_enabled:
        return

    if "كود" in event.raw_text or "code" in event.raw_text.lower():
        # استخراج الكود من الرسالة
        lines = event.raw_text.split()
        for word in lines:
            if len(word) > 4:
                copied_code = word
                break

        # حماية من التكرار: انتظار دقيقة قبل إرسال /start
        current_time = time.time()
        if current_time - last_start_time < 60:
            print("تجاوز إرسال /start لتجنب الحظر المؤقت")
            return
        last_start_time = current_time

        await client.send_message(target_bot, '/start')

        response = await client.wait_event(events.NewMessage(from_users=target_bot))
        buttons = response.buttons

        # البحث عن زر يحتوي كلمة "كود"
        clicked = False
        for row in buttons:
            for btn in row:
                if 'كود' in btn.text or 'code' in btn.text.lower():
                    await btn.click()
                    clicked = True
                    break
            if clicked:
                break

        await asyncio.sleep(0.3)
        await client.send_message(target_bot, copied_code)

# Web server for Render
async def handle(request):
    return web.Response(text="Userbot is running")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

async def main():
    await client.start()
    print("Userbot Started")
    await start_web_server()
    await client.run_until_disconnected()

asyncio.run(main())
