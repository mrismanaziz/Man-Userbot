# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
)

from userbot import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Gambar Terlalu Kecil`"
PP_ERROR = "`Gagal Memproses Gambar`"
NO_ADMIN = "`Gagal dikarenakan Bukan Admin :)`"
NO_PERM = "`Tidak Mempunyai Izin!`"
NO_SQL = "`Berjalan Pada Mode Non-SQL`"

CHAT_PP_CHANGED = "`Berhasil Mengubah Profil Grup`"
CHAT_PP_ERROR = (
    "`Ada Masalah Dengan Memperbarui Foto,`"
    "`Mungkin Karna Bukan Admin,`"
    "`Atau Tidak Mempunyai Izin.`"
)
INVALID_MEDIA = "`Media Tidak Valid`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern=r"^\.setgpic$")
async def set_group_photo(gpic):
    if not gpic.is_group:
        await gpic.edit("`Mohon Lakukan Perintah Ini Di Grup.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        return await gpic.edit(NO_ADMIN)

    if replymsg and replymsg.media:
        await gpic.edit("`Mengubah Profil Grup`")
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern=r"^\.promote(?: |$)(.*)")
async def promote(promt):
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        return await promt.edit(NO_ADMIN)

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await promt.edit("`Promosikan Pengguna Sebagai Admin... Mohon Menunggu`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"  # Just in case.
    if not user:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Berhasil Mempromosikan Pengguna Ini Sebagai Admin!`")
        await sleep(5)
        await promt.delete()

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        return await promt.edit(NO_PERM)

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOSI\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {promt.chat.title}(`{promt.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.demote(?: |$)(.*)")
async def demote(dmod):
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await dmod.edit(NO_ADMIN)

    # If passing, declare that we're going to demote
    await dmod.edit("`Sedang Melepas Admin...`")
    rank = "Admin"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        return await dmod.edit(NO_PERM)
    await dmod.edit("`Admin Berhasil Dilepas!`")
    await sleep(5)
    await dmod.delete()

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#MENURUNKAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.ban(?: |$)(.*)")
async def ban(bon):
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await bon.edit(NO_ADMIN)

    user, reason = await get_user_from_event(bon)
    if not user:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Processing Banned...`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await bon.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await bon.edit(
            "`Saya tidak memiliki hak pesan nuking! Tapi tetap saja dia di banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(
            r"\\**#Banned_User**//"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
            f"**User ID:** `{str(user.id)}`\n"
            f"**Reason:** `{reason}`"
        )
    else:
        await bon.edit(
            r"\\**#Banned_User**//"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
            f"**User ID:** `{str(user.id)}`\n"
            f"**Action:** `Banned User by {ALIVE_NAME}`"
        )
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {bon.chat.title}(`{bon.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.unban(?: |$)(.*)")
async def nothanos(unbon):
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await unbon.edit(NO_ADMIN)

    # If everything goes well...
    await unbon.edit("`Processing Unban...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unban Berhasil Dilakukan!```")
        await sleep(3)
        await unbon.delete()

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await unbon.edit("`Sepertinya Terjadi Kesalahan!`")


@register(outgoing=True, pattern=r"^\.dmute(?: |$)(.*)")
async def spider(spdr):
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await spdr.edit(NO_SQL)

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await spdr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(spdr)
    if not user:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        return await spdr.edit("`Tidak Bisa Membisukan Diri Sendiri..（>﹏<）`")

    if user.id == 844432220:
        return await spdr.edit("`Gagal Mute Ke Man, Dia Adalah Pembuat Saya 🤪`")

    # If everything goes well, do announcing and mute
    await spdr.edit(
        r"\\**#DMute_User**//"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Action:** `DMute by {ALIVE_NAME}`"
    )
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit("`Error! Pengguna Sudah Dibisukan.`")
    else:
        try:
            await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await spdr.edit(
                    r"\\**#DMute_User**//"
                    f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                    f"**User ID:** `{user.id}`\n"
                    f"**Reason:** `{reason}`"
                )
            else:
                await spdr.edit(
                    r"\\**#DMute_User**//"
                    f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                    f"**User ID:** `{user.id}`\n"
                    f"**Action:** `DMute by {ALIVE_NAME}`"
                )

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                    f"GRUP: {spdr.chat.title}(`{spdr.chat_id}`)",
                )
        except UserIdInvalidError:
            return await spdr.edit("`Terjadi Kesalahan!`")


@register(outgoing=True, pattern=r"^\.undmute(?: |$)(.*)")
async def unmoot(unmot):
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await unmot.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("```Melakukan Unmute...```")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Kesalahan! Pengguna Sudah Tidak Dibisukan.`")
    else:

        try:
            await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(
                "```Berhasil Melakukan Unmute! User Sudah Tidak Lagi Dibisukan```"
            )
            await sleep(3)
            await unmot.delete()
        except UserIdInvalidError:
            return await unmot.edit("`Terjadi Kesalahan!`")

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unmot.chat.title}(`{unmot.chat_id}`)",
            )


@register(incoming=True)
async def muter(moot):
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                )
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, pattern=r"^\.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    # Admin or creator check
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await un_gmute.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        return await un_gmute.edit(NO_SQL)

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if not user:
        return

    # If pass, inform and start ungmuting
    await un_gmute.edit("```Membuka Global Mute Pengguna...```")

    if ungmute(user.id) is False:
        await un_gmute.edit("`Kesalahan! Pengguna Sedang Tidak Di Gmute.`")
    else:
        # Inform about success
        await un_gmute.edit("```Berhasil! Pengguna Sudah Tidak Lagi Dibisukan```")
        await sleep(3)
        await un_gmute.delete()

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)",
            )


