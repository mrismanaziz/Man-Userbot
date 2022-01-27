# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting the weather of a city. """

import json
from datetime import datetime

from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz
from requests import get

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot import OPEN_WEATHER_MAP_APPID as OWM_API
from userbot import WEATHER_DEFCITY
from userbot.utils import edit_or_reply, man_cmd

DEFCITY = WEATHER_DEFCITY or None


async def get_tz(con):
    """Get time zone of the given country."""
    """ Credits: @aragon12 and @zakaryan2004. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@man_cmd(pattern="weather(?: |$)(.*)")
async def get_weather(weather):
    if not OWM_API:
        return await weather.edit(
            "**Get an API key from** https://openweathermap.org **first.**"
        )
    xx = await edit_or_reply(weather, "Processing...")
    APPID = OWM_API
    anonymous = False
    if not weather.pattern_match.group(1):
        CITY = DEFCITY
    elif weather.pattern_match.group(1).lower() == "anon":
        CITY = DEFCITY
        anonymous = True
    else:
        CITY = weather.pattern_match.group(1)
    if not CITY:
        return await xx.edit(
            "**Please specify a city or set one as default using the WEATHER_DEFCITY config variable.**"
        )
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                return await weather.edit("`Invalid country.`")
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}"
    request = get(url)
    result = json.loads(request.text)
    if request.status_code != 200:
        return await weather.edit("`Invalid country.`")
    cityname = result["name"]
    curtemp = result["main"]["temp"]
    humidity = result["main"]["humidity"]
    min_temp = result["main"]["temp_min"]
    max_temp = result["main"]["temp_max"]
    desc = result["weather"][0]
    desc = desc["main"]
    country = result["sys"]["country"]
    sunrise = result["sys"]["sunrise"]
    sunset = result["sys"]["sunset"]
    wind = result["wind"]["speed"]
    winddir = result["wind"]["deg"]
    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    div = 360 / len(dirs)
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(f):
        temp = str((f - 273.15) * 9 / 5 + 32).split(".")
        return temp[0]

    def celsius(c):
        temp = str(c - 273.15).split(".")
        return temp[0]

    def sun(unix):
        return datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")

    results = (
        f"**Temperature:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        + f"**Min. Temp.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        + f"**Max. Temp.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"**Humidity:** `{humidity}%`\n"
        + f"**Wind:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
        + f"**Sunrise:** `{sun(sunrise)}`\n"
        + f"**Sunset:** `{sun(sunset)}`\n\n"
        + f"**{desc}**\n"
        + f"`{time}`\n"
    )
    if not anonymous:
        results += f"`{cityname}, {fullc_n}`"

    await edit_or_reply(weather, results)


CMD_HELP.update(
    {
        "weather": f"**Plugin : **`weather`\
        \n\n  •  **Syntax :** `{cmd}weather` <city> or `.weather` <city>, <country name/code>\
        \n  •  **Function : **Untuk Mendapat informasi cuaca kota.\
        \n\n  •  **Syntax : **`{cmd}weather anon` \
        \n  •  **Function : **Untuk Mendapat informasi cuaca kota, dan menghilangkan detail lokasi di hasil. (Ini membutuhkan var WEATHER_DEFCITY untuk disetel)\
    "
    }
)
