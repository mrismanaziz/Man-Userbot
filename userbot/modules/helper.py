""" Userbot module for other small commands. """
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="ihelp$")
async def usit(event):
    me = await event.client.get_me()
    await edit_or_reply(
        event,
        f"**Hai {me.first_name} Kalo Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.help` Atau Bisa Minta Bantuan Ke:\n"
        f"✣ **Group Support :** [Sharing Userbot](t.me/sharinguserbot)\n"
        f"✣ **Channel Man :** [Lunatic0de](t.me/Lunatic0de)\n"
        f"✣ **Owner Repo :** [Risman](t.me/mrismanaziz)\n"
        f"✣ **Repo :** [Man-Userbot](https://github.com/mrismanaziz/Man-Userbot)\n",
    )


@man_cmd(pattern="listvar$")
async def var(event):
    await edit_or_reply(
        event,
        "**Daftar Lengkap Vars Dari Man-Userbot:** [KLIK DISINI](https://telegra.ph/List-Variabel-Heroku-untuk-Man-Userbot-09-22)",
    )


CMD_HELP.update(
    {
        "helper": f"**Plugin : **`helper`\
        \n\n  •  **Syntax :** `{cmd}ihelp`\
        \n  •  **Function : **Bantuan Untuk Man-Userbot.\
        \n\n  •  **Syntax :** `{cmd}listvar`\
        \n  •  **Function : **Melihat Daftar Vars.\
        \n\n  •  **Syntax :** `{cmd}repo`\
        \n  •  **Function : **Melihat Repository Man-Userbot.\
        \n\n  •  **Syntax :** `{cmd}string`\
        \n  •  **Function : **Link untuk mengambil String Man-Userbot.\
    "
    }
)
