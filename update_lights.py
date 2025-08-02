#!/usr/bin/python

import json
import warnings
from datetime import datetime, timezone
import pytz
from timezonefinder import TimezoneFinder
import pigpio
import pysolar.solar as pysolar


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
  target_tz = get_tz(coords)

  time = datetime.now(local_tz) # grab the actual local time
  time = time.replace(tzinfo=None) # naive-ify it
  time = pytz.timezone(target_tz).localize(time) # fake it to the target time zone
  return(time)


def get_flux(time: datetime, coords: dict[str, float]) -> float:
  assert coords.get("lat", None) is not None
  assert coords.get("lng", None) is not None

  elevation = pysolar.get_altitude(
    coords['lat'],
    coords['lng'],
    time)

  azimuth = pysolar.get_azimuth(
    coords['lat'],
    coords['lng'],
    time)

  if elevation > 0:
    flux = pysolar.radiation.get_radiation_direct(time, elevation)
  else:
    flux = 0

  return(flux, elevation, azimuth)


def flux_to_ppfd(flux):
  return flux * 0.45


def ppfd_to_duty_cycle(
    ppfd: float,
    ppfd_min: float,
    ppfd_max: float,
    duty_min: int,
    duty_max: int) -> int:
  if(ppfd <= 0):
    return(0)
  if(ppfd > 0 and ppfd < ppfd_min):
    return(duty_min)
  if(ppfd > ppfd_max):
    return(ppfd_max)

  return(int(((ppfd - ppfd_min) / (ppfd_max - ppfd_min) * (duty_max - duty_min) + duty_min))


def flux_to_dutycycle(
    flux: float,
    flux_min: float,
    flux_max: float,
    duty_min: int,
    duty_max: int
    ) -> int:
  if(flux <= 0):
    return(0)
  if(flux > 0 and flux < flux_min):
    return(duty_min)
  if(flux > flux_max):
    return(duty_max)

  return(int(((flux - flux_min) / (flux_max - flux_min)) * (duty_max - duty_min) + duty_min))


def main():
  warnings.filterwarnings("ignore", category=UserWarning)

  with open('/usr/local/etc/greenhouse/config.json', 'r') as f:
    config = json.load(f)

  time = get_faux_local_time(config['local_tz'], config['target_location'])
  flux, elevation, azimuth = get_flux(time, config['target_location'])
  ppfd = flux_to_ppfd(flux)

  pi = pigpio.pi()

  for light in config['lights']:
    pi.set_mode(light['pin'], pigpio.OUTPUT)
    pi.set_PWM_frequency(light['pin'], light['frequency'])
    if(not light['active']):
      #print(f'Setting {light["name"]} to 0/{light["duty_max"]} (inactive)')
      pi.set_PWM_dutycycle(light['pin'], 0)
    else:
      duty = ppfd_to_dutycycle(
        flux,
        light['ppfd_min'],
        light['ppfd_max'],
        light['duty_min'],
        light['duty_max']
        )
      #print(f'Setting {light["name"]} to {duty}/{light["duty_max"]}')
      pi.set_PWM_dutycycle(light['pin'], duty)


if __name__ == "__main__":
  main()
