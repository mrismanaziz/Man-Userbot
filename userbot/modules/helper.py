""" Userbot module for other small commands. """
from userbot import ALIVE_NAME
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@bot.on(man_cmd(outgoing=True, pattern=r"ihelp$"))
async def usit(e):
    await e.edit(
        f"**Hai {DEFAULTUSER} Kalo Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `.help` Atau Bisa Minta Bantuan Ke:\n"
        f"➤ **ɢʀᴏᴜᴘ sᴜᴘᴘᴏʀᴛ :** [sᴏɴɪᴄ sᴜᴘᴘᴏʀᴛ​](t.me/SonicSupport)\n"
        f"➤ **ᴄʜᴀɴɴᴇʟ sᴏɴɪᴄ :** [sᴏɴɪᴄ ᴜᴘᴅᴀᴛᴇ​](t.me/SonicUpdatee)\n"
        f"➤ **ᴏᴡɴᴇʀ ʀᴇᴘᴏ  :** [ᴄᴀᴠᴇɴᴅɪsʜ](t.me/Badboicartii)\n"
        f"➤ **ʀᴇᴘᴏ :** [sᴏɴɪᴄ-ᴜsᴇʀʙᴏᴛ](https://github.com/SonicXsap/Man-Userbot)\n"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"listvar$"))
async def var(m):
    await m.edit(
        f"**Disini Daftar Vars Dari {DEFAULTUSER}:**\n"
        "\n[DAFTAR VARS](https://telegra.ph/List-Variabel-Heroku-untuk-Man-Userbot-09-22)"
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
