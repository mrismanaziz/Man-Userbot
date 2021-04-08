# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

import io
import os
import os.path
import time
from os.path import exists, isdir

from userbot.events import register
from userbot.utils import humanbytes

MAX_MESSAGE_SIZE_LIMIT = 4095


@register(outgoing=True, pattern=r"^\.ls ?(.*)")
async def lst(event):
    if event.fwd_from:
        return
    cat = event.pattern_match.group(1)
    path = cat if cat else os.getcwd()
    if not exists(path):
        await event.edit(
            f"**There is no such directory or file with the name `{cat}` check again!**"
        )
        return
    if isdir(path):
        if cat:
            msg = "**Folders and Files in `{}`** :\n\n".format(path)
        else:
            msg = "**Folders and Files in Current Directory** :\n\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            catpath = path + "/" + contents
            if not isdir(catpath):
                size = os.stat(catpath).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵 " + f"`{contents}`\n"
                if contents.endswith((".opus")):
                    files += "🎙 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += "🎞 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")
                ):
                    files += "🗜 " + f"`{contents}`\n"
                elif contents.endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")
                ):
                    files += "🖼 " + f"`{contents}`\n"
                elif contents.endswith((".exe", ".deb")):
                    files += "⚙️ " + f"`{contents}`\n"
                elif contents.endswith((".iso", ".img")):
                    files += "💿 " + f"`{contents}`\n"
                elif contents.endswith((".apk", ".xapk")):
                    files += "📱 " + f"`{contents}`\n"
                elif contents.endswith((".py")):
                    files += "🐍 " + f"`{contents}`\n"
                else:
                    files += "📄 " + f"`{contents}`\n"
            else:
                folders += f"📁 `{contents}`\n"
        msg = msg + folders + files if files or folders else msg + "__empty path__"
    else:
        size = os.stat(path).st_size
        msg = "**The details of given file** :\n\n"
        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵 "
        if path.endswith((".opus")):
            mode = "🎙 "
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞 "
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
            mode = "🗜 "
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
            mode = "🖼 "
        elif path.endswith((".exe", ".deb")):
            mode = "⚙️ "
        elif path.endswith((".iso", ".img")):
            mode = "💿 "
        elif path.endswith((".apk", ".xapk")):
            mode = "📱 "
        elif path.endswith((".py")):
            mode = "🐍 "
        else:
            mode = "📄 "
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location :** `{path}`\n"
        msg += f"**Icon :** `{mode}`\n"
        msg += f"**Size :** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"

    if len(msg) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await event.delete()
    else:
        await event.edit(msg)
