""" Userbot module for other small commands. """
from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.ihelp$")
async def usit(e):
    await e.edit(
        f"**Hai {DEFAULTUSER} Kalo Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.help` Atau Bisa Minta Bantuan Ke:\n"
        "\n[Telegram](t.me/mrismanaziz)"
        "\n[Repo](https://github.com/mrismanaziz/Man-Userbot)"
        "\n[Instagram](Instagram.com/mrismanaziz_)"
    )


@register(outgoing=True, pattern="^.listvar$")
async def var(m):
    await m.edit(
        f"**Disini Daftar Vars Dari {DEFAULTUSER}:**\n"
        "\n[DAFTAR VARS](https://raw.githubusercontent.com/mrismanaziz/Man-Userbot/Man-Userbot/varshelper.txt)"
    )


CMD_HELP.update(
    {
        "helper": "**Plugin : **`helper`\
        \n\n  •  **Syntax :** `.ihelp`\
        \n  •  **Function : **Bantuan Untuk Man-Userbot.\
        \n\n  •  **Syntax :** `.listvar`\
        \n  •  **Function : **Melihat Daftar Vars.\
        \n\n  •  **Syntax :** `.repo`\
        \n  •  **Function : **Melihat Repository Man-Userbot.\
        \n\n  •  **Syntax :** `.string`\
        \n  •  **Function : **Link untuk mengambil String Man-Userbot.\
    "
    }
)
