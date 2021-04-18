import re

import requests
from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate


def paste_text(text):
    asciich = ["**", "`", "__"]
    for i in asciich:
        text = re.sub(rf"\{i}", "", text)
    try:
        nekokey = (
            requests.post(
                "https://nekobin.com/api/documents",
                json={
                    "content": text}) .json() .get("result") .get("key"))
        link = f"https://nekobin.com/{nekokey}"
    except Exception:
        url = "https://del.dog/documents"
        r = requests.post(url, data=text).json()
        link = f"https://del.dog/{r['key']}"
        if r["isUrl"]:
            link = f"https://del.dog/v/{r['key']}"
    return link


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


def htmlmentionuser(name, userid):
    return f"<a href='tg://user?id={userid}'>{name}</a>"


# kanged from uniborg @spechide
# https://github.com/SpEcHiDe/UniBorg/blob/d8b852ee9c29315a53fb27055e54df90d0197f0b/uniborg/utils.py#L250


def reformattext(text):
    return text.replace(
        "~",
        "").replace(
        "_",
        "").replace(
            "*",
            "").replace(
                "`",
        "")


def replacetext(text):
    return (
        text.replace(
            '"',
            "",
        )
        .replace(
            "\\r",
            "",
        )
        .replace(
            "\\n",
            "",
        )
        .replace(
            "\\",
            "",
        )
    )


def parse_pre(text):
    text = text.strip()
    return (
        text, [
            MessageEntityPre(
                offset=0, length=len(
                    add_surrogate(text)), language="")], )
