# ported from paperplaneExtended by avinashreddy3108 for media support
import re

from telethon import events
from telethon.utils import get_display_name

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.modules.sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from userbot.utils import edit_or_reply, man_cmd


@bot.on(events.NewMessage(incoming=True))
async def filter_incoming_handler(event):
    name = event.raw_text
    filters = get_filters(event.chat_id)
    if not filters:
        return
    a_user = await event.get_sender()
    chat = await event.get_chat()
    me = await event.client.get_me()
    if event.sender_id == me.id:
        return
    title = get_display_name(await event.get_chat()) or "this chat"
    participants = await event.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            file_media = None
            filter_msg = None
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                file_media = msg_o.media
                filter_msg = msg_o.message
                link_preview = True
            elif trigger.reply:
                filter_msg = trigger.reply
                link_preview = False
            await event.reply(
                filter_msg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                link_preview=link_preview,
            )


@man_cmd(pattern="filter (.*)")
async def add_new_filter(event):
    "To save the filter"
    value = event.pattern_match.group(1).split(None, 1)
    keyword = value[0]
    try:
        string = value[1]
    except IndexError:
        string = None
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#FILTER\
            \nCHAT ID: {event.chat_id}\
            \nTRIGGER: {keyword}\
            \n\nThe following message is saved as the filter's reply data for the chat, please do NOT delete it !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "__Saving media as reply to the filter requires the__ `PRIVATE_GROUP_BOT_API_ID` __to be set.__",
            )
            return
    elif msg and msg.text and not string:
        string = msg.text
    elif not string:
        return await edit_or_reply(event, "__What should i do ?__")
    success = "`Filter` **{}** `{} successfully`"
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "added"))
    remove_filter(str(event.chat_id), keyword)
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "Updated"))
    await edit_or_reply(event, f"Error while setting filter for {keyword}")


@man_cmd(pattern="filters$")
async def on_snip_list(event):
    OUT_STR = "There are no filters in this chat."
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "There are no filters in this chat.":
            OUT_STR = "Active filters in this chat:\n"
        OUT_STR += "👉 `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="Available Filters in the Current Chat",
        file_name="filters.text",
    )


@man_cmd(pattern="stop ([\s\S]*)")
async def remove_a_filter(event):
    filt = event.pattern_match.group(1)
    if not remove_filter(event.chat_id, filt):
        await event.edit("Filter` {} `doesn't exist.".format(filt))
    else:
        await event.edit("Filter `{} `was deleted successfully".format(filt))


@man_cmd(pattern="rmallfilters$")
async def on_all_snip_delete(event):
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, "filters in current chat deleted successfully")
    else:
        await edit_or_reply(event, "There are no filters in this group")


CMD_HELP.update(
    {
        "filter": f"**Plugin : **`filter`\
        \n\n  •  **Syntax :** `{cmd}filters`\
        \n  •  **Function : **Melihat filter userbot yang aktif di obrolan.\
        \n\n  •  **Syntax :** `{cmd}filter` <keyword> <balasan> atau balas ke pesan ketik `.filter` <keyword>\
        \n  •  **Function : **Membuat filter di obrolan, Bot Akan Membalas Jika Ada Yang Menyebut 'keyword' yang dibuat. Bisa dipakai ke media/sticker/vn/file.\
        \n\n  •  **Syntax :** `{cmd}stop` <keyword>\
        \n  •  **Function : **Untuk Nonaktifkan Filter.\
        \n\n  •  **Syntax :** `{cmd}rmallfilters`\
        \n  •  **Function : **Menghapus semua filter yang ada di grup.\
    "
    }
)