@register(outgoing=True, pattern=r"^\.gmute(?: |$)(.*)")
async def gspider(gspdr):
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await gspdr.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        return await gspdr.edit(NO_SQL)

    user, reason = await get_user_from_event(gspdr)
    if not user:
        return

    self_user = await gspdr.client.get_me()

    if user.id == self_user.id:
        return await gspdr.edit("`Tidak Bisa Membisukan Diri Sendiri..（>﹏<）`")

    if user.id == 844432220:
        return await gspdr.edit("`Gagal Global Mute Ke Man, Dia Adalah Pembuat Saya 🤪`")

    # If pass, inform and start gmuting
    await gspdr.edit("`Berhasil Membisukan Pengguna!`")
    if gmute(user.id) is False:
        await gspdr.edit("`Kesalahan! Pengguna Sudah Dibisukan.`")
    else:
        if reason:
            await gspdr.edit(
                r"\\**#GMuted_User**//"
                f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:** `{user.id}`\n"
                f"**Reason:** `{reason}`"
            )
        else:
            await gspdr.edit(
                r"\\**#GMuted_User**//"
                f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:** `{user.id}`\n"
                f"**Action:** `Global Muted by {ALIVE_NAME}`"
            )

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GLOBALMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )


@register(outgoing=True, pattern=r"^\.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Grup Bersih, Tidak Menemukan Akun Terhapus.`"

    if con != "clean":
        await show.edit("`Mencari Akun Hantu/Terhapus/Zombie...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"`Menemukan` **{del_u}** `Akun Hantu/Terhapus/Zombie Dalam Grup Ini,"
                "\nBersihkan Itu Menggunakan Perintah .zombies clean`"
            )
        return await show.edit(del_status)

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await show.edit("`Bukan Admin Disini!`")

    await show.edit("`Menghapus Akun Terhapus... Tunggu Sedang Dalam Proses`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Tidak Memiliki Izin Banned Dalam Grup Ini`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"`Membersihkan` **{del_u}** `Akun Terhapus`"

    if del_a > 0:
        del_status = (
            f"Membersihkan **{del_u}** Akun Terhapus "
            f"\n**{del_a}** `Admin Akun Terhapus Tidak Bisa Dihapus.`"
        )
    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#MEMBERSIHKAN\n"
            f"Membersihkan **{del_u}** Akun Terhapus!"
            f"\nGRUP: {show.chat.title}(`{show.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.admins$")
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = f"<b>👑 Daftar Admin Grup {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n⚜️ {link}"
            else:
                mentions += f"\nAkun Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern=r"^\.pin(?: |$)(.*)")
async def pin(msg):
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await msg.edit(NO_ADMIN)

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        return await msg.edit("`Mohon Balas Ke Pesan Untuk Melakukan Pin.`")

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        return await msg.edit(NO_PERM)

    await msg.edit("`Berhasil Melakukan Pin!`")
    await sleep(2)
    await msg.delete()

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"NOTIF: {not is_silent}",
        )


