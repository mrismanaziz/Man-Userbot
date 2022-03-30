# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Kalo mau ngecopas, jangan hapus credit ya goblok

from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from telethon.utils import get_peer_id

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, call_py
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply, man_cmd


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@man_cmd(pattern="startvc$")
@register(pattern=r"^\.startvcs$", sudo=True)
async def start_voice(c):
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await edit_or_reply(c, "`Voice Chat Started...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@man_cmd(pattern="stopvc$")
@register(pattern=r"^\.stopvcs$", sudo=True)
async def stop_voice(c):
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await edit_delete(c, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await edit_or_reply(c, "`Voice Chat Stopped...`")
    except Exception as ex:
        await edit_delete(c, f"**ERROR:** `{ex}`")


@man_cmd(pattern="vcinvite")
async def _(c):
    xxnx = await edit_or_reply(c, "`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 6))
    for p in botman:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await xxnx.edit(f"`{z}` **Orang Berhasil diundang ke VCG**")


@man_cmd(pattern="vctitle(?: |$)(.*)")
@register(pattern=r"^\.cvctitle$", sudo=True)
async def change_title(e):
    title = e.pattern_match.group(1)
    me = await e.client.get_me()
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await edit_delete(e, "**Silahkan Masukan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await edit_delete(e, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await edit_or_reply(e, f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await edit_delete(e, f"**ERROR:** `{ex}`")


@man_cmd(pattern="joinvc(?: |$)(.*)")
@register(pattern=r"^\.joinvcs(?: |$)(.*)", sudo=True)
async def _(event):
    Man = await edit_or_reply(event, "`Processing...`")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(chat_id)
        except Exception as e:
            return await Man.edit(f"**ERROR:** `{e}`")
    else:
        chat_id = event.chat_id
    file = "./userbot/resources/audio-man.mp3"
    if chat_id:
        try:
            await call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().pulse_stream,
            )
            await Man.edit(f"**Berhasil Begabung Ke Obrolan Suara {chat_id}**")
        except AlreadyJoinedError:
            await call_py.leave_group_call(chat_id)
            await Man.edit(
                "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan coba `.joinvc` lagi"
            )
        except Exception as ep:
            await Man.edit(f"`{ep}`")


@man_cmd(pattern="leavevc$")
@register(pattern=r"^\.leavevcs$", sudo=True)
async def vc_end(event):
    chat_id = event.chat_id
    chat = await event.get_chat()
    Man = await edit_or_reply(event, "`Processing...`")
    if chat_id:
        try:
            await call_py.leave_group_call(chat_id)
            await Man.edit(f"**Berhasil Turun dari Obrolan Suara {chat.title}**")
        except Exception:
            await edit_delete(Man, "**Tidak Sedang Bergabung di Obrolan Suara**")


CMD_HELP.update(
    {
        "vctools": f"**Plugin : **`vctools`\
        \n\n  •  **Syntax :** `{cmd}startvc`\
        \n  •  **Function : **Untuk Memulai voice chat group\
        \n\n  •  **Syntax :** `{cmd}stopvc`\
        \n  •  **Function : **Untuk Memberhentikan voice chat group\
        \n\n  •  **Syntax :** `{cmd}joinvc`\
        \n  •  **Function : **Untuk Bergabung ke voice chat group\
        \n\n  •  **Syntax :** `{cmd}leavevc`\
        \n  •  **Function : **Untuk Turun dari voice chat group\
        \n\n  •  **Syntax :** `{cmd}vctitle` <title vcg>\
        \n  •  **Function : **Untuk Mengubah title/judul voice chat group\
        \n\n  •  **Syntax :** `{cmd}vcinvite`\
        \n  •  **Function : **Mengundang Member group ke voice chat group\
    "
    }
)
