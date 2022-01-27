# fix by @heyworld for OUB
# bug fixed by @d3athwarrior
# Recode by @mrismanaziz
# t.me/SharingUserbot

from telethon.tl.types import InputMediaDice

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import man_cmd


@man_cmd(pattern="dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(""))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))
        except BaseException:
            pass


@man_cmd(pattern="dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎯"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except BaseException:
            pass


@man_cmd(pattern="basket(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except BaseException:
            pass


@man_cmd(pattern="bowling(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎳"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎳"))
        except BaseException:
            pass


@man_cmd(pattern="ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("⚽"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("⚽"))
        except BaseException:
            pass


@man_cmd(pattern="jackpot(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎰"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎰"))
        except BaseException:
            pass


CMD_HELP.update(
    {
        "emojigames": f"**Plugin : **`emojigames`\
        \n\n  •  **Syntax :** `{cmd}dice` 1-6\
        \n  •  **Function : **Memainkan emoji game dice dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `{cmd}dart` 1-6\
        \n  •  **Function : **Memainkan emoji game dart dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `{cmd}basket` 1-5\
        \n  •  **Function : **Memainkan emoji game basket dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `{cmd}bowling` 1-6\
        \n  •  **Function : **Memainkan emoji game bowling dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `{cmd}ball` 1-5\
        \n  •  **Function : **Memainkan emoji game ball telegram score yg di tentukan kita.\
        \n\n  •  **Syntax :** `{cmd}jackpot` 1\
        \n  •  **Function : **Memainkan emoji game jackpot dengan score yg di tentukan kita.\
        \n\n  •  **NOTE: **Jangan gunakan nilai lebih atau bot akan Crash**\
    "
    }
)
