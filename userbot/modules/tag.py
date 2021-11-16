# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# Recode by @mrismanaziz
# @sharinguserbot

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.types import UserStatusRecently as rec
from telethon.utils import get_display_name

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import man_cmd


@man_cmd(pattern="tag(on|off|all|bots|rec|admins|owner)?(.*)")
async def _(e):
    okk = e.text
    lll = e.pattern_match.group(2)
    o = 0
    nn = 0
    rece = 0
    xx = f"{lll}" if lll else ""
    xnxx = await e.client.get_participants(e.chat_id, limit=99)
    for users, bb in enumerate(xnxx):
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            if "on" in okk:
                xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, off):
            nn += 1
            if "off" in okk and not bb.bot and not bb.deleted:
                xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, rec):
            rece += 1
            if "rec" in okk and not bb.bot and not bb.deleted:
                xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(y, owner):
            xx += f"\n👑 [{get_display_name(bb)}](tg://user?id={bb.id}) 👑"
        if isinstance(y, admin) and "admin" in okk and not bb.deleted:
            xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if "all" in okk and not bb.bot and not bb.deleted:
            xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if "bot" in okk and bb.bot:
            xx += f"\n🤖 [{get_display_name(bb)}](tg://user?id={bb.id})"
    await e.client.send_message(e.chat_id, xx)
    await e.delete()


CMD_HELP.update(
    {
        "tagger": f"**Plugin : **`tagger`\
        \n\n  •  **Syntax :** `{cmd}tagall`\
        \n  •  **Function : **Tag Top 100 Members di group chat.\
        \n\n  •  **Syntax :** `{cmd}tagowner`\
        \n  •  **Function : **Tag Owner group chat\
        \n\n  •  **Syntax : **`{cmd}tagadmins`\
        \n  •  **Function : **Tag Admins group chat.\
        \n\n  •  **Syntax :** `{cmd}tagbots`\
        \n  •  **Function : **Tag Bots group chat.\
        \n\n  •  **Syntax :** `{cmd}tagrec`\
        \n  •  **Function : **Tag Member yang Baru Aktif.\
        \n\n  •  **Syntax :** `{cmd}tagon`\
        \n  •  **Function : **Tag Online Members (hanya berfungsi jika privasi dimatikan)\
        \n\n  •  **Syntax :** `{cmd}tagoff`\
        \n  •  **Function : **Tag Offline Members (hanya berfungsi jika privasi dimatikan)\
        "
    }
)
