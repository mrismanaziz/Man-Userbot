from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.utils import man_cmd


@man_cmd(pattern="sadboy(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "`Pertama-tama kamu cantik`")
    sleep(2)
    await xx.edit("`Kedua kamu manis`")
    sleep(1)
    await xx.edit("`Dan yang terakhir adalah kamu bukan jodohku`")


# Create by myself @localheart


@man_cmd(pattern="punten(?: |$)(.*)")
async def _(event):
    await edit_or_reply(event,
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Punten**"
    )


@man_cmd(pattern="pantau(?: |$)(.*)")
async def _(event):
    await edit_or_reply(event,
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
