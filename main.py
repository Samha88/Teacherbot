import asyncio
from telethon import TelegramClient, events
from aiohttp import web

api_id = 22707838
api_hash = '7822c50291a41745fa5e0d63f21bbfb6'
session_name = 'my_session'

admin_chat_id = 7577774656
target_bot = 'DiamondIchancyBot'

monitoring_enabled = True

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=admin_chat_id, pattern=r'/monitor (on|off)'))
async def toggle_monitor(event):
    global monitoring_enabled
    state = event.pattern_match.group(1)
    monitoring_enabled = (state == 'on')
    await event.reply(f"Monitoring is now {'enabled' if monitoring_enabled else 'disabled'}.")

@client.on(events.NewMessage(from_users=target_bot))
async def handle_bot_message(event):
    global monitoring_enabled

    if not monitoring_enabled:
        return

    # مباشرة يرسل نفس الرسالة للبوت
    copied_code = event.raw_text.strip()
    if copied_code:
        await client.send_message(target_bot, copied_code)
        print(f"أُرسل الكود: {copied_code}")

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
