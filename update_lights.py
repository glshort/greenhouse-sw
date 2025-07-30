#!/usr/bin/python

from datetime import datetime, timedelta, timezone
import pytz
# Need to decide if I want a virtualenv and pip it in or to find this via apt somewhere
# Hard-coding values in-line for now
# FIXME
#from timezonefinder import TimezoneFinder
import pigpio
import pysolar.solar as pysolar

local_tz = 'America/Chicago'
# Test locations, using the first one by default
target_coords = {'lat': 41.549570, 'lng': -93.924374} # Van Meter, IA
target_coords2 = {'lat': -2.221543, 'lng': -54.930931} # Somewhere along the Amazon River
target_coords3 = {'lat': -39.173011, 'lng': 175.514709} # Gollum's Fishin' Hole

# These should all be moved to a config and calibrated
light_min = 60 # Light shuts off well above 0 dutycycle
light_max = 255
flux_min = 200 # Min light output before shutdown
flux_max = 1000 # Max light output

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

  local_tz = pytz.timezone(local_tz) # local time zone
  target_tz = 'America/Chicago' #get_tz(coords) # FIXME

  time = datetime.now(local_tz) # grab the actual local time
  time = time.replace(tzinfo=None) # naive-ify it
  time = pytz.timezone(target_tz).localize(time) # fake it to the target time zone
  return(time)


def get_flux(time: datetime, coords: dict[str, float]) -> float:
  assert coords.get("lat", None) is not None
  assert coords.get("lng", None) is not None

  elevation = pysolar.get_altitude(
    target_coords['lat'],
    target_coords['lng'],
    time)

  azimuth = pysolar.get_azimuth(
    target_coords['lat'],
    target_coords['lng'],
    time)

  if elevation > 0:
    flux = pysolar.radiation.get_radiation_direct(time, elevation)
  else:
    flux = 0

  return(flux, elevation, azimuth)


def flux_to_dutycycle(flux: float) -> int:
  min_duty = 60
  max_duty = 255
  min_flux = 200
  max_flux = 1000

  if(flux < min_flux):
    return(0)
  if(flux > max_flux):
    return(max_flux)

  return(int(((flux - min_flux) / (max_flux - min_flux)) * (max_duty - min_duty) + min_duty))


def main():
  pi = pigpio.pi()
  pi.set_mode(5, pigpio.OUTPUT)
  pi.set_PWM_frequency(5, 1000)

  time = get_faux_local_time(local_tz, target_coords)
  flux, elevation, azimuth = get_flux(time, target_coords)
  duty = flux_to_dutycycle(flux)

  pi.set_PWM_dutycycle(5, duty)


if __name__ == "__main__":
  main()
