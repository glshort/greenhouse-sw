#!/usr/bin/python

import math
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests
import pytz
# Need to decide if I want a virtualenv and pip it in or to find this via apt somewhere
# Hard-coding values in-line for now
# FIXME
#from timezonefinder import TimezoneFinder
from time import sleep
import pigpio

local_tz = 'America/Chicago'
# Test locations, using the first one by default
target_coords = {'lat': 41.549570, 'lng': -93.924374} # Van Meter, IA
target_coords2 = {'lat': -2.221543, 'lng': -54.930931} # Somewhere along the Amazon River
target_coords3 = {'lat': -39.173011, 'lng': 175.514709} # Gollum's Fishin' Hole

light_min = 50 # Light shuts off well above 0 dutycycle
light_max = 255

def get_tz(coords: dict[str, float])->str:
  assert coords.get("lat", None) is not None
  assert coords.get("lng", None) is not None
  tf = TimezoneFinder()
  return(tf.certain_timezone_at(lat=coords['lat'], lng=coords['lng']))

def get_faux_local_time(
    local_tz: str,
    coords: dict[str, float]
    ) -> datetime:

  assert coords.get("lat", None) is not None
  assert coords.get("lng", None) is not None

  tz = pytz.timezone(local_tz) # actual local time zone
  target_tz = 'America/Chicago' #get_tz(coords) # FIXME

  # Grab the local time and move it to the make-believe time zone without actually adjusting
  time = datetime.now(tz)
  time = time.replace(tzinfo=None)
  faux_tz = pytz.timezone(target_tz)
  time = faux_tz.localize(time)
  return(time)

def get_light_data(
    coords: dict[str, float],
    date: datetime | None = None,
) -> dict[str, str] | None:
    """Returns solar rise/zenith/set data from an API.

    Args:
        coords (dict[str, float]): REQUIRED. Latitude and Longitude coordinates of the location of
        solar movement. Required structure is {"lat": <float>, "long": <float>}

        date (datetime.datetime | None): OPTIONAL. The date of the solar data. If
        timezone-naive, this is assumed to be UTC

    Returns:
        dict[str, str]: the JSON solar data returned by the API
    """
    assert coords.get("lat", None) is not None
    assert coords.get("lng", None) is not None

    if date is None:
        date = datetime.now(timezone.utc)

    if date.tzinfo is not None:
        date = date.astimezone(timezone.utc)
    
    api_url = 'https://api.sunrise-sunset.org/json'
    ret = requests.get(api_url, params={
        'lat': coords['lat'],
        'lng': coords['lng'],
        'date': date.date(),
        'tzid': date.tzinfo
    })
    if not ret.status_code == 200:
        raise RuntimeError(f"The API request was unsucessful: {ret.status_code} {ret}")

    return ret.json().get("results")

def times_to_datetimes(
    light_data: dict[str, str], time: datetime
) -> tuple[datetime, datetime]:
    sunrise_datetime: datetime = datetime.strptime(
        f"{time.date().isoformat()} {light_data['sunrise']}", "%Y-%m-%d %I:%M:%S %p"
    )
    sunrise_datetime = sunrise_datetime.replace(tzinfo=ZoneInfo("UTC"))

    sunset_datetime: datetime = datetime.strptime(
        f"{time.date().isoformat()} {light_data['sunset']}", "%Y-%m-%d %I:%M:%S %p"
    )
    sunset_datetime = sunset_datetime.replace(tzinfo=ZoneInfo("UTC"))

    if sunset_datetime <= sunrise_datetime:
        sunset_datetime = sunset_datetime + timedelta(days=1)

    return sunrise_datetime, sunset_datetime

def get_light_curve_point(
    sunrise_datetime: datetime, sunset_datetime: datetime, time: datetime
) -> float:
    """
    """
    day_len_seconds = (sunset_datetime - sunrise_datetime).total_seconds()

    if time > sunrise_datetime and time < sunset_datetime:
        time_after_sunrise_seconds = (sunset_datetime - time).total_seconds()
        return math.sin(math.pi * time_after_sunrise_seconds / day_len_seconds)
    else:
        return 0.0


def main():
  pi = pigpio.pi()
  pi.set_mode(5, pigpio.OUTPUT)
  pi.set_PWM_frequency(5, 1000)
  pi.set_PWM_dutycycle(5, 0)

  time = get_faux_local_time(local_tz, target_coords)

  light = get_light_data(target_coords, time)
  if light is None:
    print("Something is wrong with the sunrise-sunset API response")
    return()

  sunrise_datetime, sunset_datetime = times_to_datetimes(light, time)
  light_level = get_light_curve_point(sunrise_datetime, sunset_datetime, time)
  dutycycle = int((light_max - light_min) * light_level + light_min)
  pi.set_PWM_dutycycle(5, dutycycle)


if __name__ == "__main__":
  main()
