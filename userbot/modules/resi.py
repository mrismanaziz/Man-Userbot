from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.resi(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    event.pattern_match.group(1)
    chat = "@GeDebugBetaBot"  # pylint:disable=E0602
    resi = f"resi"  # pylint:disable=E0602
    await event.edit("Processing....")
    async with bot.conversation("@GeDebugBetaBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=443213072)
            )
            await conv.send_message(f"{kurir} {resi}")
            response = await response
        except YouBlockedUserError:
            await event.reply("Unblock @ GeDebugBetaBot dulu Goblok!!")
            return
        else:
            await event.edit(f"{response.message.message}")
            await event.client.delete_messages(response.message.message)


CMD_HELP.update(
    {
        "resi": "**Plugin : **`resi`\
        \n\n  •  **Syntax :** `.resi`\
        \n  •  **Function : **Cek resi.\
        \n\n  •  **Syntax :** `.lacak`\
        \n  •  **Function : **melacak paket.\
    "
    }
)
