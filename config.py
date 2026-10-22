import os

try:
    from dotenv import load_dotenv
    load_dotenv()  # loads .env for local runs; host env vars still win
except ImportError:
    pass


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _optional(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _int(name: str, default: int = 0) -> int:
    raw = _optional(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        raise RuntimeError(f"Environment variable {name} must be a number, got: {raw!r}")


API_ID = 31862898
API_HASH = "c0e5fa94ba15a7d8fd4a883c21db2afe"
BOT_TOKEN = "8781475628:AAFhetyDEYXHod7RVnalPN8SCVhCjKEp9gg"
STRING_SESSION = "BQHmMHIAV8Htpyl8gXYIMbE8o0TGdvRaEEfBNLaCUfNPkpE_8b5xonEjOr2XEUNVWjEjCZvjBkgA6vkpR8ONrEt8BH33N6Ukz3uGcEo1YLEmnrUZ6_7elxNeQ3t5R2UPO4VZ1nBEMoIinKMcnWwv04UTvWmSS3DZhqStLzCmt-4IFb1JSELXm9HqdR8V2X6iUnLfThF4ZWhGLyOq7HdALSu3BEji-l5tSZhzhCWyC49pHSaN4d4WuYMWff4ktjXin7NuVdL9fXBrYGFHA9DdpzgGAFsWQn9yg5VlB3dyf1trfqS75ckwXLqPWQ2jow85ynpEVJyOI0M-UOzB1vQ4c5zA_GoCZgAAAAILnKT9AA"
OWNER_ID = 8734813395
STREAM_URL = "https://eu8.fastcast4u.com/proxy/clyedupq/stream"
CHANNEL_USERNAME = "Sukuna X Music"
CHANNEL_LINK = "https://t.me/youcanplaymusicbyurchoice"

if not BOT_TOKEN and not STRING_SESSION:
    raise RuntimeError(
        "Set BOT_TOKEN or STRING_SESSION. Voice-chat streaming needs a user session."
    )
