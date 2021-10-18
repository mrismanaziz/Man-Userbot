import requests
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS, bot
from userbot.events import man_cmd, register
from userbot.utils import edit_or_reply


@bot.on(man_cmd(outgoing=True, pattern="truth$"))
@register(incoming=True, from_users=DEVS, pattern=r"^\.ctruth$")
async def tede_truth(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/truth").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Truth**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Something went wrong LOL...**")


@bot.on(man_cmd(outgoing=True, pattern="dare$"))
@register(incoming=True, from_users=DEVS, pattern=r"^\.cdare$")
async def tede_dare(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/dare").json()
        results = resp["message"]
        await edit_or_reply(event, f"**#Dare**\n\n`{results}`")
    except Exception:
        await edit_or_reply(event, "**Something went wrong LOL...**")


CMD_HELP.update(
    {
        "truthdare": f"**Plugin : **`truthdare`\
        \n\n  •  **Syntax :** `{cmd}truth`\
        \n  •  **Function : **Untuk tantangan.\
        \n\n  •  **Syntax :** `{cmd}dare`\
        \n  •  **Function : **Untuk kejujuran.\
    "
    }
)
