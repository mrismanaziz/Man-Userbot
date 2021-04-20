from platform import uname

from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.p(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Assalamu'alaikum Warahmatullahi Wabarakatuh**")


@register(outgoing=True, pattern="^.pe(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Assalamu'alaikum 😍**")


@register(outgoing=True, pattern="^A(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**Hai Salken Saya {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("**Assalamu'alaikum...**")


@register(outgoing=True, pattern="^L(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**😍 Wa'alaikumussalam 💐**")


CMD_HELP.update(
    {
        "salam": "**Plugin : **`salam`\
        \n\n  •  **Syntax :** `.p`\
        \n  •  **Function : **Assalamu'alaikum Warahmatullahi Wabarakatuh..\
        \n\n  •  **Syntax :** `.pe`\
        \n  •  **Function : **salam Kenal dan salam\
        \n\n  •  **Syntax :** `L`\
        \n  •  **Function : **Untuk Menjawab salam\
        \n\n  •  **Syntax :** `.ass`\
        \n  •  **Function : **Salam Bahas arab\
        \n\n  •  **Syntax :** `.semangat`\
        \n  •  **Function : **Memberikan Semangat.\
        \n\n  •  **Syntax :** `.ywc`\
        \n  •  **Function : **nMenampilkan Sama sama\
        \n\n  •  **Syntax :** `.sayang`\
        \n  •  **Function : **Kata I Love You.\
        \n\n  •  **Syntax :** `.k`\
        \n  •  **Function : **LU SEMUA NGENTOT 🔥\
        \n\n  •  **Syntax :** `.j`\
        \n  •  **Function : **NIMBRUNG GOBLOKK!!!🔥\
    "
    }
)
