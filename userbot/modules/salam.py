from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, owner
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="p(?: |$)(.*)")
async def _(event):
    await edit_or_reply(event, "**Assalamualaikum Anak Ngentot**")


@man_cmd(pattern="pe(?: |$)(.*)")
async def _(event):
    await edit_or_reply(event, "**Assalamualaikum, Jadi Ngentot Ga?**")


@man_cmd(pattern="P(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Haii Salken Saya {owner}**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@man_cmd(pattern="l(?: |$)(.*)")
async def _(event):
    await edit_or_reply(event, "**Wa'alaikumsalam Anak Anjing**")


@man_cmd(pattern="a(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Haii Salken Saya {owner}**")
    sleep(2)
    await xx.edit("**Assalamualaikum**")


@man_cmd(pattern="j(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**JAKA SEMBUNG BELI DUREN**")
    sleep(3)
    await xx.edit("**MENDING LU SUREN🔥**")


@man_cmd(pattern="k(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**HALLO YATIM PIATU GUA{owner}**")
    sleep(2)
    await xx.edit("**LU SEMUA GOBLOK ANJING 🔥**")


@man_cmd(pattern="kntl(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, "**LU SEMUA KONTOL**")
    sleep(2)
    await xx.edit("**KALO JELEK MINIMAL MANDI NGENTOT**")
    (sleep)(2) 
    await xx.edit("**UDAH JELEK GAPERNAH MANDI**") 
    (sleep)(2) 
    await xx.edit("**KALO GAPUNYA AIR BILANG NGENTOT**") 
    (sleep)(2) 
    await xx.edit("**BIAR GUA KASI AIR COMBERAN ANJING**") 
    (sleep)(2) 
    await xx.edit("**MUKA ITEM KEK KETAN ITEM BANGSAT**") 
    (sleep)(2) 
    await xx.edit("**KAKI LU BANYAK KORENGNYA TOLOL**") 
    (sleep)(2) 
    await xx.edit("**MUKA LU AJA ITU MIRIP MONYET RAGUNAN BEGO**") 
    (sleep)(2) 
    await xx.edit("**DASAR ANAK LUTUNG**") 
    (sleep)(2)
    await xx.edit("**MENDING LU MULUNG**") 
    (sleep)(2)
    await xx.edit("**BOCAH GATAU DI UNTUNG**") 
    (sleep)(2) 
    await xx.edit("**MUKA KAYA GEMBELAN LAMPUNG**") 
    (sleep)(2) 
    await xx.edit("**BUNTUNGG BUNTUNGG**") 

CMD_HELP.update(
    {
        "salam": f"**Plugin : **`salam`\
        \n\n  •  **Syntax :** `{cmd}p`\
        \n  •  **Function : **salam \
        \n\n  •  **Syntax :** `{cmd}pe`\
        \n  •  **Function : **salam Kenal dan salam\
        \n\n  •  **Syntax :** `{cmd}l`\
        \n  •  **Function : **Untuk Menjawab salam\
        \n\n  •  **Syntax :** `{cmd}a`\
        \n  •  **Function : **coba aja dongo\
        \n\n  •  **Syntax :** `{cmd}j`\
        \n  •  **Function : **Kasi Pantun.\
        \n\n  •  **Syntax :** `{cmd}kntl`\
        \n  •  **Function : **hina orang jelek\
    "
    }
)
