# fix by @heyworld for OUB
# bug fixed by @d3athwarrior
# Recode by @mrismanaziz
# t.me/SharingUserbot

from telethon.tl.types import InputMediaDice

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.dice(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.dart(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.basket(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.bowling(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.ball(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.jackpot(?: |$)(.*)")
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
        "emojigames": "**Plugin : **`emojigames`\
        \n\n  •  **Syntax :** `.dice` 1-6\
        \n  •  **Function : **Memainkan emoji game dice dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.dart` 1-6\
        \n  •  **Function : **Memainkan emoji game dart dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.basket` 1-5\
        \n  •  **Function : **Memainkan emoji game basket dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.bowling` 1-6\
        \n  •  **Function : **Memainkan emoji game bowling dengan score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.ball` 1-5\
        \n  •  **Function : **Memainkan emoji game ball telegram score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.jackpot` 1\
        \n  •  **Function : **Memainkan emoji game jackpot dengan score yg di tentukan kita.\
        \n\n  •  **NOTE: **Jangan gunakan nilai lebih atau bot akan Crash**\
    "
    }
)
