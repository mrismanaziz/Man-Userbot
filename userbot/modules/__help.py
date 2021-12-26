# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# @Qulec tarafından yazılmıştır.
# Thanks @Spechide.

from telethon.errors.rpcerrorlist import BotInlineDisabledError as noinline
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import BOT_USERNAME
from userbot import CMD_HANDLER as cmd
from userbot import bot
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="helpme")
async def _(event):
    if event.fwd_from:
        return
    if BOT_USERNAME is not None:
        chat = "@Botfather"
        try:
            results = await event.client.inline_query(BOT_USERNAME, "@SharingUserbot")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except noinline:
            xx = await edit_or_reply(
                event,
                "**Inline Mode Tidak aktif.**\n__Sedang Menyalakannya, Harap Tunggu Sebentar...__",
            )
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(BOT_USERNAME)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("Search")
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    await event.client(UnblockRequest(chat))
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(BOT_USERNAME)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("Search")
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                await xx.edit(
                    f"**Berhasil Menyalakan Mode Inline**\n\n**Ketik** `{cmd}helpme` **lagi untuk membuka menu bantuan.**"
                )
            await bot.delete_messages(
                conv.chat_id,
                [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id],
            )
    else:
        await edit_or_reply(
            event,
            "**Silahkan Buat BOT di @BotFather dan Tambahkan Var** `BOT_TOKEN` & `BOT_USERNAME`",
        )
