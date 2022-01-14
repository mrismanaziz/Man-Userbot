from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"kenalin(?: |$)(.*)"))
async def _(event):
    await event.edit("`Woy Kenalin Gw {owner}, Orang Paling Ganteng`")
    sleep(2)
    await event.edit("`Apa Lu? Sirik Sama Gw? Haha Goblok Babu`")
    sleep(2)
    await event.edit("`Makanya Ganteng Tolol Haha,Anak Stell Kalem Nih Boss🔥🔥`")


@bot.on(man_cmd(outgoing=True, pattern=r"kalem(?: |$)(.*)"))
async def _(event):
    await event.edit("`STELL KALEM NIH BOS🔥`")
    (sleep)(2)
    await event.edit("`ANTI KUBU KUBU TAI ANJING`")
    (sleep)(2)
    await event.edit("`GUA PANTUNIN DULU YEKANNN`")
    (sleep)(2)
    await event.edit("`JALAN JALAN BARENG SI GALANG`")
    (sleep)(2)
    await event.edit("`PULANGNYA BELI GELANG`")
    (sleep)(2)
    await event.edit("`KALO GAKUAT SILAHKAN BILANG`")
    (sleep)(2)
    await event.edit("`KARENA GA BUTUH MENTAL PECUNDANG`")
    (sleep)(2)
    await event.edit("`YAHAHA WAHYOE`")
    (sleep)(2)
    await event.edit("`UDAH KALEM PALING OP TOLOL🔥`")
    (sleep)(2)
    await event.edit("`KALO MASIH BERALIBI`")
    (sleep)(2) 
    await event.edit("`JANGAN NANTANG SANA SINI`") 
    (sleep)(2)
    await event.edit("`DASAR BOCAH GAADA AKSI`")
    (sleep)(2)
    await event.edit("`KACUNG ALIANSI`")
    (sleep)(2)
    await event.edit("`DASAR TUKANG JUALAN KAOS KAKI`")
    (sleep)(2)
    await event.edit("`MUKA KAYA AKI AKI`")
    (sleep)(2)
    await event.edit("`MENDING LU PULANG BANTU NYUCI TOLOL`")
    (sleep)(2)
    await event.edit("`SLOWLY CALM AND FIGHT🔥`")
    (sleep)(2)

@bot.on(man_cmd(outgoing=True, pattern=r"dor(?: |$)(.*)"))
async def _(event):
    await event.edit("`DARR DEER DORR`")
    (sleep)(2)
    await event.edit("`MENTAL BAPAK LU GUA GEDOR`")
    (sleep)(2)
    await event.edit("`GUA PANTUNIN DULU YEKANNN`")
    (sleep)(2)
    await event.edit("`SI OJOK MAKAN KEPITING`")
    (sleep)(2)
    await event.edit("`SI JAYA PERGI KE HUNTING`")
    (sleep)(2)
    await event.edit("`EHH BOCAH GOBLOK RAMBUT KRITING`")
    (sleep)(2)
    await event.edit("`JANGAN BANYAK GAYA KALO GAMAU DI BANTING`")
    (sleep)(2)
    await event.edit("`YAHAHA WAHYOE`")
    (sleep)(2)
    await event.edit("`BOCAH GATAU DI UNTUNG`")
    (sleep)(2)
    await event.edit("`MUKA MIRIP LUTUNG`")
    (sleep)(2)
    await event.edit("`DASAR ANAK TUKANG PULUNG`")
    (sleep)(2)
    await event.edit("`BADAN KURUS KERING`")
    (sleep)(2)
    await event.edit("`RAMBUT KERITING`")
    (sleep)(2)
    await event.edit("`BOCAH KAMPUNG ANJING`")
    (sleep)(2)
    await event.edit("`KAMPUNG KAMPUNG🔥`")
    (sleep)(2)


# Create by myself @localheart


@bot.on(man_cmd(outgoing=True, pattern=r"punten(?: |$)(.*)"))
async def _(event):
    await event.edit(
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Punten Mamank**"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"pantau(?: |$)(.*)"))
async def _(event):
    await event.edit(
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Masih Gua Pantau Ajg**"
    )


# Create by myself @localheart


CMD_HELP.update(
    {
        "punten": f"**Plugin : **`Animasi Punten`\
        \n\n  •  **Syntax :** `{cmd}punten` ; `{cmd}pantau`\
        \n  •  **Function : **Arts Beruang kek lagi mantau.\
        \n\n  •  **Syntax :** `{cmd}kalem` ; `{cmd}dor`\
        \n  •  **Function : **coba aja tolol🔥.\
        \n\n  •  **Syntax :** `{cmd}kenalin`\
        \n  •  **Function : **perkenalkan.\
    "
    }
)
