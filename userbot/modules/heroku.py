# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
"""
   Heroku manager for your userbot
"""

import math
import os

import aiohttp
import heroku3

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME
from userbot.events import register

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


"""
   ConfigVars setting, get current var, set var or delete var...
"""


@register(outgoing=True, pattern=r"^\.(get|del) var(?: |$)(\w*)")
async def variable(var):
    exe = var.pattern_match.group(1)
    if app is None:
        await var.edit("**[HEROKU]" "\nHarap Siapkan** `HEROKU_APP_NAME`")
        return False
    if exe == "get":
        await var.edit("`Mendapatkan Informasi...`")
        variable = var.pattern_match.group(2)
        if variable == "":
            configvars = heroku_var.to_dict()
            if BOTLOG:
                msg = "".join(
                    f"`{item}` = `{configvars[item]}`\n" for item in configvars
                )
                await var.client.send_message(
                    BOTLOG_CHATID, "#CONFIGVARS\n\n" "**Config Vars**:\n" f"{msg}"
                )
                await var.edit("**Berhasil Mengirim Ke BOTLOG_CHATID**")
                return True
            else:
                await var.edit("**Mohon Ubah Var** `BOTLOG` **Ke** `True`")
                return False
        elif variable in heroku_var:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID,
                    "**Logger : #SYSTEM**\n\n"
                    "**#SET #VAR_HEROKU #ADDED**\n\n"
                    f"`{variable}` **=** `{heroku_var[variable]}`\n",
                )
                await var.edit("**Berhasil Mengirim Ke BOTLOG_CHATID**")
                return True
            else:
                await var.edit("**Mohon Ubah Var** `BOTLOG` **Ke** `True`")
                return False
        else:
            await var.edit("`Informasi Tidak Ditemukan...`")
            return True
    elif exe == "del":
        await var.edit("`Menghapus Config Vars...`")
        variable = var.pattern_match.group(2)
        if variable == "":
            await var.edit("`Mohon Tentukan Config Vars Yang Mau Anda Hapus`")
            return False
        if variable in heroku_var:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID,
                    "**Logger : #SYSTEM**\n\n"
                    "**#SET #VAR_HEROKU #DELETED**\n\n"
                    f"`{variable}`",
                )
            await var.edit("**Config Vars Telah Dihapus**")
            del heroku_var[variable]
        else:
            await var.edit("**Tidak Dapat Menemukan Config Vars**")
            return True


@register(outgoing=True, pattern=r"^\.set var (\w*) ([\s\S]*)")
async def set_var(var):
    await var.edit("`Processing Config Vars..`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID,
                "**Logger : #SYSTEM**\n\n"
                "**#SET #VAR_HEROKU #ADDED**\n\n"
                f"`{variable}` = `{value}`",
            )
        await var.edit("`Sedang Proses, Mohon Tunggu sebentar..`")
    else:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID,
                "**Logger : #SYSTEM**\n\n"
                "**#SET #VAR_HEROKU #ADDED**\n\n"
                f"`{variable}` **=** `{value}`",
            )
        await var.edit("`Menambahkan Config Vars..`")
    heroku_var[variable] = value


"""
    Check account quota, remaining quota, used quota, used app quota
"""


@register(outgoing=True, pattern=r"^\.usage(?: |$)")
async def dyno_usage(dyno):
    """
    Get your account Dyno Usage
    """
    await dyno.edit("`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.117 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await dyno.client.send_message(
                    dyno.chat_id, f"`{r.reason}`", reply_to=dyno.id
                )
                await dyno.edit("**Gagal Mendapatkan Informasi Dyno**")
                return False
            result = await r.json()
            quota = result["account_quota"]
            quota_used = result["quota_used"]

            """ - User Quota Limit and Used - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - User App Used Quota - """
            Apps = result["apps"]
            for apps in Apps:
                if apps.get("app_uuid") == app.id:
                    AppQuotaUsed = apps.get("quota_used") / 60
                    AppPercentage = math.floor(apps.get("quota_used") * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await dyno.edit(
                "✥ **Informasi Dyno Heroku :**\n"
                "╔════════════════════╗\n"
                f" ✣ **Penggunaan Dyno** `{app.name}` :\n"
                f"     •  `{AppHours}`**Jam**  `{AppMinutes}`**Menit**  "
                f"**|**  [`{AppPercentage}`**%**]"
                "\n◖════════════════════◗\n"
                " ✣ **Sisa kuota dyno bulan ini** :\n"
                f"     •  `{hours}`**Jam**  `{minutes}`**Menit**  "
                f"**|**  [`{percentage}`**%**]"
                "\n╚════════════════════╝"
            )
            return True


@register(outgoing=True, pattern=r"^\.logs")
async def _(dyno):
    if app is None:
        return await dyno.edit(
            "**Wajib Mengisi Var** `HEROKU_APP_NAME` **dan** `HEROKU_API_KEY`"
        )
    await dyno.edit("**Sedang Mengambil Logs Heroku**")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await dyno.client.send_file(
        entity=dyno.chat_id, file="logs.txt", caption="**Ini Logs Heroku anda**"
    )
    await dyno.delete()
    return os.remove("logs.txt")


CMD_HELP.update(
    {
        "heroku": "**Plugin : **`heroku`\
        \n\n  •  **Syntax :** `.usage`\
        \n  •  **Function : **Check Kouta Dyno Heroku\
        \n\n  •  **Syntax :** `.set var <nama var> <value>`\
        \n  •  **Function : **Tambahkan Variabel Baru Atau Memperbarui Variabel\n Setelah Menyetel Variabel Man-Userbot Akan Di Restart.\
        \n\n  •  **Syntax :** `.get var or .get var <nama var>`\
        \n  •  **Function : **Dapatkan Variabel Yang Ada,Harap Gunakan Di Grup Private Anda! Ini Untuk Mengembalikan Informasi Heroku Pribadi Anda.\
        \n\n  •  **Syntax :** `.del var <nama var>`\
        \n  •  **Function : **Untuk Menghapus var heroku\
        \n\n  •  **Syntax :** `.usange`\
        \n  •  **Function : **Fake Check Kouta Dyno Heroku jadi 9989jam Untuk menipu temanmu wkwk\
    "
    }
)
