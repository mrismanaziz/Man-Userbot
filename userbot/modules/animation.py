import asyncio
from time import sleep

from telethon import events

from userbot import CMD_HELP, bot
from userbot.events import register


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 1

    animation_ttl = range(117)

    input_str = event.pattern_match.group(1)

    if input_str == "avengers":

        await event.edit(input_str)

        animation_chars = [
            "Assalamualaikum, kami adalah avengers",
            "Mari berkenalan yaitu :",
            "Aladdin si om ganteng",
            "Achong si cina sesat",
            "Andre si maska botak",
            "Malika kedelai hitam pilihan",
            "Arjen si kang TMO",
            "Adi si kuli 24jam",
            "Dyka si mata mata",
            "Cece si ratu desah",
            "Steven si ilang ilangan",
            "Reno si caper",
            "Jamrud si brondong sangean",
            "Boy si gondrong ga nyopet",
            "Jo si gembul",
            "Cobor si misterius",
            "Jamal si bocah terbully",
            "Yuhu si bocah lemot",
            "Kimy si cewe caper",
            "Dodo si tukang berak",
            "Anna si TT gede",
            "Cala si mami hot",
            "Coki siapasih",
            "Eja si akang jedag jedug",
            "Saldi si bocah ilang",
            "Gery si cowo cool",
            "Tuni si patkay",
            "Brilian si lelek jawa",
            "Zeen si kembaran dyka",
            "Billa si cewe jutek",
            "Lucifer si cowo beatbox",
            "Sekian dari kami, makasih",

        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 32])


