# Credits: @mrconfused
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import inspect
import re
from pathlib import Path

from telethon import events

from userbot import (
    BL_CHAT,
    CMD_HANDLER,
    CMD_LIST,
    LOAD_PLUG,
    MAN2,
    MAN3,
    MAN4,
    MAN5,
    SUDO_HANDLER,
    SUDO_USERS,
    bot,
    tgbot,
)


def man_cmd(
    pattern: str = None,
    allow_sudo: bool = True,
    disable_edited: bool = False,
    forword=False,
    command: str = None,
    **args,
):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    if "disable_edited" in args:
        del args["disable_edited"]

    args["blacklist_chats"] = True
    black_list_chats = list(BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    if pattern is not None:
        global man_reg
        global sudo_reg
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            man_reg = sudo_reg = re.compile(pattern)
        else:
            man_ = "\\" + CMD_HANDLER
            sudo_ = "\\" + SUDO_HANDLER
            man_reg = re.compile(man_ + pattern)
            sudo_reg = re.compile(sudo_ + pattern)
            if command is not None:
                cmd1 = man_ + command
                cmd2 = sudo_ + command
            else:
                cmd1 = (
                    (man_ + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
                cmd2 = (
                    (sudo_ + pattern)
                    .replace("$", "")
                    .replace("\\", "")
                    .replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd1)
            except BaseException:
                CMD_LIST.update({file_test: [cmd1]})

    def decorator(func):
        if bot:
            if not disable_edited:
                bot.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
                )
            bot.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
            )
        if bot:
            if allow_sudo:
                if not disable_edited:
                    bot.add_event_handler(
                        func,
                        events.MessageEdited(
                            **args, from_users=list(SUDO_USERS), pattern=sudo_reg
                        ),
                    )
                bot.add_event_handler(
                    func,
                    events.NewMessage(
                        **args, from_users=list(SUDO_USERS), pattern=sudo_reg
                    ),
                )
        if MAN2:
            if not disable_edited:
                MAN2.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
                )
            MAN2.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
            )
        if MAN3:
            if not disable_edited:
                MAN3.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
                )
            MAN3.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
            )
        if MAN4:
            if not disable_edited:
                MAN4.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
                )
            MAN4.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
            )
        if MAN5:
            if not disable_edited:
                MAN5.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=man_reg)
                )
            MAN5.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=man_reg)
            )
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def man_handler(
    **args,
):
    def decorator(func):
        if bot:
            bot.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if MAN2:
            MAN2.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if MAN3:
            MAN3.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if MAN4:
            MAN4.add_event_handler(func, events.NewMessage(**args, incoming=True))
        if MAN5:
            MAN5.add_event_handler(func, events.NewMessage(**args, incoming=True))
        return func

    return decorator


def asst_cmd(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/!]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        if tgbot:
            tgbot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def chataction(**args):
    def decorator(func):
        if bot:
            bot.add_event_handler(func, events.ChatAction(**args))
        if MAN2:
            MAN2.add_event_handler(func, events.ChatAction(**args))
        if MAN3:
            MAN3.add_event_handler(func, events.ChatAction(**args))
        if MAN4:
            MAN4.add_event_handler(func, events.ChatAction(**args))
        if MAN5:
            MAN5.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def callback(**args):
    def decorator(func):
        if tgbot:
            tgbot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
