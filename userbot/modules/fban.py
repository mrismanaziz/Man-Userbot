# Copyright (C) 2020 KenHV

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, disable_edited=True, pattern=r"^\.fban(?: |$)(.*)")
async def fban(event):
    """Bans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    reply_msg = await event.get_reply_message()

    if reply_msg:
        fban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
        user_link = f"[{fban_id}](tg://user?id={fban_id})"
    elif not reply_msg:
        pattern = str(event.pattern_match.group(1)).split()
        fban_id = pattern[0]
        reason = " ".join(pattern[1:])
        user_link = fban_id
    else:
        return

    self_user = await event.client.get_me()

    if fban_id == self_user.id or fban_id == "@" + self_user.username:
        return await event.edit(
            "**Error: This action has been prevented by KensurBot self preservation protocols.**"
        )

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**You haven't connected to any federations yet!**")

    await event.edit(f"**Fbanning** {user_link}...")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/fban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("New FedBan" not in reply.text)
                    and ("Starting a federation ban" not in reply.text)
                    and ("Start a federation ban" not in reply.text)
                    and ("FedBan reason updated" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Fbanned in {total} feds."

    await event.edit(
        f"**Fbanned **{user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.unfban(?: |$)(.*)")
async def unfban(event):
    """Unbans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    reply_msg = await event.get_reply_message()

    if reply_msg:
        unfban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
        user_link = f"[{unfban_id}](tg://user?id={unfban_id})"
    elif not reply_msg:
        pattern = str(event.pattern_match.group(1)).split()
        unfban_id = pattern[0]
        reason = " ".join(pattern[1:])
        user_link = unfban_id
    else:
        return

    self_user = await event.client.get_me()

    if unfban_id == self_user.id or unfban_id == "@" + self_user.username:
        return await event.edit("**Wait, that's illegal**")

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**You haven't connected any federations yet!**")

    await event.edit(f"**Un-fbanning **{user_link}**...**")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/unfban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("New un-FedBan" not in reply.text)
                    and ("I'll give" not in reply.text)
                    and ("Un-FedBan" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to un-fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Un-fbanned in {total} feds."

    reason = reason if reason else "Not specified."
    await event.edit(
        f"**Un-fbanned** {user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^\.addf(?: |$)(.*)")
async def addf(event):
    """Adds current chat to connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import add_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if not (fed_name := event.pattern_match.group(1)):
        return await event.edit("**Pass a name in order connect to this group!**")

    try:
        add_flist(event.chat_id, fed_name)
    except IntegrityError:
        return await event.edit(
            "**This group is already connected to federations list.**"
        )

    await event.edit("**Added this group to federations list!**")


@register(outgoing=True, pattern=r"^\.delf$")
async def delf(event):
    """Removes current chat from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist(event.chat_id)
    await event.edit("**Removed this group from federations list!**")


@register(outgoing=True, pattern=r"^\.listf$")
async def listf(event):
    """List all connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**You haven't connected to any federations yet!**")

    msg = "**Connected federations:**\n\n"

    for i in fed_list:
        msg += "• " + str(i.fed_name) + "\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^\.clearf$")
async def delf(event):
    """Removes all chats from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist_all
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist_all()
    await event.edit("**Disconnected from all connected federations!**")


CMD_HELP.update(
    {
        "fban": "**Plugin : **`Federations Banned`\
        \n\n  •  **Syntax :** `.fban` <id/username/reply> <reason>\
        \n  •  **Function : **Bans user dari federasi yang terhubung.\
        \n\n  •  **Syntax :** `.unfban` <id/username/reply> <reason>\
        \n  •  **Function : **Membatalkan Federations Banned\
        \n\n  •  **Syntax :** `.addf` <nama>\
        \n  •  **Function : **Menambahkan grup saat ini dan menyimpannya sebagai <nama> di federasi yang terhubung. Menambahkan satu grup sudah cukup untuk satu federasi.\
        \n\n  •  **Syntax :** `.delf`\
        \n  •  **Function : **Menghapus grup saat ini dari federasi yang terhubung\
        \n\n  •  **Syntax :** `.listf`\
        \n  •  **Function : **Mencantumkan semua federasi yang terhubung dengan nama yang ditentukan.\
    "
    }
)
