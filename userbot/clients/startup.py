# Credits: @mrismanaziz || https://github.com/mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import telethon.utils

from userbot import (
    LOGS,
    MAN2,
    MAN3,
    MAN4,
    MAN5,
    STRING_2,
    STRING_3,
    STRING_4,
    STRING_5,
    STRING_SESSION,
    bot,
    call_py,
)


async def man_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def multiman():
    if STRING_SESSION:
        try:
            bot.start()
            call_py.start()
            bot.loop.run_until_complete(man_client(bot))
            user = bot.get_me()
            LOGS.info(f"STRING_1 detected! Starting as {user.first_name}")
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_1 Not Found")

    if STRING_2:
        try:
            MAN2.start()
            MAN2.loop.run_until_complete(man_client(MAN2))
            user = MAN2.get_me()
            LOGS.info(f"STRING_1 detected! Starting as {user.first_name}")
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_2 Not Found")

    if STRING_3:
        try:
            MAN3.start()
            MAN3.loop.run_until_complete(man_client(MAN3))
            user = MAN3.get_me()
            LOGS.info(f"STRING_3 detected! Starting as {user.first_name}")
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_3 Not Found")

    if STRING_4:
        try:
            MAN4.start()
            MAN4.loop.run_until_complete(man_client(MAN4))
            user = MAN4.get_me()
            LOGS.info(f"STRING_4 detected! Starting as {user.first_name}")
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_4 Not Found")

    if STRING_5:
        try:
            MAN5.start()
            MAN5.loop.run_until_complete(man_client(MAN5))
            user = MAN5.get_me()
            LOGS.info(f"STRING_5 detected! Starting as {user.first_name}")
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_5 Not Found")
