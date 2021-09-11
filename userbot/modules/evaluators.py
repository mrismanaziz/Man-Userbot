# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for executing code and terminal commands from Telegram."""

import asyncio
import sys
from io import StringIO
from os import remove
from traceback import format_exc

from userbot import CMD_HELP, bot
from userbot.events import register

MAX_MESSAGE_SIZE_LIMIT = 4095


@register(outgoing=True, pattern=r"^\.eval(?: |$|\n)([\s\S]*)")
async def evaluate(event):
    """For .eval command, evaluates the given Python expression."""
    expression = event.pattern_match.group(1)
    if not expression:
        return await event.edit("`Give an expression to evaluate.`")

    if expression in ("userbot.session", "config.env"):
        return await event.edit("`Itu operasi yang berbahaya! Tidak diperbolehkan!`")

    await event.edit("`Processing...`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc, returned = None, None, None, None

    async def aexec(code, event):
        head = "async def __aexec(event):\n "
        code = "".join(f"\n {line}" for line in code.split("\n"))
        exec(head + code)  # pylint: disable=exec-used
        return await locals()["__aexec"](event)

    try:
        returned = await aexec(expression, event)
    except Exception:  # pylint: disable=broad-except
        exc = format_exc()

    stdout = redirected_output.getvalue().strip()
    stderr = redirected_error.getvalue().strip()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    expression.encode("unicode-escape").decode().replace("\\\\", "\\")

    evaluation = str(exc or stderr or stdout or returned)
    if evaluation and evaluation != "":
        evaluation = evaluation.encode("unicode-escape").decode().replace("\\\\", "\\")
    else:
        evaluation = "Success"

    if len(str(evaluation)) >= 4096:
        with open("output.txt", "w+") as file:
            file.write(evaluation)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        return remove("output.txt")
    await event.edit(f"**Query:**\n`{expression}`\n\n**Result:**\n`{evaluation}`")


@register(outgoing=True, pattern=r"^\.exec(?: |$|\n)([\s\S]*)")
async def run(event):
    """For .exec command, which executes the dynamically created program"""
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
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        return remove("output.txt")
    await event.edit(f"**Query:**\n`{codepre}`\n\n**Result:**\n`{stdout}`")


@register(outgoing=True, pattern=r"^\.term(?: |$|\n)([\s\S]*)")
async def terminal_runner(event):
    """For .term command, runs bash commands and scripts on your server."""
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
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        return remove("output.txt")

    await event.edit(f"**Command:**\n`{command}`\n\n**Result:**\n`{result}`")


@register(outgoing=True, pattern=r"^\.json$")
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
    if len(the_real_message) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await event.edit("`{}`".format(the_real_message))


CMD_HELP.update(
    {
        "json": "**Plugin : **`json`\
        \n\n  •  **Syntax :** `.json` <reply ke pesan>\
        \n  •  **Function : **Untuk mendapatkan detail pesan dalam format json.\
    "
    }
)


CMD_HELP.update(
    {
        "eval": "**Plugin : **`eval`\
        \n\n  •  **Syntax :** `.eval` <cmd>\
        \n  •  **Function : **Evaluasi ekspresi Python dalam argumen skrip yang sedang berjalan\
    "
    }
)


CMD_HELP.update(
    {
        "exec": "**Plugin : **`exec`\
        \n\n  •  **Syntax :** `.exec print('hello')`\
        \n  •  **Function : **Jalankan skrip python kecil di subproses.\
    "
    }
)


CMD_HELP.update(
    {
        "term": "**Plugin : **`term`\
        \n\n  •  **Syntax :** `.term` <cmd>\
        \n  •  **Function : **Jalankan perintah dan skrip bash di server Anda.\
    "
    }
)
