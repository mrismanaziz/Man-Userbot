# Based Code by @adekmaulana
# Improve by @aidilaryanto
#
#
import os

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="hz(:? |$)(.*)?")
async def _(hazmat):
    xx = await edit_or_reply(hazmat, "`Processing Hazmat...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await xx.edit("**Mohon Balas Ke Sticker/Gambar**")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await xx.edit("`Kata Bisa Menghancurkan Apapun`")
        return
    chat = "@hazmat_suit_bot"
    await xx.edit("`Perintah Hazmat Diaktifkan, Sedang Memproses...`")
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
            await hazmat.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.client(UnblockRequest(chat))
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
            await hazmat.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("I can't"):
            await xx.edit("`Mohon Maaf, GIF Tidak Bisa...`")
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
        "hazmat": f"**Plugin : **`hazmat`\
        \n\n  •  **Syntax :** `{cmd}hz` atau `{cmd}hz [flip, x2, rotate (level), background (nomer), black]`\
        \n  •  **Function : **Balas ke gambar/sticker untuk menyesuaikan!\
    "
    }
)
