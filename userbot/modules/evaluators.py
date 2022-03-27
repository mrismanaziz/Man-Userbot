# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for executing code and terminal commands from Telegram."""

import asyncio
import io
import sys
import traceback
from os import remove
from pprint import pprint

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.utils import man_cmd

p, pp = print, pprint


@man_cmd(pattern="eval(?:\s|$)([\s\S]*)")
async def _(event):
    expression = event.pattern_match.group(1)
    if not expression:
        return await event.edit("**Berikan Code untuk di eksekusi.**")
    if expression in ("userbot.session", "config.env"):
        return await event.edit("**Itu operasi yang berbahaya! Tidak diperbolehkan!**")
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return event.edit("**Apa yang harus saya jalankan?**")
    cmd = (
        cmd.replace("sendmessage", "send_message")
        .replace("sendfile", "send_file")
        .replace("editmessage", "edit_message")
    )
    xx = await event.edit("`Processing...`")
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    reply_to_id = event.message.id

    async def aexec(code, event):
        exec(
            "async def __aexec(e, client): "
            + "\n message = event = e"
            + "\n reply = await event.get_reply_message()"
            + "\n chat = (await event.get_chat()).id"
            + "".join(f"\n {line}" for line in code.split("\n")),
        )

        return await locals()["__aexec"](event, event.client)

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**•  Eval : **\n`{cmd}` \n\n**•  Result : **\n`{evaluation}` \n"

    if len(final_output) > 4096:
        man = final_output.replace("`", "").replace("**", "").replace("__", "")
        with io.BytesIO(str.encode(man)) as out_file:
            out_file.name = "eval.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                thumb="userbot/resources/logo.jpg",
                allow_cache=False,
                caption=f"`{cmd}`" if len(cmd) < 998 else None,
                reply_to=reply_to_id,
            )
            await xx.delete()
    else:
        await xx.edit(final_output)


@man_cmd(pattern="exec(?: |$|\n)([\s\S]*)")
async def run(event):
    code = event.pattern_match.group(1)
    if not code:
        return await event.edit("**Read** `.help exec` **for an example.**")
    if code in ("userbot.session", "config.env"):
        return await event.edit("`Itu operasi yang berbahaya! Tidak diperbolehkan!`")
    await event.edit("`Processing...`")
    if len(code.splitlines()) <= 5:
        codepre = code
    else:
        clines = code.splitlines()
        codepre = (
            clines[0] + "\n" + clines[1] + "\n" + clines[2] + "\n" + clines[3] + "..."
        )
    command = "".join(f"\n {l}" for l in code.split("\n.strip()"))
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-c",
        command.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    codepre.encode("unicode-escape").decode().replace("\\\\", "\\")
    stdout, _ = await process.communicate()
    if stdout and stdout != "":
        stdout = str(stdout.decode().strip())
        stdout.encode("unicode-escape").decode().replace("\\\\", "\\")
    else:
        stdout = "Success"
    if len(stdout) > 4096:
        with open("output.txt", "w+") as file:
            file.write(stdout)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            thumb="userbot/resources/logo.jpg",
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        return remove("output.txt")
    await event.edit(f"**Query:**\n`{codepre}`\n\n**Result:**\n`{stdout}`")


@man_cmd(pattern="term(?: |$|\n)([\s\S]*)")
async def terminal_runner(event):
    command = event.pattern_match.group(1)
    if not command:
        return await event.edit("`Give a command or use .help term for an example.`")
    if command in ("userbot.session", "config.env"):
        return await event.edit("`Itu operasi yang berbahaya! Tidak diperbolehkan!`")
    await event.edit("`Processing...`")
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    command.encode("unicode-escape").decode().replace("\\\\", "\\")
    stdout, _ = await process.communicate()
    if stdout and stdout != "":
        result = str(stdout.decode().strip())
        result.encode("unicode-escape").decode().replace("\\\\", "\\")
    else:
        result = "Success"
    if len(result) > 4096:
        with open("output.txt", "w+") as output:
            output.write(result)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            thumb="userbot/resources/logo.jpg",
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        return remove("output.txt")

    await event.edit(f"**Command:**\n`{command}`\n\n**Result:**\n`{result}`")


@man_cmd(pattern="json$")
async def _(event):
    if event.fwd_from:
        return
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    if len(the_real_message) > 4096:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                thumb="userbot/resources/logo.jpg",
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await event.edit("`{}`".format(the_real_message))


CMD_HELP.update(
    {
        "json": f"**Plugin : **`json`\
        \n\n  •  **Syntax :** `{cmd}json` <reply ke pesan>\
        \n  •  **Function : **Untuk mendapatkan detail pesan dalam format json.\
    "
    }
)


CMD_HELP.update(
    {
        "eval": f"**Plugin : **`eval`\
        \n\n  •  **Syntax :** `{cmd}eval` <cmd>\
        \n  •  **Function : **Evaluasi ekspresi Python dalam argumen skrip yang sedang berjalan\
    "
    }
)


CMD_HELP.update(
    {
        "exec": f"**Plugin : **`exec`\
        \n\n  •  **Syntax :** `{cmd}exec print('hello')`\
        \n  •  **Function : **Jalankan skrip python kecil di subproses.\
    "
    }
)


CMD_HELP.update(
    {
        "term": f"**Plugin : **`term`\
        \n\n  •  **Syntax :** `{cmd}term` <cmd>\
        \n  •  **Function : **Jalankan perintah dan skrip bash di server Anda.\
    "
    }
)
