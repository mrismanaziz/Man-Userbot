# imported from ppe-remix by @heyworld & @DeletedUser420
# Based Code by @adekmaulana
# Improve by @aidilaryanto
import os
import random
from asyncio import sleep

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import man_cmd
from userbot.utils import deEmojify


@bot.on(man_cmd(outgoing=True, pattern=r"waifu(?: |$)(.*)"))
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
            silent=bool(animu.is_reply),
            hide_via=True,
        )

    except Exception:
        return await animu.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )
    await sleep(5)
    await animu.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"hz(:? |$)(.*)?"))
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
            elif reply_message.gif:
                m = "/hazmat"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
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
        "waifu": f"**Plugin : **`waifu`\
        \n\n  •  **Syntax :** `{cmd}waifu <text>`\
        \n  •  **Function : **Untuk Mengcuston sticer anime dengan text yg di tentukan.\
        \n\n  •  **Syntax :** `{cmd}hz` or `{cmd}hz [flip, x2, rotate (degree), background (number), black]`\
        \n  •  **Function : **Reply ke image / sticker yang sesuai!\
    "
    }
)
