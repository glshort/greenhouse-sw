# Setup
### Preamble
 1. Use the raspberry pi imager to flash a microsd for the pi, recommended:
    - Pi Zero 2 W
    - 64-bit Raspberry-Pi OS Lite (no desktop)
    - 32GB card
 3. Edit the settings before flashing:
    - Set the network name (I like `greenhouse1` and so on)
    - Configure wifi
    - Enable ssh access, either with credentials or ssh key
### Installation
 1. ssh to your greenhouse using the name set above, i.e. `greenhouse1.local`
 1. Grab `install.sh` from this repo, dump that into a same-named file on the pi
 2. `chmod a+x install.sh`
 3. `sudo ./install.sh`
 4. It should be fully automatic but there is at least one prompt that might appear that I can't get rid of yet
 5. Godspeed
### More to come
 - actual SW setup for light control
   - Thanks to Palmieri for figuring out the location-based light level mimickry
 - A python/Beehive/Toga/Briefcase phone app to control it?! Thanks to Buechler for that tip
