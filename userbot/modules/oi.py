from time import sleep

from userbot import BLACKLIST_CHAT
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="sayang(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**Cuma Mau Bilang**")
    sleep(3)
    await xx.edit("**Aku Sayang Kamu**")
    sleep(1)
    await xx.edit("**I LOVE YOU 💞**")


# Create by myself @localheart


@man_cmd(pattern="semangat(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**Apapun Yang Terjadi**")
    sleep(3)
    await xx.edit("**Tetaplah Bernapas**")
    sleep(1)
    await xx.edit("**Dan Selalu Bersyukur**")


# Create by myself @localheart


@man_cmd(pattern=r"ywc(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id, "**Ok Sama Sama**", reply_to=event.reply_to_msg_id
    )
    await event.delete()


@man_cmd(pattern="jamet(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**WOII**")
    sleep(1.5)
    await xx.edit("**JAMET**")
    sleep(1.5)
    await xx.edit("**CUMA MAU BILANG**")
    sleep(1.5)
    await xx.edit("**GAUSAH SO ASIK**")
    sleep(1.5)
    await xx.edit("**EMANG KENAL?**")
    sleep(1.5)
    await xx.edit("**GAUSAH REPLY**")
    sleep(1.5)
    await xx.edit("**KITA BUKAN KAWAN**")
    sleep(1.5)
    await xx.edit("**GASUKA PC ANJING**")
    sleep(1.5)
    await xx.edit("**BOCAH KAMPUNG**")
    sleep(1.5)
    await xx.edit("**MENTAL TEMPE**")
    sleep(1.5)
    await xx.edit("**LEMBEK NGENTOT🔥**")


@man_cmd(pattern="pp(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**PASANG PP DULU GOBLOK,BIAR ORANG-ORANG PADA TAU BETAPA HINA NYA MUKA LU 😆**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="dp(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**MUKA LU HINA, GAUSAH SOK KERAS YA ANJENGG!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="so(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**GAUSAH SOKAB SAMA GUA GOBLOK, LU BABU GA LEVEL!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="nb(?: |$)(.*)")
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    await event.client.send_message(
        event.chat_id,
        "**MAEN BOT MULU ALAY NGENTOTT, KESANNYA NORAK GOBLOK!!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="met(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**NAMANYA JUGA JAMET CAPER SANA SINI BUAT CARI NAMA**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="war(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**WAR WAR PALAK BAPAK KAU WAR, SOK KERAS BANGET GOBLOK, DI TONGKRONGAN JADI BABU, DI TELE SOK JAGOAN...**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="wartai(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**WAR WAR TAI ANJING, KETRIGGER MINTA SHARELOK LU KIRA MAU COD-AN GOBLOK, BACOTAN LU AJA KGA ADA KERAS KERASNYA GOBLOK**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="kismin(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**CUIHHHH, MAKAN AJA MASIH NGEMIS LO GOBLOK, JANGAN SO NINGGI YA KONTOL GA KEREN LU KEK GITU GOBLOK!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="ded(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**MATI AJA LU GOBLOK, GAGUNA LU HIDUP DI BUMI**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="sokab(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**SOKAB BET LU GOBLOK, KAGA ADA ISTILAH NYA BAWAHAN TEMENAN AMA BOS!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="gembel(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**MUKA BAPAK LU KEK KELAPA SAWIT ANJING, GA USAH NGATAIN ORANG, MUKA LU AJA KEK GEMBEL TEXAS GOBLOK!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="cuih(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**GAK KEREN LO KEK BEGITU GOBLOK, KELUARGA LU BAWA SINI GUA LUDAHIN SATU-SATU. CUIHH!!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="dih(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**DIHHH NAJISS ANAK HARAM LO GOBLOK, JANGAN BELAGU DIMARI KAGA KEREN LU KEK BGITU TOLOL!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern=r"gcs(?: |$)(.*)")
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    await event.client.send_message(
        event.chat_id,
        "**GC SAMPAH KAYA GINI, BUBARIN AJA GOBLOK!!**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="skb(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**EMANG KITA KENAL? KAGA GOBLOK SOKAB BANGET LU GOBLOK**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@man_cmd(pattern="virtual(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**OOOO**")
    sleep(1.5)
    await xx.edit("**INI YANG VIRTUAL**")
    sleep(1.5)
    await xx.edit("**YANG KATANYA SAYANG BANGET**")
    sleep(1.5)
    await xx.edit("**TAPI TETEP AJA DI TINGGAL**")
    sleep(1.5)
    await xx.edit("**NI INGET**")
    sleep(1.5)
    await xx.edit("**TANGANNYA AJA GA BISA DI PEGANG**")
    sleep(1.5)
    await xx.edit("**APALAGI OMONGANNYA**")
    sleep(1.5)
    await xx.edit("**BHAHAHAHA**")
    sleep(1.5)
    await xx.edit("**KASIAN MANA MASIH MUDA**")


CMD_HELP.update(
    {
        "war": f"**Plugin : **`war`\
        \n\n  •  **Syntax :** `{cmd}jamet`\
        \n  •  **Function : **Menghina Jamet telegram\
        \n\n  •  **Syntax :** `{cmd}pp`\
        \n  •  **Function : **Menghina Jamet telegram yang ga pake foto profil\
        \n\n  •  **Syntax :** `{cmd}dp`\
        \n  •  **Function : **Menghina Jamet muka hina!\
        \n\n  •  **Syntax :** `{cmd}so`\
        \n  •  **Function : **Ngeledek orang sokab\
        \n\n  •  **Syntax :** `{cmd}nb`\
        \n  •  **Function : **Ngeledek orang norak baru pake bot\
        \n\n  •  **Syntax :** `{cmd}so`\
        \n  •  **Function : **Ngeledek orang sokab\
        \n\n  •  **Syntax :** `{cmd}skb`\
        \n  •  **Function : **Ngeledek orang sokab versi 2\
        \n\n  •  **Syntax :** `{cmd}met`\
        \n  •  **Function : **Ngeledek si jamet caper\
        \n\n  •  **Syntax :** `{cmd}war`\
        \n  •  **Function : **Ngeledek orang so keras ngajak war\
        \n\n  •  **Syntax :** `{cmd}wartai`\
        \n  •  **Function : **Ngeledek orang so ketrigger ngajak cod minta sharelok\
        \n\n  •  **Syntax :** `{cmd}kismin`\
        \n  •  **Function : **Ngeledek orang kismin so jagoan di tele\
        \n\n  •  **Syntax :** `{cmd}ded`\
        \n  •  **Function : **Nyuruh orang mati aja goblok wkwk\
        \n\n  •  **Syntax :** `{cmd}sokab`\
        \n  •  **Function : **Ngeledek orang so kenal so dekat padahal kga kenal goblok\
        \n\n  •  **Syntax :** `{cmd}gembel`\
        \n  •  **Function : **Ngeledek bapaknya si jamet\
        \n\n  •  **Syntax :** `{cmd}cuih`\
        \n  •  **Function : **Ngeludahin keluarganya satu satu wkwk\
        \n\n  •  **Syntax :** `{cmd}dih`\
        \n  •  **Function : **Ngeledek anak haram\
        \n\n  •  **Syntax :** `{cmd}gcs`\
        \n  •  **Function : **Ngeledek gc sampah\
        \n\n  •  **Syntax :** `{cmd}virtual`\
        \n  •  **Function : **Ngeledek orang pacaran virtual\
        \n\n**Klo mau Req, kosa kata dari lu Bisa pake Module costum. Ketik** `{cmd}help custom`\
    "
    }
)