@register(outgoing=True, pattern=r"^\.kick(?: |$)(.*)")
async def kick(usr):
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await usr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(usr)
    if not user:
        return await usr.edit("`Tidak Dapat Menemukan Pengguna.`")

    await usr.edit("`Melakukan Kick....`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await usr.edit(NO_PERM + f"\n{str(e)}")

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**\n**Alasan:** `{reason}`"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**"
        )
        await sleep(5)
        await usr.delete()

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@register(outgoing=True, pattern=r"^\.users ?(.*)")
async def get_users(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = "Pengguna Di {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nAkun Terhapus `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nAkun Terhapus `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Grup Ini Terlalu Besar Mengunggah Daftar Pengguna Sebagai File."
        )
        file = open("daftarpengguna.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "daftarpengguna.txt",
            caption="Pengguna Dalam Grup {}".format(title),
            reply_to=show.id,
        )
        remove("daftarpengguna.txt")


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Ketik Username Atau Balas Ke Pengguna!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.usersdel ?(.*)")
async def get_usersdel(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = "Daftar Akun Terhapus Di {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n👻 [{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
        #                mentions += f"\nAkun Terhapus `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
    #              mentions += f"\nAkun Terhapus `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Grup Ini Terlalu Besar, Mengunggah Daftar Akun Terhapus Sebagai File."
        )
        file = open("daftarpengguna.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "daftarpengguna.txt",
            caption="Daftar Pengguna {}".format(title),
            reply_to=show.id,
        )
        remove("daftarpengguna.txt")


async def get_userdel_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Ketik username Atau Balas Ke Pesan Pengguna!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.bots$", groups_only=True)
async def get_bots(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Grup Ini"
    mentions = f"<b>Daftar Bot Di {title}:</b>\n"
    try:
        if isinstance(show.to_id, PeerChat):
            return await show.edit(
                "`Saya mendengar bahwa hanya Supergrup yang dapat memiliki bot`"
            )
        else:
            async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots
            ):
                if not user.deleted:
                    link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n ⚜️ {link} {userid}"
                else:
                    mentions += f"\nBot Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Terlalu Banyak Bot Di Grup Ini, Mengunggah Daftar Bot Sebagai File."
        )
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption="Daftar Bot Di {}".format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")


CMD_HELP.update(
    {
        "admin": "**Plugin : **`admin`\
        \n\n  •  **Syntax :** `.promote <username/reply> <nama title (optional)>`\
        \n  •  **Function : **Mempromosikan member sebagai admin.\
        \n\n  •  **Syntax :** `.demote <username/balas ke pesan>`\
        \n  •  **Function : **Menurunkan admin sebagai member.\
        \n\n  •  **Syntax :** `.ban <username/balas ke pesan> <alasan (optional)>`\
        \n  •  **Function : **Membanned Pengguna dari grup.\
        \n\n  •  **Syntax :** `.unban <username/reply>`\
        \n  •  **Function : **Unbanned pengguna jadi bisa join grup lagi.\
        \n\n  •  **Syntax :** `.dmute <username/reply> <alasan (optional)>`\
        \n  •  **Function : **Membisukan Seseorang Di Grup dengan menghapus pesannya, Bisa Ke Admin Juga.\
        \n\n  •  **Syntax :** `.undmute <username/reply>`\
        \n  •  **Function : **Membuka bisu orang yang dibisukan.\
        \n\n  •  **Syntax :** `.gmute <username/reply> <alasan (optional)>`\
        \n  •  **Function : **Membisukan Pengguna ke semua grup yang kamu punya sebagai admin.\
        \n\n  •  **Syntax :** `.ungmute <username/reply>`\
        \n  •  **Function : ** Membuka global mute orang yang dibisukan.\
        \n\n  •  **Syntax :** `.setgpic <balas ke gambar>`\
        \n  •  **Function : **Mengganti foto profil grup.\
        \n\n  •  **Syntax :** `.all`\
        \n  •  **Function : **Tag semua member dalam grup.\
        \n\n  •  **Syntax :** `.admins`\
        \n  •  **Function : **Melihat daftar admin di grup.\
        \n\n  •  **Syntax :** `.bots`\
        \n  •  **Function : **Melihat daftar bot dalam grup.\
        \n\n  •  **Syntax :** `.users` Atau `.users <nama member>`\
        \n  •  **Function : **Mendapatkan daftar pengguna daam grup.\
    "
    }
)


CMD_HELP.update(
    {
        "zombies": "**Plugin : **`zombies`\
        \n\n  •  **Syntax :** `.zombies`\
        \n  •  **Function : **Untuk mencari akun terhapus dalam grup\
        \n\n  •  **Syntax :** `.zombies clean`\
        \n  •  **Function : **untuk menghapus Akun Terhapus dari grup.\
    "
    }
)
