from time import sleep

from userbot import BLACKLIST_CHAT
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"sayang(?: |$)(.*)"))
async def _(event):
    await event.edit("**Cuma Mau Bilang**")
    sleep(3)
    await event.edit("**Aku Sayang Kamu**")
    sleep(1)
    await event.edit("**I LOVE YOU 💞**")


# Create by myself @localheart


@bot.on(man_cmd(outgoing=True, pattern=r"semangat(?: |$)(.*)"))
async def _(event):
    await event.edit("**Apapun Yang Terjadi**")
    sleep(3)
    await event.edit("**Tetaplah Bernapas**")
    sleep(1)
    await event.edit("**Dan Selalu Bersyukur**")


# Create by myself @localheart


@bot.on(man_cmd(outgoing=True, pattern=r"ywc(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(event.chat_id, "**Ok Sama Sama**")
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"jamet(?: |$)(.*)"))
async def _(event):
    await event.edit("**WOII**")
    sleep(1.5)
    await event.edit("**JAMET**")
    sleep(1.5)
    await event.edit("**CUMA MAU BILANG**")
    sleep(1.5)
    await event.edit("**GAUSAH SO ASIK**")
    sleep(1.5)
    await event.edit("**EMANG KENAL?**")
    sleep(1.5)
    await event.edit("**GAUSAH REPLY**")
    sleep(1.5)
    await event.edit("**KITA BUKAN KAWAN**")
    sleep(1.5)
    await event.edit("**GASUKA PC ANJING**")
    sleep(1.5)
    await event.edit("**BOCAH KAMPUNG**")
    sleep(1.5)
    await event.edit("**MENTAL TEMPE**")
    sleep(1.5)
    await event.edit("**LEMBEK NGENTOT🔥**")


@bot.on(man_cmd(outgoing=True, pattern=r"pp(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**PASANG PP DULU GOBLOK,BIAR ORANG-ORANG PADA TAU BETAPA HINA NYA MUKA LU 😆**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"dp(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id, "**MUKA LU HINA, GAUSAH SOK KERAS YA ANJENGG!!**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"so(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id, "**GAUSAH SOKAB SAMA GUA GOBLOK, LU BABU GA LEVEL!!**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"nb(?: |$)(.*)"))
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit("**Perintah ini Dilarang digunakan di Group ini**")
    await event.client.send_message(
        event.chat_id, "**MAEN BOT MULU ALAY NGENTOTT, KESANNYA NORAK GOBLOK!!!**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"met(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id, "**NAMANYA JUGA JAMET CAPER SANA SINI BUAT CARI NAMA**"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"war(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**WAR WAR PALAK BAPAK KAU WAR, SOK KERAS BANGET GOBLOK, DI TONGKRONGAN JADI BABU, DI TELE SOK JAGOAN...**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"wartai(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**WAR WAR TAI ANJING, KETRIGGER MINTA SHARELOK LU KIRA MAU COD-AN GOBLOK, BACOTAN LU AJA KGA ADA KERAS KERASNYA GOBLOK**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"kismin(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**CUIHHHH, MAKAN AJA MASIH NGEMIS LO GOBLOK, JANGAN SO NINGGI YA KONTOL GA KEREN LU KEK GITU GOBLOK!!**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"ded(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id, "**MATI AJA LU GOBLOK, GAGUNA LU HIDUP DI BUMI**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"sokab(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**SOKAB BET LU GOBLOK, KAGA ADA ISTILAH NYA BAWAHAN TEMENAN AMA BOS!!**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"gembel(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**MUKA BAPAK LU KEK KELAPA SAWIT ANJING, GA USAH NGATAIN ORANG, MUKA LU AJA KEK GEMBEL TEXAS GOBLOK!!**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"cuih(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**GAK KEREN LO KEK BEGITU GOBLOK, KELUARGA LU BAWA SINI GUA LUDAHIN SATU-SATU. CUIHH!!!**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"dih(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**DIHHH NAJISS ANAK HARAM LO GOBLOK, JANGAN BELAGU DIMARI KAGA KEREN LU KEK BGITU TOLOL!**",
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"gcs(?: |$)(.*)"))
async def _(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit("**Perintah ini Dilarang digunakan di Group ini**")
    await event.client.send_message(
        event.chat_id, "**GC SAMPAH KAYA GINI, BUBARIN AJA GOBLOK!!**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"skb(?: |$)(.*)"))
async def _(event):
    await event.client.send_message(
        event.chat_id, "**EMANG KITA KENAL? KAGA GOBLOK SOKAB BANGET LU GOBLOK**"
    )
    await event.delete()


@bot.on(man_cmd(outgoing=True, pattern=r"virtual(?: |$)(.*)"))
async def _(event):
    await event.edit("**OOOO**")
    sleep(1.5)
    await event.edit("**INI YANG VIRTUAL**")
    sleep(1.5)
    await event.edit("**YANG KATANYA SAYANG BANGET**")
    sleep(1.5)
    await event.edit("**TAPI TETEP AJA DI TINGGAL**")
    sleep(1.5)
    await event.edit("**NI INGET**")
    sleep(1.5)
    await event.edit("**TANGANNYA AJA GA BISA DI PEGANG**")
    sleep(1.5)
    await event.edit("**APALAGI OMONGANNYA**")
    sleep(1.5)
    await event.edit("**BHAHAHAHA**")
    sleep(1.5)
    await event.edit("**KASIAN MANA MASIH MUDA**")


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
        \n\n**Klo mau Req, kosa kata dari lu Bisa pake Module costum. Ketik** `{cmd}help costum`\
    "
    }
)
