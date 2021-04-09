"""
This module updates the userbot based on upstream revision
"""

import asyncio
import sys
from os import environ, execle, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_BRANCH,
    UPSTREAM_REPO_URL,
)
from userbot.events import register


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        )
    return ch_log


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`[HEROKU]: Harap Siapkan Variabel` **HEROKU_APP_NAME** `"
                " untuk dapat deploy perubahan terbaru dari Userbot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n`Kredensial Heroku tidak valid untuk deploy Man-Userbot dyno.`"
            )
            return repo.__del__()
        await event.edit("`[HEROKU]: Update Deploy Man-Userbot Sedang Dalam Proses...`")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await event.edit(f"{txt}\n`Terjadi Kesalahan Di Log:\n{error}`")
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await event.edit(
                "`Build Gagal!" "Dibatalkan atau ada beberapa kesalahan...`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        else:
            await event.edit(
                "`Man-Userbot Berhasil Di Deploy! Userbot bisa di gunakan kembali.`"
            )
            await asyncio.sleep(15)
            await event.delete()

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#BOT \n" "`Man-Userbot Berhasil Di Update`"
            )

    else:
        await event.edit("`[HEROKU]: Harap Siapkan Variabel` **HEROKU_API_KEY** `.`")
        await asyncio.sleep(10)
        await event.delete()
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await event.edit("**✥ Man-Userbot** `Berhasil Di Update!`")
    await asyncio.sleep(1)
    await event.edit("**✥ Man-Userbot** `Sedang di Restart....`")
    await asyncio.sleep(1)
    await event.edit("`Tunggu Beberapa Detik `")
    await asyncio.sleep(10)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#BOT \n" "**Man-Userbot Sedang Di Perbarui**"
        )
        await asyncio.sleep(100)
        await event.delete()

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern=r"^.update(?: |$)(now|deploy)?")
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    await event.edit("`Mengecek Pembaruan, Silakan Menunggu....`")
    conf = event.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "`Pembaruan Tidak Dapat Di Lanjutkan Karna "
        txt += "Beberapa Masalah Terjadi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`Directory {error} Tidak Dapat Di Temukan`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Gagal Awal! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Sayangnya, Directory {error} Tampaknya Bukan Dari Repo."
                "\nTapi Kita Bisa Memperbarui Paksa Userbot Menggunakan .update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if changelog == "" and force_update is False:
        await event.edit(f"\n**✥ Man-Userbot Sudah Versi Terbaru**\n")
        await asyncio.sleep(15)
        await event.delete()
        return repo.__del__()

    if conf is None and force_update is False:
        changelog_str = f"**✥ Pembaruan Untuk Man-Userbot [{ac_br}] :\n\n✥ Pembaruan:**\n`{changelog}`"
        if len(changelog_str) > 4096:
            await event.edit("`Changelog Terlalu Besar, Buka File Untuk Melihatnya.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await event.client.send_file(
                event.chat_id,
                "output.txt",
                reply_to=event.id,
            )
            remove("output.txt")
        else:
            await event.edit(changelog_str)
        return await event.respond(
            "✥ **Perintah Untuk Update Man-Userbot**\n ›`.update now`\n ›`.update deploy`\n\n__Untuk Meng Update Fitur Terbaru Dari Man-Userbot.__"
        )

    if force_update:
        await event.edit(
            "`Sinkronisasi Paksa Ke Kode Userbot Stabil Terbaru, Harap Tunggu .....`"
        )
    else:
        await event.edit("`✣ Proses Update Man-Userbot, Loading....1%`")
        await event.edit("`✣ Proses Update Man-Userbot, Loading....12%`")
        await event.edit("`✣ Proses Update Man-Userbot, Loading....25%`")
        await event.edit("`✣ Proses Update Man-Userbot, Loading....46%`")
        await event.edit("`✣ Proses Update Man-Userbot, Loading....76%`")
        await event.edit("`✣ Proses Update Man-Userbot, Updating...92%`")
        await event.edit("`✣ Proses Update Man-Userbot, Tunggu Sebentar....100%`")
    if conf == "now":
        await update(event, repo, ups_rem, ac_br, txt)
        await asyncio.sleep(10)
        await event.delete()
    elif conf == "deploy":
        await deploy(event, repo, ups_rem, ac_br, txt)
        await asyncio.sleep(10)
        await event.delete()
    return


CMD_HELP.update(
    {
        "update": "**Plugin : **`update`\
        \n\n  •  **Syntax :** `.update`\
        \n  •  **Function : **Untuk Melihat Pembaruan Terbaru Man-Userbot.\
        \n\n  •  **Syntax :** `.update now`\
        \n  •  **Function : **Memperbarui Man-Userbot.\
        \n\n  •  **Syntax :** `.update deploy`\
        \n  •  **Function : **Memperbarui Man-Userbot Dengan Cara Deploy Ulang.\
    "
    }
)
