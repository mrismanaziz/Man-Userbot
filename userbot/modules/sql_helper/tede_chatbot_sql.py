import threading

from sqlalchemy import Column, String
from userbot.modules.sql_helper import BASE, SESSION


class TedeChatBot(BASE):
    __tablename__ = "tede_chatbot"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


TedeChatBot.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def is_tede(chat_id):
    try:
        chat = SESSION.query(TedeChatBot).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_tede(chat_id):
    with INSERTION_LOCK:
        tedechat = SESSION.query(TedeChatBot).get(str(chat_id))
        if not tedechat:
            tedechat = TedeChatBot(str(chat_id))
        SESSION.add(tedechat)
        SESSION.commit()


def rem_tede(chat_id):
    with INSERTION_LOCK:
        tedechat = SESSION.query(TedeChatBot).get(str(chat_id))
        if tedechat:
            SESSION.delete(tedechat)
        SESSION.commit()
