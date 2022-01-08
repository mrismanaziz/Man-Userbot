   from platform import uname
   from time import sleep

   from userbot import ALIVE_NAME, CMD_HELP, WEATHER_DEFCITY
   from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

# gabut

@register(outgoing=True, pattern=r"^\.jelek(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("**EHH GOBLOK LU JELEK**")
    sleep(2.5)
    await typew.edit("**GAUSA SOSOAN NGEGHOSTING TOLOL**")
    sleep(2.5)
    await typew.edit("**MUKA LU AJA DEKIL GOBLOK**")
    sleep(2.5)
    await typew.edit("**SADAR TOLOL LU JELEK**")
    sleep(2.5)
    await typew.edit("**UDAH JELEK NYAKITIN GOBLOK**")
    sleep(2.5)
    await typew.edit("**DASAR ANAK NGENTOT**")
    sleep(2.5)
    await typew.edit("**DAKI DIMANA MANA**")
    sleep(2.5)
    await typew.edit("**KALO LU JELEK**")
    sleep(2.5)
    await typew.edit("**MINIMAL MANDILAH KONTOL**")


@register(outgoing=True, pattern="^.kalem(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("**DARR DERR DORR**")
    sleep(2)
    await typew.edit("**STELL KALEM MINTA DI GEDOR**")
    sleep(2)
    await typew.edit("**KUKIRA SITU KERAS🥺**")
    sleep(2)
    await typew.edit("**TERNYATA KERTAS**")
    sleep(2)
    await typew.edit("**AWOKAWOKAWOK**")
    sleep(2)
    await typew.edit("**UDAH GOBLOK**")
    sleep(2)
    await typew.edit("**CIRCLE STELL KALEM PALING OP**")
    sleep(2)
    await typew.edit("**INDEPENDENT NIH BOS**")
    sleep(2)
    await typew.edit("**ANTI KUBU KUBU TAI ANJING**")
    sleep(2)
    await typew.edit("**INTINYA KALEM PALING OP NGENTOT**")

# joo

    CMD_HELP.update(
    
        "gabut": "**Modules** - `Gabut`\
        \n\n Cmd : `.jelek`\
        \nUsage :  `Ngehina orang jelek'\
        "gabut": "**Modules** - `Gabut`\
        \n\n Cmd : `.kalem`\
        \nUsage : `Kalem Nih Bos`\
