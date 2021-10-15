# Based Plugins
# Ported For Lord-Userbot By liualvinas/Alvin
# If You Kang It Don't Delete / Warning!! Jangan Hapus Ini!!!
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"xogame(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


# Alvin Gans


@bot.on(man_cmd(outgoing=True, pattern=r"wp(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    wwwspr = event.pattern_match.group(1)
    botusername = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, wwwspr)
    await tap[0].click(event.chat_id)
    await event.delete()


# Alvin Gans


@bot.on(man_cmd(outgoing=True, pattern=r"mod(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()


# Ported For Lord-Userbot By liualvinas/Alvin


CMD_HELP.update(
    {
        "justfun": f"**Plugin : **`justfun`\
        \n\n  •  **Syntax :** `{cmd}xogame`\
        \n  •  **Function : **Game xogame bot\
        \n\n  •  **Syntax :** `{cmd}mod <nama app>`\
        \n  •  **Function : **Dapatkan applikasi mod\
    "
    }
)


CMD_HELP.update(
    {
        "secretchat": f"**Plugin : **`secretchat`\
        \n\n  •  **Syntax :** `{cmd}wp <teks> <username/ID>`\
        \n  •  **Function : **Memberikan pesan rahasia haya orang yang di tag yang bisa melihat\
        \n  •  **Example  : **{cmd}wp aku sayang kamu @mrismanaziz\
    "
    }
)