@register(outgoing=True, pattern=r"^\.sayang$")
async def koc(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("I LOVEE YOUUU 💕")
        await e.edit("💝💘💓💗")
        await e.edit("💞💕💗💘")
        await e.edit("💝💘💓💗")
        await e.edit("💞💕💗💘")
        await e.edit("💘💞💗💕")
        await e.edit("💘💞💕💗")
        await e.edit("SAYANG KAMU 💝💖💘")
        await e.edit("💝💘💓💗")
        await e.edit("💞💕💗💘")
        await e.edit("💘💞💕💗")
        await e.edit("SAYANG")
        await e.edit("KAMU")
        await e.edit("SELAMANYA 💕")
        await e.edit("💘💘💘💘")
        await e.edit("SAYANG")
        await e.edit("KAMU")
        await e.edit("SAYANG")
        await e.edit("KAMU")
        await e.edit("I LOVE YOUUUU")
        await e.edit("MY BABY")
        await e.edit("💕💞💘💝")
        await e.edit("💘💕💞💝")
        await e.edit("SAYANG KAMU💞")


@register(outgoing=True, pattern=r"^\.sultan(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`SUL SULLLL.....`")
    sleep(1)
    await typew.edit("`SUULLLLLLTTTAAAANN!!`")
    sleep(1)
    await typew.edit("`🏃                        👩‍🦽`")
    await typew.edit("`🏃                       👩‍🦽`")
    await typew.edit("`🏃                      👩‍🦽`")
    await typew.edit("`🏃                     👩‍🦽`")
    await typew.edit("`🏃   `KEJAR`          👩‍🦽`")
    await typew.edit("`🏃                   👩‍🦽`")
    await typew.edit("`🏃                  👩‍🦽`")
    await typew.edit("`🏃                 👩‍🦽`")
    await typew.edit("`🏃                👩‍🦽`")
    await typew.edit("`🏃               👩‍🦽`")
    await typew.edit("`🏃              👩‍🦽`")
    await typew.edit("`🏃             👩‍🦽`")
    await typew.edit("`🏃            👩‍🦽`")
    await typew.edit("`🏃           👩‍🦽`")
    await typew.edit("`🏃WOARGH!   👩‍🦽`")
    await typew.edit("`🏃           👩‍🦽`")
    await typew.edit("`🏃            👩‍🦽`")
    await typew.edit("`🏃             👩‍🦽`")
    await typew.edit("`🏃              👩‍🦽`")
    await typew.edit("`🏃               👩‍🦽`")
    await typew.edit("`🏃                👩‍🦽`")
    await typew.edit("`🏃                 👩‍🦽`")
    await typew.edit("`🏃                  👩‍🦽`")
    await typew.edit("`🏃                   👩‍🦽`")
    await typew.edit("`🏃                    👩‍🦽`")
    await typew.edit("`🏃                     👩‍🦽`")
    await typew.edit("`🏃Kencang juga sultan 👩‍🦽`")
    await typew.edit("`🏃                   👩‍🦽`")
    await typew.edit("`🏃                  👩‍🦽`")
    await typew.edit("`🏃                 👩‍🦽`")
    await typew.edit("`🏃                👩‍🦽`")
    await typew.edit("`🏃               👩‍🦽`")
    await typew.edit("`🏃              👩‍🦽`")
    await typew.edit("`🏃             👩‍🦽`")
    await typew.edit("`🏃            👩‍🦽`")
    await typew.edit("`🏃           👩‍🦽`")
    await typew.edit("`🏃          👩‍🦽`")
    await typew.edit("`🏃         👩‍🦽`")
    await typew.edit("`AYOLAH DIKIT LAGI TERKEJAR!!!`")
    sleep(1)
    await typew.edit("`🏃       👩‍🦽`")
    await typew.edit("`🏃      👩‍🦽`")
    await typew.edit("`🏃     👩‍🦽`")
    await typew.edit("`🏃    👩‍🦽`")
    await typew.edit("`Dahlah SULTAN pasrah Aja`")
    sleep(1)
    await typew.edit("`🧎👩‍🦽`")
    sleep(2)
    await typew.edit("`-TAMAT-`")


@register(outgoing=True, pattern=r"^\.gabut$")
async def koc(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`KAMIII ADALAHHH AVANGERS FAMILY`")
        await e.edit("`SEPEEERTIIIII INILAH FAMILY KAMIIIII`")
        await e.edit("`BERBAGAI BENTUK WATAK ORANGNYA`")
        await e.edit("`ADA YANG LUCU `")
        await e.edit("`ADA PULA MACAM BABIIII`")
        await e.edit("`WALAAUUUU BEGITU KAMI SELALU KOMPAK`")
        await e.edit("`KALAU GABUUTTTT`")
        await e.edit("`PALING NGERUSUH`")
        await e.edit("`ITULAH KAMI PARA AVENGERS`")
        await e.edit("🙈🙈🙈🙈")
        await e.edit("🙉🙉🙉🙉")
        await e.edit("🙈🙈🙈🙈")
        await e.edit("🙉🙉🙉🙉")
        await e.edit("`CILUUUKKK BAAAAA`")
        await e.edit("🙉🙉🙉🙉")
        await e.edit("🦸                       🚶")
        await e.edit("🦸                      🚶")
        await e.edit("🦸                     🚶")
        await e.edit("🦸                    🚶")
        await e.edit("🦸                   🚶")
        await e.edit("🦸                  🚶")
        await e.edit("🦸                 🚶")
        await e.edit("🦸                🚶")
        await e.edit("🦸               🚶")
        await e.edit("🦸              🚶")
        await e.edit("🦸             🚶")
        await e.edit("🦸            🚶")
        await e.edit("🦸           🚶")
        await e.edit("🦸          🚶")
        await e.edit("🦸         🚶")
        await e.edit("🦸        🚶")
        await e.edit("🦸       🚶")
        await e.edit("🦸      🚶")
        await e.edit("🦸     🚶")
        await e.edit("🦸    🚶")
        await e.edit("🦸   🚶")
        await e.edit("🦸  🚶")
        await e.edit("🦸 🚶")
        await e.edit("🦸🚶")
        await e.edit("🚶🦸")
        await e.edit("🚶 🦸")
        await e.edit("🚶  🦸")
        await e.edit("🚶   🦸")
        await e.edit("🚶    🦸")
        await e.edit("🚶     🦸")
        await e.edit("🚶      🦸")
        await e.edit("🚶       🦸")
        await e.edit("🚶        🦸")
        await e.edit("🚶         🦸")
        await e.edit("🚶          🦸")
        await e.edit("🚶           🦸")
        await e.edit("🚶            🦸")
        await e.edit("🚶             🦸")
        await e.edit("🚶              🦸")
        await e.edit("🚶               🦸")
        await e.edit("🚶                🦸")
        await e.edit("🚶                 🦸")
        await e.edit("🚶                  🦸")
        await e.edit("🚶                   🦸")
        await e.edit("🚶                    🦸")
        await e.edit("🚶                     🦸")
        await e.edit("🚶                      🦸")
        await e.edit("🚶                       🦸")
        await e.edit("🚶                        🦸")
        await e.edit("🚶                         🦸")
        await e.edit("🚶                          🦸")
        await e.edit("🚶                           🦸")
        await e.edit("🚶                            🦸")
        await e.edit("🚶                             🦸")
        await e.edit("🚶                              🦸")
        await e.edit("🚶                               🦸")
        await e.edit("🚶                                🦸")
        await e.edit("🚶                                 🦸")
        await e.edit("`BERUBAAHHHHH`")
        await e.edit("😛")
        await e.edit("😝")
        await e.edit("😜")
        await e.edit("🤪")
        await e.edit("😋")
        await e.edit("😂")
        await e.edit("🦸                       🚶")
        await e.edit("🦸                      🚶")
        await e.edit("🦸                     🚶")
        await e.edit("🦸                    🚶")
        await e.edit("🦸                   🚶")
        await e.edit("🦸                  🚶")
        await e.edit("🦸                 🚶")
        await e.edit("🦸                🚶")
        await e.edit("🦸               🚶")
        await e.edit("🦸              🚶")
        await e.edit("🦸             🚶")
        await e.edit("🦸            🚶")
        await e.edit("🦸           🚶")
        await e.edit("🦸          🚶")
        await e.edit("🦸         🚶")
        await e.edit("🦸        🚶")
        await e.edit("🦸       🚶")
        await e.edit("🦸      🚶")
        await e.edit("🦸     🚶")
        await e.edit("🦸    🚶")
        await e.edit("🦸   🚶")
        await e.edit("🦸  🚶")
        await e.edit("🦸 🚶")
        await e.edit("🦸🚶")
        await e.edit("🚶🦸")
        await e.edit("🚶 🦸")
        await e.edit("🚶  🦸")
        await e.edit("🚶   🦸")
        await e.edit("🚶    🦸")
        await e.edit("🚶     🦸")
        await e.edit("🚶      🦸")
        await e.edit("🚶       🦸")
        await e.edit("🚶        🦸")
        await e.edit("🚶         🦸")
        await e.edit("🚶          🦸")
        await e.edit("🚶           🦸")
        await e.edit("🚶            🦸")
        await e.edit("🚶             🦸")
        await e.edit("🚶              🦸")
        await e.edit("🚶               🦸")
        await e.edit("🚶                🦸")
        await e.edit("🚶                 🦸")
        await e.edit("🚶                  🦸")
        await e.edit("🚶                   🦸")
        await e.edit("🚶                    🦸")
        await e.edit("🚶                     🦸")
        await e.edit("🚶                      🦸")
        await e.edit("🚶                       🦸")
        await e.edit("🚶                        🦸")
        await e.edit("🚶                         🦸")
        await e.edit("🚶                          🦸")
        await e.edit("🚶                           🦸")
        await e.edit("🚶                            🦸")
        await e.edit("🚶                             🦸")
        await e.edit("🚶                              🦸")
        await e.edit("🚶                               🦸")
        await e.edit("🚶                                🦸")
        await e.edit("🦸                       🚶")
        await e.edit("🦸                      🚶")
        await e.edit("🦸                     🚶")
        await e.edit("🦸                    🚶")
        await e.edit("🦸                   🚶")
        await e.edit("🦸                  🚶")
        await e.edit("🦸                 🚶")
        await e.edit("🦸                🚶")
        await e.edit("🦸               🚶")
        await e.edit("🦸              🚶")
        await e.edit("🦸             🚶")
        await e.edit("🦸            🚶")
        await e.edit("🦸           🚶")
        await e.edit("🦸          🚶")
        await e.edit("🦸         🚶")
        await e.edit("🦸        🚶")
        await e.edit("🦸       🚶")
        await e.edit("🦸      🚶")
        await e.edit("🦸     🚶")
        await e.edit("🦸    🚶")
        await e.edit("🦸   🚶")
        await e.edit("🦸  🚶")
        await e.edit("🦸 🚶")
        await e.edit("🦸🚶")
        await e.edit("🚶🦸")
        await e.edit("🚶 🦸")
        await e.edit("🚶  🦸")
        await e.edit("🚶   🦸")
        await e.edit("🚶    🦸")
        await e.edit("🚶     🦸")
        await e.edit("🚶      🦸")
        await e.edit("🚶       🦸")
        await e.edit("🚶        🦸")
        await e.edit("🚶         🦸")
        await e.edit("🚶          🦸")
        await e.edit("🚶           🦸")
        await e.edit("🚶            🦸")
        await e.edit("🚶             🦸")
        await e.edit("🚶              🦸")
        await e.edit("🚶               🦸")
        await e.edit("🚶                🦸")
        await e.edit("🚶                 🦸")
        await e.edit("🚶                  🦸")
        await e.edit("🚶                   🦸")
        await e.edit("🚶                    🦸")
        await e.edit("🚶                     🦸")
        await e.edit("🚶                      🦸")
        await e.edit("🚶                       🦸")
        await e.edit("🚶                        🦸")
        await e.edit("🚶                         🦸")
        await e.edit("🚶                          🦸")
        await e.edit("🚶                           🦸")
        await e.edit("🚶                            🦸")
        await e.edit("🚶                             🦸")
        await e.edit("🚶                              🦸")
        await e.edit("🚶                               🦸")
        await e.edit("🚶                                🦸")
        await e.edit("🦸                       🚶")
        await e.edit("🦸                      🚶")
        await e.edit("🦸                     🚶")
        await e.edit("🦸                    🚶")
        await e.edit("🦸                   🚶")
        await e.edit("🦸                  🚶")
        await e.edit("🦸                 🚶")
        await e.edit("🦸                🚶")
        await e.edit("🦸               🚶")
        await e.edit("🦸              🚶")
        await e.edit("🦸             🚶")
        await e.edit("🦸            🚶")
        await e.edit("🦸           🚶")
        await e.edit("🦸          🚶")
        await e.edit("🦸         🚶")
        await e.edit("🦸        🚶")
        await e.edit("🦸       🚶")
        await e.edit("🦸      🚶")
        await e.edit("🦸     🚶")
        await e.edit("🦸    🚶")
        await e.edit("🦸   🚶")
        await e.edit("🦸  🚶")
        await e.edit("🦸 🚶")
        await e.edit("🦸🚶")
        await e.edit("🚶🦸")
        await e.edit("🚶 🦸")
        await e.edit("🚶  🦸")
        await e.edit("🚶   🦸")
        await e.edit("🚶    🦸")
        await e.edit("🚶     🦸")
        await e.edit("🚶      🦸")
        await e.edit("🚶       🦸")
        await e.edit("🚶        🦸")
        await e.edit("🚶         🦸")
        await e.edit("🚶          🦸")
        await e.edit("🚶           🦸")
        await e.edit("🚶            🦸")
        await e.edit("🚶             🦸")
        await e.edit("🚶              🦸")
        await e.edit("🚶               🦸")
        await e.edit("🚶                🦸")
        await e.edit("🚶                 🦸")
        await e.edit("🚶                  🦸")
        await e.edit("🚶                   🦸")
        await e.edit("🚶                    🦸")
        await e.edit("🚶                     🦸")
        await e.edit("🚶                      🦸")
        await e.edit("🚶                       🦸")
        await e.edit("🚶                        🦸")
        await e.edit("🚶                         🦸")
        await e.edit("🚶                          🦸")
        await e.edit("🚶                           🦸")
        await e.edit("🚶                            🦸")
        await e.edit("🚶                             🦸")
        await e.edit("🚶                              🦸")
        await e.edit("🚶                               🦸")
        await e.edit("🚶                                🦸")
        await e.edit("`DAHLAH CAPEK GESS`")


@register(outgoing=True, pattern=r"^\.terkadang(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Terkadang`")
    sleep(1)
    await typew.edit("`Mencintai Seseorang`")
    sleep(1)
    await typew.edit("`Hanya Akan Membuang Waktumu`")
    sleep(1)
    await typew.edit("`Ketika Waktumu Habis`")
    sleep(1)
    await typew.edit("`Tambah Aja 5000 Dapat 2jam lagi`")
    sleep(1)
    await typew.edit("`wkwkwk becanda gess`")


# Create by myself @localheart


@register(outgoing=True, pattern=r"^\.mf$")
async def koc(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`mf g dl` **ミ(ノ;_ _)ノ=3** ")


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "cinta":

        await event.edit(input_str)

        animation_chars = [
            "`Connecting Ke Server Cinta`",
            "`Mencari Target Cinta`",
            "`Mengirim Cintaku.. 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Mengirim Cintaku.. 84%\n█████████████████████▒▒▒▒ `",
            "`Mengirim Cintaku.. 100%\n█████████CINTAKU███████████ `",
            f"`Cintaku Sekarang Sepenuhnya Terkirim Padamu, Dan Sekarang Aku Sangat Mencintai Mu, I Love You 💞`",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


@register(outgoing=True, pattern=r"^\.gombal(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`Hai, I LOVE YOU 💞`")
    sleep(1)
    await typew.edit("`I LOVE YOU SO MUCH!`")
    sleep(1)
    await typew.edit("`I NEED YOU!`")
    sleep(1)
    await typew.edit("`I WANT TO BE YOUR BOYFRIEND!`")
    sleep(1)
    await typew.edit("`I LOVEE YOUUUU💕💗`")
    sleep(1)
    await typew.edit("`I LOVEE YOUUUU💗💞`")
    sleep(1)
    await typew.edit("`I LOVEE YOUUUU💝💗`")
    sleep(1)
    await typew.edit("`I LOVEE YOUUUU💟💖`")
    sleep(1)
    await typew.edit("`I LOVEE YOUUUU💘💓`")
    sleep(1)
    await typew.edit("`Tapi Bo'ong hayuuu, Palpale Palpale`")


# Create by myself @localheart


@register(outgoing=True, pattern=r"^\.helikopter(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "▬▬▬.◙.▬▬▬ \n"
        "═▂▄▄▓▄▄▂ \n"
        "◢◤ █▀▀████▄▄▄▄◢◤ \n"
        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬ \n"
        "◥█████◤ \n"
        "══╩══╩══ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ Hallo gesss :) \n"
        "╬═╬☻/ \n"
        "╬═╬/▌ \n"
        "╬═╬/ \\ \n"
    )


@register(outgoing=True, pattern=r"^\.tembak(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "_/﹋\\_\n" "(҂`_´)\n" "<,︻╦╤─ ҉\n" r"_/﹋\_" "\n**Mau Jadi Pacarku Gak?!**"
    )


@register(outgoing=True, pattern=r"^\.bundir(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "`Dadah gesssssss...`          \n　　　　　|"
        "\n　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　／￣￣＼| \n"
        "＜ ´･ 　　 |＼ \n"
        "　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n"
        "　＼＿＿／∪ _ ∪) \n"
        "　　　　　 Ｕ Ｕ\n"
    )


@register(outgoing=True, pattern=r"^\.awk(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "────██──────▀▀▀██\n"
        "──▄▀█▄▄▄─────▄▀█▄▄▄\n"
        "▄▀──█▄▄──────█─█▄▄\n"
        "─▄▄▄▀──▀▄───▄▄▄▀──▀▄\n"
        "─▀───────▀▀─▀───────▀▀\n`Awkwokwokwok..`"
    )


@register(outgoing=True, pattern=r"^\.ular(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "░░░░▓\n"
        "░░░▓▓\n"
        "░░█▓▓█\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓███\n"
        "░░░░██▓▓████\n"
        "░░░░░██▓▓█████\n"
        "░░░░░░██▓▓██████\n"
        "░░░░░░███▓▓███████\n"
        "░░░░░████▓▓████████\n"
        "░░░░█████▓▓█████████\n"
        "░░░█████░░░█████●███\n"
        "░░████░░░░░░░███████\n"
        "░░███░░░░░░░░░██████\n"
        "░░██░░░░░░░░░░░████\n"
        "░░░░░░░░░░░░░░░░███\n"
        "░░░░░░░░░░░░░░░░░░░\n"
    )


@register(outgoing=True, pattern=r"^\.y(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "‡‡‡‡‡‡‡‡‡‡‡‡▄▄▄▄\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡█‡‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡█‡‡‡‡‡‡█\n"
        "██████▄▄█‡‡‡‡‡‡████████▄\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█████‡‡‡‡‡‡‡‡‡‡‡‡██\n"
        "█████‡‡‡‡‡‡‡██████████\n"
    )


@register(outgoing=True, pattern=r"^\.tank(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "█۞███████]▄▄▄▄▄▄▄▄▄▄▃ \n"
        "▂▄▅█████████▅▄▃▂…\n"
        "[███████████████████]\n"
        "◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤\n"
    )


@register(outgoing=True, pattern=r"^\.babi(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "┈┈┏━╮╭━┓┈╭━━━━╮\n"
        "┈┈┃┏┗┛┓┃╭┫Tuni ┃\n"
        "┈┈╰┓▋▋┏╯╯╰━━━━╯\n"
        "┈╭━┻╮╲┗━━━━╮╭╮┈\n"
        "┈┃▎▎┃╲╲╲╲╲╲┣━╯┈\n"
        "┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
        "┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n"
        "┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n"
    )


@register(outgoing=True, pattern=r"^\.ajg(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "╥━━━━━━━━╭━━╮━━┳\n"
        "╢╭╮╭━━━━━┫┃▋▋━▅┣\n"
        "╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫┣\n"
        "╢╰━┫┈┈┈┈┈╰╯╰┳━╯┣\n"
        "╢┊┊┃┏┳┳━━┓┏┳┫┊┊┣\n"
        "╨━━┗┛┗┛━━┗┛┗┛━━┻\n"
    )


@register(outgoing=True, pattern=r"^\.bernyanyi(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Ganteng Doang Gak Bernyanyi (ง˙o˙)ว**")
    sleep(2)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")
    sleep(1)
    await typew.edit("**♪┏(・o･)┛♪┗ ( ･o･) ┓**")
    sleep(1)
    await typew.edit("**♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪**")


@register(outgoing=True, pattern=r"^\.hua$")
async def koc(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("أ‿أ")
        await e.edit("╥﹏╥")
        await e.edit("(;﹏;)")
        await e.edit("(ToT)")
        await e.edit("(┳Д┳)")
        await e.edit("(ಥ﹏ಥ)")
        await e.edit("（；へ：）")
        await e.edit("(T＿T)")
        await e.edit("（πーπ）")
        await e.edit("(Ｔ▽Ｔ)")
        await e.edit("(⋟﹏⋞)")
        await e.edit("（ｉДｉ）")
        await e.edit("(´Д⊂ヽ")
        await e.edit("(;Д;)")
        await e.edit("（>﹏<）")
        await e.edit("(TдT)")
        await e.edit("(つ﹏⊂)")
        await e.edit("༼☯﹏☯༽")
        await e.edit("(ノ﹏ヽ)")
        await e.edit("(ノAヽ)")
        await e.edit("(╥_╥)")
        await e.edit("(T⌓T)")
        await e.edit("(༎ຶ⌑༎ຶ)")
        await e.edit("(☍﹏⁰)｡")
        await e.edit("(ಥ_ʖಥ)")
        await e.edit("(つд⊂)")
        await e.edit("(≖͞_≖̥)")
        await e.edit("(இ﹏இ`｡)")
        await e.edit("༼ಢ_ಢ༽")
        await e.edit("༼ ༎ຶ ෴ ༎ຶ༽")


@register(outgoing=True, pattern=r"^\.huh(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n />❤️ *Ini Buat Kamu`")
    sleep(3)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n/>💔  *Aku Ambil Lagi`")
    sleep(2)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n💔<\\  *Terimakasih`")


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 3

    animation_ttl = range(0, 103)

    input_str = event.pattern_match.group(1)

    if input_str == "ceritangenskuy":

        await event.edit(input_str)

        animation_chars = [
            "`Cerita Ngenskuy` ",
            "  😐             😕 \n/👕\\         <👗\\ \n 👖               /|",
            "  😉          😳 \n/👕\\       /👗\\ \n  👖            /|",
            "  😚            😒 \n/👕\\         <👗> \n  👖             /|",
            "  😍         ☺️ \n/👕\\      /👗\\ \n  👖          /|",
            "  😍          😍 \n/👕\\       /👗\\ \n  👖           /|",
            "  😘   😊 \n /👕\\/👗\\ \n   👖   /|",
            " 😳  😁 \n /|\\ /👙\\ \n /     / |",
            "😈    /😰\\ \n<|\\      👙 \n /🍆    / |",
            "😅 \n/(),✊😮 \n /\\         _/\\/|",
            "😎 \n/\\_,__😫 \n  //    //       \\",
            "😖 \n/\\_,💦_😋  \n  //         //        \\",
            "  😭      ☺️ \n  /|\\   /(👶)\\ \n  /!\\   / \\ ",
            "`TAMAT 😅`",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 103])


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 1

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "canda":

        await event.edit(input_str)

        animation_chars = [
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀   ⢳⡀⠀⡏⠀⠀⠀   ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀  ⠀   ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Kamu    ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀⠀__⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀  ⠀⢳⡀⠀⡏⠀⠀⠀   ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀      ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Pasti   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀|__|⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀     ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Belum   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀         ⡇\n  ⠙⢿⣯⠄⠀⠀(x)⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀     ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀   ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Mandi  ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀   ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀⠀__ ⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀   ⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀ ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Bwhaha  ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀  ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀|__| ⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
            "`⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀\n ⠀⣴⠿⠏⠀⠀⠀⠀⠀  ⠀⢳⡀⠀⡏⠀⠀    ⠀⢷\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀  ⠀     ⡇\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿  ⣸ Canda   ⡇\n ⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀   ⣿  ⢹⠀        ⡇\n  ⠙⢿⣯⠄⠀⠀****⠀⠀⡿ ⠀⡇⠀⠀⠀⠀    ⡼\n⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀   ⠘⠤⣄⣠⠞⠀\n⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀ ⠀⣄⢸⠀⠀⠀⠀⠀⠀`",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


@register(outgoing=True, pattern=r"^\.santet(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Mengaktifkan Perintah Santet Online....`")
    sleep(2)
    await typew.edit("`Mencari Nama Orang Ini...`")
    sleep(1)
    await typew.edit("`Santet Online Segera Dilakukan`")
    sleep(1)
    await typew.edit("0%")
    number = 1
    await typew.edit(str(number) + "%   ▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▊")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▉")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▎")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▍")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▌")
    number = number + 1
    sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▌")
    sleep(1)
    await typew.edit("`Target Berhasil Tersantet Online 🥴`")


@register(outgoing=True, pattern="^.nah(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n />💖 *Ini Buat Kamu`")
    sleep(2)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n💖<\\  *Tapi Bo'ong`")


# Alpinnnn Gans


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 0.5

    animation_ttl = range(0, 6)

    input_str = event.pattern_match.group(1)

    if input_str == "owner":

        await event.edit(input_str)

        animation_chars = [
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬜⬛\n⬛⬛⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬛⬜⬜⬛⬛\n⬛⬛⬜⬜⬛⬛\n⬛⬛⬜⬜⬛⬛\n⬛⬛⬜⬜⬛⬛\n⬛⬛⬜⬜⬛⬛\n⬛⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬜⬛⬛⬜⬛\n⬛⬛⬛⬛⬛⬛",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 6])


CMD_HELP.update(
    {
        "animasi": "`.gabut` ; `.sultan`\
    \nUsage: ntahlah gabut doang.\
    \n\n`.gombal`\
    \nUsage: buat bercanda\
    \n\n`.cinta`\
    \nUsage: mengirim cintamu ke seseorang.\
    \n\n`.sayang`\
    \nUsage: untuk jadi buaya.\
    \n\n`.terkadang`\
    \nUsage: Auk dah iseng doang.\
    \n\n`.helikopter` ; `.tank` ; `.tembak`\n`.bundir`\
    \nUsage: liat sendiri\
    \n\n`.y`\
    \nUsage: jempol\
    \n\n`.avengers` ; `.hati` ; `.bernyanyi`\
    \nUsage: liat aja.\
    \n\n`.awk`\
    \nUsage: ketawa lari.\
    \n\n`.ular` ; `.babi` ; `.ajg`\
    \nUsage: liat sendiri.\
    \n\n`.nah` ; `.huh` ; `.owner`\
    \nUsage: cobain.\
    \n\n`.bunga` ; `.buah`\
    \nUsage: animasi.\
    \n\n`.waktu`\
    \nUsage: animasi.\
    \n\n`.hua`\
    \nUsage: nangis.\
    \n\n`.ceritacinta` ; `.canda`\
    \nUsage: liat sendiri\
    \n\n`.santet`\
    \nUsage: Santet Online Buat Bercanda."
    }
)
