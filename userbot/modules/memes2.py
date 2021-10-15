from random import choice

from userbot import bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"gey$"))
async def gey(e):
        await e.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈Lu Bau Hehe`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"gay$"))
async def gey(e):
        await e.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈ANDA GAY`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"bot$"))
async def bot(e):
        await e.edit(
            "` \n   ╲╲╭━━━━╮ \n╭╮┃▆┈┈▆┃╭╮ \n┃╰┫▽▽▽┣╯┃ \n╰━┫△△△┣━╯`"
            "`\n╲╲┃┈┈┈┈┃  \n╲╲┃┈┏┓┈┃ `"
        )


@bot.on(man_cmd(outgoing=True, pattern=r"koc$"))
async def koc(e):
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8✊===D")
        await e.edit("8=✊==D")
        await e.edit("8==✊=D")
        await e.edit("8===✊D")
        await e.edit("8==✊=D")
        await e.edit("8=✊==D")
        await e.edit("8===✊D💦")
        await e.edit("8==✊=D💦💦")
        await e.edit("8=✊==D💦💦💦")
        await e.edit("8✊===D💦💦💦💦")
        await e.edit("8===✊D💦💦💦💦💦")
        await e.edit("8==✊=D💦💦💦💦💦💦")
        await e.edit("8=✊==D💦💦💦💦💦💦💦")
        await e.edit("8✊===D💦💦💦💦💦💦💦💦")
        await e.edit("8===✊D💦💦💦💦💦💦💦💦💦")
        await e.edit("8==✊=D💦💦💦💦💦💦💦💦💦💦")
        await e.edit("8=✊==D Lah Kok Habis?")
        await e.edit("😭😭😭😭")


@bot.on(man_cmd(outgoing=True, pattern="gas$"))
async def gas(e):
        await e.edit("___________________🚑")
        await e.edit("________________🚑___")
        await e.edit("______________🚑_____")
        await e.edit("___________🚑________")
        await e.edit("________🚑___________")
        await e.edit("_____🚑______________")
        await e.edit("__🚑_________________")
        await e.edit("🚑___________________")
        await e.edit("_____________________")
        await e.edit(choice(FACEREACTS))


@bot.on(man_cmd(outgoing=True, pattern=r"shg$"))
async def shrugger(shg):
    r"""¯\_(ツ)_/¯"""
    await shg.edit(choice(SHGS))


@bot.on(man_cmd(outgoing=True, pattern=r"(?:penis|dick)\s?(.)?"))
async def emoji_penis(e):
    emoji = e.pattern_match.group(1)
    titid = GAMBAR_TITIT
    if emoji:
        titid = titid.replace("😋", emoji)
    await e.edit(titid)


@bot.on(man_cmd(outgoing=True, pattern=r"(?:kontol)\s?(.)?"))
async def emoji_kontl(e):
    emoji = e.pattern_match.group(1)
    kontl = GAMBAR_KONTL
    if emoji:
        kontl = kontl.replace("😂", emoji)
    await e.edit(kontl)


@bot.on(man_cmd(outgoing=True, pattern=r"skull$"))
async def emoji_tengkorak(e):
    emoji = e.pattern_match.group(1)
    tengkorak = GAMBAR_TENGKORAK
    if emoji:
        tengkorak = tengkorak.replace("😂", emoji)
    await e.edit(tengkorak)
