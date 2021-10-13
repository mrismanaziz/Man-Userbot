from platform import uname

from userbot import ALIVE_NAME
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@bot.on(man_cmd(outgoing=True, pattern="p(?: |$)(.*)"))
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Assalamualaikum Dulu Biar Sopan**")


@bot.on(man_cmd(outgoing=True, pattern=r"pe(?: |$)(.*)"))
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Assalamualaikum Warahmatullahi Wabarakatuh**")


@bot.on(man_cmd(outgoing=True, pattern="P(?: |$)(.*)"))
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**Haii Salken Saya {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("**Assalamualaikum...**")


@bot.on(man_cmd(outgoing=True, pattern=r"l(?: |$)(.*)"))
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Wa'alaikumsalam**")


CMD_HELP.update(
    {
        "salam": f"**Plugin : **`salam`\
        \n\n  •  **Syntax :** `{cmd}p`\
        \n  •  **Function : **Assalamualaikum Dulu Biar Sopan..\
        \n\n  •  **Syntax :** `{cmd}pe`\
        \n  •  **Function : **salam Kenal dan salam\
        \n\n  •  **Syntax :** `{cmd}l`\
        \n  •  **Function : **Untuk Menjawab salam\
        \n\n  •  **Syntax :** `{cmd}ass`\
        \n  •  **Function : **Salam Bahas arab\
        \n\n  •  **Syntax :** `{cmd}semangat`\
        \n  •  **Function : **Memberikan Semangat.\
        \n\n  •  **Syntax :** `{cmd}ywc`\
        \n  •  **Function : **nMenampilkan Sama sama\
        \n\n  •  **Syntax :** `{cmd}sayang`\
        \n  •  **Function : **Kata I Love You.\
        \n\n  •  **Syntax :** `{cmd}k`\
        \n  •  **Function : **LU SEMUA NGENTOT 🔥\
        \n\n  •  **Syntax :** `{cmd}j`\
        \n  •  **Function : **NIMBRUNG GOBLOKK!!!🔥\
    "
    }
)
