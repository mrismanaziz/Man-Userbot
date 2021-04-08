# created by @eve_enryu

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.firmware(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    firmware = "firmware"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{firmware} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.fastboot(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    fboot = "fastboot"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{fboot} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBoot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.recovery(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    recovery = "recovery"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{recovery} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.pb(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    pitch = "pb"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{pitch} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.of(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    ofox = "of"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{ofox} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.eu(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    eu = "eu"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{eu} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.vendor(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    vendor = "vendor"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{vendor} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.specs(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    specs = "specs"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=774181428)
            )
            await conv.send_message(f"/{specs} {link}")
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @XiaomiGeeksBot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)


CMD_HELP.update(
    {
        "xiaomi": "**Plugin : **`xiaomi`\
        \n\n  •  **Syntax :** `firmware` (codename)\
        \n  •  **Function : **Get lastest Firmware.\
        \n\n  •  **Syntax :** `.pb` (codename)\
        \n  •  **Function : **Get latest PitchBlack Recovery.\
        \n\n  •  **Syntax :** `.specs` (codename)\
        \n  •  **Function : **Get quick spec information about device.\
        \n\n  •  **Syntax :** `.fastboot` (codename)\
        \n  •  **Function : **Get latest fastboot MIUI.\
        \n\n  •  **Syntax :** `.recovery` (codename)\
        \n  •  **Function : **Get latest recovery MIUI.\
        \n\n  •  **Syntax :** `.eu` (codename)\
        \n  •  **Function : **Get latest xiaomi.eu rom.\
        \n\n  •  **Syntax :** `.vendor` (codename)\
        \n  •  **Function : **fetches latest vendor.\
        \n\n  •  **Syntax :** `.of` (codename)\
        \n  •  **Function : **Get latest ORangeFox Recovery.\
    "
    }
)
