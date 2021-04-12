# frm Ultroid
# port by Koala @manusiarakitann
# @LordUserbot_Group
# @sharinguserbot

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.gcast (.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`Globally Broadcasting Msg...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **Grup, Gagal Mengirim Pesan Ke** `{er}` **Grup**"
    )


CMD_HELP.update(
    {
        "gcast": "**Plugin : **`gcast`\
        \n\n  •  **Syntax :** `.gcast` <text>`\
        \n  •  **Function : **Mengirim  Global Broadcast pesan ke Seluruh Grup yang kamu masuk.\
    "
    }
)
