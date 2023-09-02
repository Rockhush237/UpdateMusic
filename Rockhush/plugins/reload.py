import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from strings import get_command
from Rockhush import app
from Rockhush.core.call import Rock
from Rockhush.misc import db
from Rockhush.utils.database import get_authuser_names, get_cmode
from Rockhush.utils.decorators import ActualAdminCB, AdminActual, language
from Rockhush.utils.formatters import alpha_to_int

### Multi-Lang Commands
RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(chat_id, filter="administrators")
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except Exception as e:
        await message.reply_text(
            "Failed to refresh admins list, make sure you promoted the bot."
        )
        print(e)


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"Please wait, rebooting {MUSIC_BOT_NAME} for your chat."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Anon.stop_stream(message.chat.id)
    except Exception as e:
        print(e)
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except Exception as e:
            print(e)
        try:
            db[chat_id] = []
            await Anon.stop_stream(chat_id)
        except Exception as e:
            print(e)
    return await mystic.edit_text(
        f"Successfully rebooted {MUSIC_BOT_NAME} for your chat, you can start playing again..."
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
        await CallbackQuery.message.reply_text(
            f"𝓒𝓵𝓸𝓼𝓮𝓭 𝓑𝔂 ➣ {CallbackQuery.from_user.mention}\n{CallbackQuery.from_user.mention} ➣ @Logs_Gban"
        )
    except Exception as e:
        print(e)


@app.on_callback_query(
    filters.regex("stop_downloading") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "Download already completed.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "Downloading already completed or cancelled.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "Downloading cancelled.", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"Downloading process cancelled by {CallbackQuery.from_user.mention}"
            )
        except Exception as e:
            print(e)
            return await CallbackQuery.answer(
                "Failed to cancel downloading...", show_alert=True
            )
    await CallbackQuery.answer(
        "Failed to recognize the ongoing task.", show_alert=True
    )
