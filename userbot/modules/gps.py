# credits: mrconfused
from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"gps(?: |$)(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("`Berikan Tempat Yang Dicari...`")

    await event.edit("`Menemukan Lokasi Ini Di Server Map....`")

    geolocator = Nominatim(user_agent="Man")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await event.delete()
    else:
        await event.edit("`Maaf Saya Tidak Dapat Menemukannya`")


CMD_HELP.update(
    {
        "gps": f"**Plugin : **`gps`\
        \n\n  •  **Syntax :** `{cmd}gps` <nama lokasi>\
        \n  •  **Function : **Untuk Mendapatkan Lokasi Map.\
    "
    }
)
