# imported from ppe-remix by @heyworld & @DeletedUser420
# Based Code by @adekmaulana
# Improve by @aidilaryanto
import os
import random
import re
from asyncio import sleep

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


@register(outgoing=True, pattern="^.waifu(?: |$)(.*)")
async def waifu(animu):
    # """Generate random waifu sticker with the text!"""

    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`No text given, hence the waifu ran away.`")
            return
    animus = [15, 30, 32, 33, 40, 41, 42, 48, 55, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    try:
        await sticcers[0].click(
            animu.chat_id,
            reply_to=animu.reply_to_msg_id,
            silent=True if animu.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await animu.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )
    await sleep(5)
    await animu.delete()


@register(outgoing=True, pattern=r"^.hz(:? |$)(.*)?")
async def _(hazmat):
    await hazmat.edit("`Sending information...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await hazmat.edit("`WoWoWo Capt!, we are not going suit a ghost!...`")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await hazmat.edit("`Word can destroy anything Capt!...`")
        return
    chat = "@hazmat_suit_bot"
    await hazmat.edit("```Suit Up Capt!, We are going to purge some virus...```")
    message_id_to_reply = hazmat.message.reply_to_msg_id
    msg_reply = None
    async with hazmat.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/hazmat {level}"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            elif reply_message.gif:
                m = f"/hazmat"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.reply("`Please unblock` @hazmat_suit_bot`...`")
            return
        if response.text.startswith("I can't"):
            await hazmat.edit("`Can't handle this GIF...`")
            await hazmat.client.delete_messages(
                conv.chat_id, [msg.id, response.id, r.id, msg_reply.id]
            )
            return
        else:
            downloaded_file_name = await hazmat.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            await hazmat.client.send_file(
                hazmat.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply,
            )
            """ - cleanup chat after completed - """
            if msg_reply is not None:
                await hazmat.client.delete_messages(
                    conv.chat_id, [msg.id, msg_reply.id, r.id, response.id]
                )
            else:
                await hazmat.client.delete_messages(conv.chat_id, [msg.id, response.id])
    await hazmat.delete()
    return os.remove(downloaded_file_name)


CMD_HELP.update(
    {
        "waifu": "**Plugin : **`waifu`\
        \n\n  •  **Syntax :** `.waifu <text>`\
        \n  •  **Function : **Untuk Mengcuston sticer anime dengan text yg di tentukan.\
        \n\n  •  **Syntax :** `.hz` or `.hz [flip, x2, rotate (degree), background (number), black]`\
        \n  •  **Function : **Reply ke image / sticker yang sesuai!\
    "
    }
)
