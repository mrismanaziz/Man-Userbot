from userbot.modules.sql_helper.global_collectionjson import get_collection


def blacklist_chats_list():
    try:
        blacklistchats = get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    blacklist = blacklistchats.keys()
    return [int(chat) for chat in blacklist]
