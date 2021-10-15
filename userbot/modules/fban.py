# Copyright (C) 2020 KenHV

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import man_cmd

fban_replies = [
    "New FedBan",
    "Starting a federation ban",
    "Start a federation ban",
    "FedBan Reason update",
    "FedBan reason updated",
    "has already been fbanned, with the exact same reason.",
]

unfban_replies = ["New un-FedBan", "I'll give", "Un-FedBan"]


@bot.on(man_cmd(outgoing=True, pattern=r"(d)?fban(?: |$)(.*)"))
async def fban(event):
    """Bans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    match = event.pattern_match.group(2)

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        fban_id = reply_msg.sender_id

        if event.pattern_match.group(1) == "d":
            await reply_msg.delete()

        reason = match
    else:
        pattern = match.split()
        fban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        fban_id = await event.client.get_peer_id(fban_id)
    except Exception:
        pass

    if event.sender_id == fban_id:
        return await event.edit(
            "**Error: Tindakan ini telah dicegah oleh protokol keamanan diri Man-UserBot.**"
        )

    fed_list = get_flist()
    if len(fed_list) == 0:
        return await event.edit("**Anda belum terhubung ke federasi mana pun!**")

    user_link = f"[{fban_id}](tg://user?id={fban_id})"

    await event.edit(f"**Fbanning** {user_link}...")
    failed = []
    total = 0

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

                if all(i not in reply.text for i in fban_replies):
                    failed.append(i.fed_name)
        except Exception:
            failed.append(i.fed_name)

    reason = reason or "Not specified."

    if failed:
        status = f"Failed to fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! Fbanned in {total} feds."

    await event.edit(
        f"**Fbanned **{user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"unfban(?: |$)(.*)"))
async def unfban(event):
    """Unbans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    match = event.pattern_match.group(1)
    if event.is_reply:
        unfban_id = (await event.get_reply_message()).sender_id
        reason = match
    else:
        pattern = match.split()
        unfban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        unfban_id = await event.client.get_peer_id(unfban_id)
    except BaseException:
        pass

    if event.sender_id == unfban_id:
        return await event.edit("**Tunggu, itu illegal**")

    fed_list = get_flist()
    if len(fed_list) == 0:
        return await event.edit("**Anda belum terhubung ke federasi mana pun!**")

    user_link = f"[{unfban_id}](tg://user?id={unfban_id})"

    await event.edit(f"**Un-fbanning **{user_link}**...**")
    failed = []
    total = 0

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

                if all(i not in reply.text for i in unfban_replies):
                    failed.append(i.fed_name)
        except Exception:
            failed.append(i.fed_name)

    reason = reason or "Not specified."

    if failed:
        status = f"Failed to un-fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! Un-fbanned in {total} feds."

    reason = reason or "Not specified."
    await event.edit(
        f"**Un-fbanned** {user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"addf(?: |$)(.*)"))
async def addf(event):
    """Adds current chat to connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import add_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    fed_name = event.pattern_match.group(1)
    if not fed_name:
        return await event.edit("**Berikan nama untuk terhubung ke grup ini!**")

    try:
        add_flist(event.chat_id, fed_name)
    except IntegrityError:
        return await event.edit("**Grup ini sudah terhubung ke daftar federasi.**")

    await event.edit("**Menambahkan grup ini ke daftar federasi!**")


@bot.on(man_cmd(outgoing=True, pattern=r"delf$"))
async def delf(event):
    """Removes current chat from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist(event.chat_id)
    await event.edit("**Menghapus grup ini dari daftar federasi!**")


@bot.on(man_cmd(outgoing=True, pattern=r"listf$"))
async def listf(event):
    """List all connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    fed_list = get_flist()
    if len(fed_list) == 0:
        return await event.edit("**Anda belum terhubung ke federasi mana pun!**")

    msg = "**Connected federations:**\n\n"

    for i in fed_list:
        msg += f"• {i.fed_name}\n"

    await event.edit(msg)


@bot.on(man_cmd(outgoing=True, pattern=r"clearf$"))
async def clearf(event):
    """Removes all chats from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist_all
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_flist_all()
    await event.edit("**Disconnected dari semua federasi yang terhubung!**")


CMD_HELP.update(
    {
        "fban": "**Plugin : **`Federations Banned`\
        \n\n  •  **Syntax :** `.fban` <id/username/reply> <reason>\
        \n  •  **Function : **Membanned user dari federasi yang terhubung.\
        \n\n  •  **Syntax :** `.dfban` <id/username/reply> <reason>\
        \n  •  **Function : **Membanned user dari federasi yang terhubung dengan menghapus pesan yang dibalas.\
        \n\n  •  **Syntax :** `.unfban` <id/username/reply> <reason>\
        \n  •  **Function : **Membatalkan Federations Banned\
        \n\n  •  **Syntax :** `.addf` <nama>\
        \n  •  **Function : **Menambahkan grup saat ini dan menyimpannya sebagai <nama> di federasi yang terhubung. Menambahkan satu grup sudah cukup untuk satu federasi.\
        \n\n  •  **Syntax :** `.delf`\
        \n  •  **Function : **Menghapus grup saat ini dari federasi yang terhubung\
        \n\n  •  **Syntax :** `.listf`\
        \n  •  **Function : **Mencantumkan semua federasi yang terhubung dengan nama yang ditentukan.\
        \n\n  •  **Syntax :** `.clearf`\
        \n  •  **Function : **Menghapus dari semua federasi yang terhubung. Gunakan dengan hati-hati.\
    "
    }
)
