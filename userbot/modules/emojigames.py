# fix by @heyworld for OUB
# bug fixed by @d3athwarrior

from telethon.tl.types import InputMediaDice

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(""))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))
        except BaseException:
            pass


@register(outgoing=True, pattern="^.dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎯"))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except BaseException:
            pass


@register(outgoing=True, pattern="^.ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except BaseException:
            pass


CMD_HELP.update(
    {
        "emojigames": "**Plugin : **`emojigames`\
        \n\n  •  **Syntax :** `.dice` 1-6\
        \n  •  **Function : **Memainkan game dice telegram score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.dart` 1-6\
        \n  •  **Function : **Memainkan game dart telegram score yg di tentukan kita.\
        \n\n  •  **Syntax :** `.ball` 1-5\
        \n  •  **Function : **Memainkan game ball telegram score yg di tentukan kita.\
        \n\n  •  **NOTE: **Jangan gunakan nilai lebih atau bot akan Crash**\
    "
    }
)
