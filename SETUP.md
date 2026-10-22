# Sukuna X Music — setup

## What it does
A starter Telegram radio bot that attempts to stream a direct audio URL into an already-active group voice chat. Use only streams/audio you have permission to rebroadcast.

## 1. Create Telegram credentials
1. Create a bot with `@BotFather` and copy its token.
2. Get `API_ID` and `API_HASH` from https://my.telegram.org.
3. Set `OWNER_ID` to your Telegram numeric ID (required for `/channelpost`).
4. If the voice-chat library/account configuration requires a user account, create a Pyrogram `STRING_SESSION` using a trusted session generator. Never share it; it can grant access to your account.

## 2. Local setup
Install Python 3.11 and FFmpeg, then run:
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and fill in your values. `config.py` loads `.env` automatically for local runs; on a host, use its environment-variable settings instead. Never commit `.env` or put secrets in the code.

Start with:
```bash
python main.py
```

## 3. Render
Create a **Background Worker** service from your GitHub repository. Add `API_ID`, `API_HASH`, `BOT_TOKEN` (or `STRING_SESSION` where required), and `STREAM_URL` under Environment. Render's web service port is not needed for this worker. Set the start command to:
```bash
python main.py
```
Do not run two copies with the same Telegram session at the same time.

## 4. Commands
- `/start` — private start/help
- `/radio` — start the configured stream in the group
- `/stopradio` — stop the stream in the group
- `/radiohelp` — show commands
- `/channelpost <text>` — owner only, in private chat; posts to `CHANNEL_USERNAME` (use `@username` or the numeric ID, not the channel title; the account must be a channel admin)

`/radio` and `/stopradio` can be used by group admins and the owner only.

Start a voice chat in the group before running `/radio`. Ensure the bot/account is in the group and permitted to join voice chat. Some Telegram call libraries require a user session instead of a bot token; if joining fails, check the current PyTgCalls compatibility notes.

## Important notes
- `STREAM_URL` must be a direct audio stream endpoint, not a normal webpage or YouTube watch page.
- This is a starter scaffold, not a guarantee that every stream host or Telegram account type will work without adjustments.
- Keep `.env`, bot tokens, API hashes, and session strings private.
