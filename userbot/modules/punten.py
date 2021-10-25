from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"sadboy(?: |$)(.*)"))
async def _(event):
    await event.edit("`Pertama-tama kamu cantik`")
    sleep(2)
    await event.edit("`Kedua kamu manis`")
    sleep(1)
    await event.edit("`Dan yang terakhir adalah kamu bukan jodohku`")


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
        "\n**Punten**"
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
        "\n**Masih Gua Pantau**"
    )


# Create by myself @localheart


CMD_HELP.update(
    {
        "punten": f"**Plugin : **`Animasi Punten`\
        \n\n  •  **Syntax :** `{cmd}punten` ; `{cmd}pantau`\
        \n  •  **Function : **Arts Beruang kek lagi mantau.\
        \n\n  •  **Syntax :** `{cmd}sadboy`\
        \n  •  **Function : **ya sadboy coba aja.\
    "
    }
)
