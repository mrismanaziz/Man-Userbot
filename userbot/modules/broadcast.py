# Credit by https://github.com/sandy1709/catuserbot
# Ported by @X_ImFine
# Recode by @mrismanaziz
# @SharingUserbot

from asyncio import sleep

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LOGS
from userbot.modules.sql_helper import broadcast_sql as sql
from userbot.utils import man_cmd, parse_pre


@man_cmd(pattern=r"sendto ?(.*)")
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "**Ke kategori mana saya harus mengirim pesan ini?**", parse_mode=parse_pre
        )
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit(
            "**apa yang harus saya kirim ke kategori ini?**", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await event.edit(
            f"**Tidak ada kategori dengan nama** `{keyword}` **Check** `.bclistall`",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(
        "**mengirim pesan ini ke semua grup dalam kategori**",
        parse_mode=parse_pre,
    )
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.send_message(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"**Pesan dikirim ke** `{i}` **obrolan keluar** `{no_of_chats}` **obrolan dalam kategori** `{keyword}`"
    await catevent.edit(resultext)
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**Sebuah pesan dikirim ke** `{i}` **obrolan keluar** `{no_of_chats}` **obrolan dalam kategori** `{keyword}`",
            parse_mode=parse_pre,
        )


@man_cmd(pattern=r"fwdto ?(.*)")
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "**Ke kategori mana saya harus mengirim pesan ini?**", parse_mode=parse_pre
        )
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit(
            "**apa yang harus saya kirim ke kategori ini?**", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await event.edit(
            f"**Tidak ada kategori dengan nama** `{keyword}` **Check** '.bclistall'",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(
        "**mengirim pesan ini ke semua grup dalam kategori**",
        parse_mode=parse_pre,
    )
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.forward_messages(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"**Pesan dikirim ke** {i} **obrolan keluar** {no_of_chats} **obrolan dalam kategori** `{keyword}`"
    await catevent.edit(resultext)
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**Sebuah pesan diteruskan ke** `{i}` **obrolan keluar** `{no_of_chats}` **obrolan dalam kategori** `{keyword}`",
            parse_mode=parse_pre,
        )


@man_cmd(pattern=r"addto ?(.*)")
async def catbroadcast_add(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "Di kategori mana saya harus menambahkan obrolan ini?", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if check:
        return await event.edit(
            f"Obrolan ini sudah ada dalam kategori ini {keyword}",
            parse_mode=parse_pre,
        )
    sql.add_to_broadcastlist(keyword, event.chat_id)
    await event.edit(
        f"Obrolan ini Sekarang ditambahkan ke kategori {keyword}", parse_mode=parse_pre
    )
    chat = await event.get_chat()
    if BOTLOG_CHATID:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Obrolan {chat.title} ditambahkan ke kategori {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Pengguna {chat.first_name} ditambahkan ke kategori {keyword}",
                parse_mode=parse_pre,
            )


@man_cmd(pattern=r"rmfrom ?(.*)")
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "Dari kategori mana saya harus menghapus obrolan ini", parse_mode=parse_pre
        )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await event.edit(
            f"Obrolan ini tidak ada dalam kategori {keyword}", parse_mode=parse_pre
        )
    sql.rm_from_broadcastlist(keyword, event.chat_id)
    await event.edit(
        f"Obrolan ini Sekarang dihapus dari kategori {keyword}",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG_CHATID:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Obrolan {chat.title} dihapus dari kategori {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"pengguna {chat.first_name} dihapus dari kategori {keyword}",
                parse_mode=parse_pre,
            )


@man_cmd(pattern=r"bclist ?(.*)")
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "Obrolan kategori mana yang harus saya daftarkan?\nCheck `.bclistall`",
            parse_mode=parse_pre,
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await event.edit(
            f"Tidak ada kategori dengan nama {keyword}. Check `.bclistall`",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(
        f"Fetching info of the category {keyword}", parse_mode=parse_pre
    )
    resultlist = f"**kategori `{keyword}` memiliki `{no_of_chats}` obrolan dan ini tercantum di bawah ini :**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **Channel** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **Group** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **User** \n  •  **Name : **{chatinfo.first_name} \n  •  **id : **`{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 __ID ini {int(chat)} dalam basis data mungkin Anda meninggalkan obrolan/saluran atau mungkin id tidak valid.\
                            \nHapus id ini dari database dengan menggunakan perintah ini__ `.frmfrom {keyword} {int(chat)}` \n\n"
    finaloutput = resultlist + errorlist
    await catevent.edit(finaloutput)


@man_cmd(pattern=r"bclistall ?(.*)")
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    if sql.num_broadcastlist_chats() == 0:
        return await event.edit(
            "Anda belum membuat setidaknya satu kategori, periksa info untuk bantuan lebih lanjut",
            parse_mode=parse_pre,
        )
    chats = sql.get_broadcastlist_chats()
    resultext = "**Berikut adalah daftar kategori Anda :**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __contains {sql.num_broadcastlist_chat(i)} chats__\n"
    await event.efit(resultext)


@man_cmd(pattern=r"frmfrom ?(.*)")
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "Dari kategori mana saya harus menghapus obrolan ini", parse_mode=parse_pre
        )
    args = catinput_str.split(" ")
    if len(args) != 2:
        return await event.edit(
            "Gunakan sintaks yang tepat seperti yang ditunjukkan .frmfrom category_name groupid",
            parse_mode=parse_pre,
        )
    try:
        groupid = int(args[0])
        keyword = args[1].lower()
    except ValueError:
        try:
            groupid = int(args[1])
            keyword = args[0].lower()
        except ValueError:
            return await event.edit(
                event,
                "Gunakan sintaks yang tepat seperti yang ditunjukkan .frmfrom category_name groupid",
                parse_mode=parse_pre,
            )
    keyword = keyword.lower()
    check = sql.is_in_broadcastlist(keyword, int(groupid))
    if not check:
        return await event.edit(
            f"Obrolan ini {groupid} tidak termasuk dalam kategori {keyword}",
            parse_mode=parse_pre,
        )
    sql.rm_from_broadcastlist(keyword, groupid)
    await event.edit(
        event,
        f"Obrolan ini {groupid} sekarang dihapus dari kategori {keyword}",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG_CHATID:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Obrolan ini {chat.title} dihapus dari kategori {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"pengguna {chat.first_name} dihapus dari kategori {keyword}",
                parse_mode=parse_pre,
            )


@man_cmd(pattern=r"delc ?(.*)")
async def catbroadcast_delete(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    check1 = sql.num_broadcastlist_chat(catinput_str)
    if check1 < 1:
        return await event.edit(
            f"Apakah Anda yakin ada kategori? {catinput_str}",
            parse_mode=parse_pre,
        )
    try:
        sql.del_keyword_broadcastlist(catinput_str)
        await event.edit(
            f"Berhasil menghapus kategori {catinput_str}",
            parse_mode=parse_pre,
        )
    except Exception as e:
        await event.edit(
            str(e),
            parse_mode=parse_pre,
        )


CMD_HELP.update(
    {
        "broadcast": f"**Plugin : **`broadcast`\
        \n\n  •  **Syntax :** `{cmd}sendto` <category_name>\
        \n  •  **Function : **akan mengirim pesan balasan ke semua obrolan dalam kategori yang diberikan.\
        \n\n  •  **Syntax :** `{cmd}fwdto` <category_name>\
        \n  •  **Function : **akan meneruskan pesan yang dibalas ke semua obrolan di kategori berikan. \
        \n\n  •  **Syntax :** `{cmd}addto` <category name>\
        \n  •  **Function : **Ini akan menambahkan obrolan / pengguna / saluran ini ke kategori nama yang diberikan. \
        \n\n  •  **Syntax :** `{cmd}rmfrom` <category name>\
        \n  •  **Function : **Untuk menghapus Obrolan / pengguna / saluran dari nama kategori yang diberikan. \
        \n\n  •  **Syntax :** `{cmd}bclist` <category_name>\
        \n  •  **Function : **Akan menampilkan daftar semua obrolan dalam kategori yang diberikan. \
        \n\n  •  **Syntax :** `{cmd}bclistall`\
        \n  •  **Function : **Akan menampilkan daftar semua nama kategori. \
        \n\n  •  **Syntax :** `{cmd}frmfrom` <category_name/chat_id>\
        \n  •  **Function : **Untuk memaksa menghapus chat_id yang diberikan dari nama kategori yang diberikan berguna ketika Anda meninggalkan obrolan itu atau melarang Anda di sana \
        \n\n  •  **Syntax :** `{cmd}delc` <category_name>\
        \n  •  **Function : **Menghapus kategori sepenuhnya di database \
    "
    }
)
