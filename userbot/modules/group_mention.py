# credits: mrconfused
# Recode by @mrismanaziz
# t.me/SharingUserbot

import asyncio

from userbot import BOTLOG_CHATID
from userbot.events import register


@register(outgoing=True, incoming=True, func=lambda e: e.mentioned)
async def log_tagged_messages(event):
    hmm = await event.get_chat()

    if BOTLOG_CHATID:
        sender = await event.get_sender()
        await asyncio.sleep(5)
        if not event.is_private and not (await event.get_sender()).bot:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"<b>📨 #TAGS #MENERUSKAN</b> \n<b> • Dari : </b><a href = 'tg://user?id={sender.id}'>{sender.first_name}</a>\
			\n<b> • Grup : </b><code>{hmm.title}</code>\
                        \n<b> • 👀 </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'>Lihat Pesan</a>",
                parse_mode="html",
                link_preview=True,
            )
            e = await event.client.get_entity(int(BOTLOG_CHATID))
            fwd_message = await event.client.forward_messages(
                e, event.message, silent=True
            )
        else:
            if event.is_private:
                if not (await event.get_chat()).bot:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"<b>📨 #TAGS</b> \n<b> • Dari : </b><a href = 'tg://user?id={sender.id}'>{sender.first_name}</a>\
                                \n<b> • User ID : </b><code>{sender.id}</code>",
                        parse_mode="html",
                        link_preview=True,
                    )
                    e = await event.client.get_entity(int(BOTLOG_CHATID))
                    fwd_message = await event.client.forward_messages(
                        e, event.message, silent=True
                    )
