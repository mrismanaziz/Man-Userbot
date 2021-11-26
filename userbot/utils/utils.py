# Credits: @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import importlib
import logging
import sys
from pathlib import Path
from random import randint

import heroku3
from telethon.tl.functions.contacts import UnblockRequest

from userbot import (
    BOT_TOKEN,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGS,
    bot,
)

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


async def autobot():
    if BOT_TOKEN:
        return
    await bot.start()
    await bot.send_message(
        BOTLOG_CHATID, "**SEDANG MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather**"
    )
    who = await bot.get_me()
    name = who.first_name + " Assistant Bot"
    if who.username:
        username = who.username + "_ubot"
    else:
        username = "man" + (str(who.id))[5:] + "ubot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "man" + (str(who.id))[6:] + str(ran) + "ubot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_file(bf, "userbot/resources/logo.jpg")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(
                bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @Lunatic0de ✨"
            )
            await bot.send_message(
                BOTLOG_CHATID,
                f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
            )
            await bot.send_message(
                BOTLOG_CHATID,
                "**Tunggu Sebentar, Sedang MeRestart Heroku untuk Menerapkan Perubahan.**",
            )
            heroku_var["BOT_TOKEN"] = token
            heroku_var["BOT_USERNAME"] = f"@{username}"
        else:
            LOGS.info(
                "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setuserpic")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_file(bf, "userbot/resources/logo.jpg")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(
            bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @Lunatic0de ✨"
        )
        await bot.send_message(
            BOTLOG_CHATID,
            f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
        )
        await bot.send_message(
            BOTLOG_CHATID,
            "**Tunggu Sebentar, Sedang MeRestart Heroku untuk Menerapkan Perubahan.**",
        )
        heroku_var["BOT_TOKEN"] = token
        heroku_var["BOT_USERNAME"] = f"@{username}"
    else:
        LOGS.info(
            "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
        )
        sys.exit(1)


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/modules/{shortname}.py")
        name = "userbot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Successfully imported " + shortname)
    else:

        path = Path(f"userbot/modules/{shortname}.py")
        name = "userbot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.LOGS = LOGS
        mod.CMD_HELP = CMD_HELP
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.modules." + shortname] = mod
        LOGS.info("Successfully imported " + shortname)


def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = "userbot.modules.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Starting Your Assistant Bot.")
        LOGS.info("Assistant Sucessfully imported " + shortname)
    else:
        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = "userbot.modules.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["userbot.modules.assistant" + shortname] = mod
        LOGS.info("Assistant Successfully imported" + shortname)


def remove_plugin(shortname):
    try:
        try:
            for i in CMD_HELP[shortname]:
                bot.remove_event_handler(i)
            del CMD_HELP[shortname]

        except BaseException:
            name = f"userbot.modules.{shortname}"

            for i in reversed(range(len(bot._event_builders))):
                ev, cb = bot._event_builders[i]
                if cb.__module__ == name:
                    del bot._event_builders[i]
    except BaseException:
        raise ValueError
