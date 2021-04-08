from time import sleep

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.sayang(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(3)
    await typew.edit("**Cuma Mau Bilang**")
    sleep(3)
    await typew.edit("**Aku Sayang Kamu**")
    sleep(1)
    await typew.edit("**I LOVE YOU 💞**")


# Create by myself @localheart


@register(outgoing=True, pattern="^.semangat(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(3)
    await typew.edit("**Apapun Yang Terjadi**")
    sleep(3)
    await typew.edit("**Tetaplah Bernapas**")
    sleep(1)
    await typew.edit("**Dan Selalu Bersyukur**")


# Create by myself @localheart


@register(outgoing=True, pattern="^.ywc(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**Sama sama kawan**")


@register(outgoing=True, pattern="^.jamet(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**WOII**")
    sleep(1.5)
    await typew.edit("**JAMET**")
    sleep(1.5)
    await typew.edit("**CUMA MAU BILANG**")
    sleep(1.5)
    await typew.edit("**GAUSAH SO ASIK**")
    sleep(1.5)
    await typew.edit("**EMANG KENAL?**")
    sleep(1.5)
    await typew.edit("**GAUSAH REPLY**")
    sleep(1.5)
    await typew.edit("**KITA BUKAN KAWAN**")
    sleep(1.5)
    await typew.edit("**GASUKA PC ANJING**")
    sleep(1.5)
    await typew.edit("**BOCAH KAMPUNG**")
    sleep(1.5)
    await typew.edit("MENTAL TEMPE")
    sleep(1.5)
    await typew.edit("LEMBEK NGENTOT🔥")


@register(outgoing=True, pattern="^.pp(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit(
        "**PASANG PP DULU GOBLOK,BIAR ORANG-ORANG PADA TAU BETAPA HINA NYA MUKA LU 😆**"
    )


@register(outgoing=True, pattern="^.dp(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**MUKA LU HINA, GAUSAH SOK KERAS YA ANJENGG!!**")


@register(outgoing=True, pattern="^.so(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**GAUSAH SOKAB SAMA GUA GOBLOK, LU BABU GA LEVEL!!**")


@register(outgoing=True, pattern="^.nb(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**MAEN BOT MULU ALAY NGENTOTT, KESANNYA NORAK GOBLOK!!!**")


CMD_HELP.update(
    {
        "war": "**Plugin : **`War Typing Telegram`\
        \n\n  •  **Syntax :** `.jamet`\
        \n  •  **Function : **Menghina Jamet telegram\
        \n\n  •  **Syntax :** `.pp`\
        \n  •  **Function : **Menghina Jamet telegram yang ga pake foto profil\
        \n\n  •  **Syntax :** `.dp`\
        \n  •  **Function : **Menghina Jamet muka hina!\
        \n\n  •  **Syntax :** `.so`\
        \n  •  **Function : **Ngeledek orang sokab\
        \n\n  •  **Syntax :** `.nb`\
        \n  •  **Function : **Ngeledek orang norak baru pake bot\
        \n\n**Klo mau Req, kosa kata dari lu Hubungi @mrismanaziz**\
    "
    }
)
