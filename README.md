# Setup
### Preamble
 1. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash a microsd for the pi, recommended:
    - [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
    - 64-bit Raspberry-Pi OS Lite (no desktop)
    - 32GB card
 3. Edit the settings before flashing:
    - Set the network name (I like `greenhouse1` and so on)
    - Configure wifi
    - Enable ssh access, either with credentials or ssh key
### Installation
 1. ssh to your greenhouse using the name set above, i.e. `greenhouse1.local`
 2. `wget -qO - 'https://github.com/glshort/greenhouse-sw/blob/main/install.sh?raw=true' | sudo bash`
 5. Godspeed
### More to come
 - Thanks to Palmieri for figuring out the location-based light level mimickry
 - A python/Beehive/Toga/Briefcase phone app to control it?! Thanks to Buechler for that tip
