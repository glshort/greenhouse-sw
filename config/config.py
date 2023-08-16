import os
import json
import RPi.GPIO as GPIO

def get_gpio_cfg():
    with open('./config/gpio.json', 'r') as f:
        gpio_cfg = json.load(f)

    GPIO.setmode(GPIO.BCM)
    for v in gpio_cfg.values():
        GPIO.setup(v['GPIO'], GPIO.OUT if v['type'] == 'out' else GPIO.IN)

    return gpio_cfg
