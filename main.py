import asyncio
import logging

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    STRING_SESSION,
    OWNER_ID,
    STREAM_URL,
    CHANNEL_USERNAME,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sukuna-x-music")

# Voice-chat streaming needs a user session. Bots cannot join voice chats.
# If STRING_SESSION is set it is used; otherwise the bot token client is used
# (commands will work, but /radio will likely fail to join the call).
if STRING_SESSION:
    app = Client("sukuna_radio", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
else:
    app = Client("sukuna_radio_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

calls = PyTgCalls(app)
active_chats: set[int] = set()  # chats currently streaming


async def is_authorized(message: Message) -> bool:
    """Only the owner and group admins may control the radio."""
    # Anonymous admins post as the group itself.
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        return True
    user = message.from_user
    if not user:
        return False
    if OWNER_ID and user.id == OWNER_ID:
        return True
    try:
        member = await app.get_chat_member(message.chat.id, user.id)
    except Exception:
        log.exception("Could not check admin status")
        return False
    return member.status in (
        enums.ChatMemberStatus.OWNER,
        enums.ChatMemberStatus.ADMINISTRATOR,
    )


@app.on_message(filters.command(["start", "help"]) & filters.private & filters.incoming)
async def start_command(_, message: Message):
    await message.reply_text(
        "🎧 **Sukuna X Music Radio**\n\n"
        "Add me to your group and start a voice chat there.\n"
        "`/radio` — start the stream in this group's voice chat (admins only)\n"
        "`/stopradio` — stop streaming (admins only)\n"
        "`/radiohelp` — show help"
    )


@app.on_message(filters.command(["radiohelp", "help_radio"]) & filters.incoming)
async def radio_help(_, message: Message):
    await message.reply_text(
        "🎵 **Radio commands**\n"
        "`/radio` — start the stream in the current group's voice chat\n"
        "`/stopradio` — stop the stream\n\n"
        "Start a voice chat in the group first. Only group admins and the owner "
        "can use these commands."
    )


@app.on_message(filters.command("radio") & filters.group)
async def radio_command(_, message: Message):
    if not await is_authorized(message):
        await message.reply_text("⛔ Only group admins can start the radio.")
        return
    if not STREAM_URL:
        await message.reply_text("Set the STREAM_URL environment variable first.")
        return

    chat_id = message.chat.id
    try:
        await calls.play(chat_id, MediaStream(STREAM_URL))
        active_chats.add(chat_id)
        await message.reply_text("📻 Radio stream started.")
    except Exception as exc:
        log.exception("Could not start stream")
        await message.reply_text(
            "Couldn't start the radio. Make sure a voice chat is already active, "
            "the stream URL is direct/reachable, and the account has permission to join.\n"
            f"Error: `{type(exc).__name__}: {exc}`"
        )


@app.on_message(filters.command("stopradio") & filters.group)
async def stop_radio(_, message: Message):
    if not await is_authorized(message):
        await message.reply_text("⛔ Only group admins can stop the radio.")
        return

    chat_id = message.chat.id
    try:
        await calls.leave_call(chat_id)
        active_chats.discard(chat_id)
        await message.reply_text("⏹️ Radio stopped.")
    except Exception as exc:
        log.exception("Could not stop stream")
        await message.reply_text(
            f"No active stream found, or stop failed: `{type(exc).__name__}`"
        )


@app.on_message(filters.command("channelpost") & filters.private & filters.incoming)
async def channel_post(_, message: Message):
    # Only the configured owner can post.
    if not message.from_user or not OWNER_ID or message.from_user.id != OWNER_ID:
        await message.reply_text("⛔ You are not authorized.")
        return

    if not CHANNEL_USERNAME:
        await message.reply_text(
            "Set CHANNEL_USERNAME (e.g. `@yourchannel` or the numeric channel ID) first."
        )
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.reply_text("Usage:\n/channelpost Your message here")
        return

    # Numeric IDs must be passed as int; usernames as str.
    target = CHANNEL_USERNAME
    if target.lstrip("-").isdigit():
        target = int(target)

    try:
        await app.send_message(target, parts[1])
        await message.reply_text("✅ Message posted to your channel!")
    except Exception as exc:
        log.exception("Channel post failed")
        await message.reply_text(f"❌ Could not post: {type(exc).__name__}: {exc}")


async def main():
    await app.start()
    await calls.start()
    log.info("Sukuna X Music is online")
    # Keep the process alive for Render/Docker/worker hosting.
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
