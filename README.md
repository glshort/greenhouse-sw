# Setup
### Preamble
 1. Use the raspberry pi imager to flash a microsd for the pi, recommend 32GB and a Pi Zero 2W, 64-bit debian with no desktop
 2. Edit the settings before flashing:
    - Set the network name (I like `greenhouse1` and so on)
    - Configure wifi
    - Enable ssh access, either with credentials or ssh key
 4. Once done, ssh to your greenhouse pi using the name set above, i.e. `greenhouse1.local` and follow the steps below:
### Basics
 1.	sudo raspi-config, update, enable i2c
 2.	sudo apt-get update
 3.	sudo apt-get upgrade
 4.	sudo apt-get install unattended-upgrades
 5.	sudo dpkg-reconfigure --priority=low unattended-upgrades
 7.	sudo nano /etc/systemd/journald.conf
    - uncomment `#SystemMaxUse=`
    - set to 1G
    - save & exit
    - I don't actually know that this is required on account of log2ram below
    - May also be bad to have differing sizes between this and the ram disk set up below? FIXME
 9.	systemctl restart systemd-journald
 10.	sudo apt-get install python3-pip
### log2ram
 1. sudo apt install rsync
 2. wget https://github.com/azlux/log2ram/archive/master.tar.gz -O log2ram.tar.gz
 3. tar xf log2ram.tar.gz
 4. cd log2ram-master/
 5. sudo ./install.sh
 6. sudo reboot
    - you'll need to reconnect after this
 8. rm -rf log2ram-master log2ram.tar.gz
 9. sudo nano /etc/log2ram.conf
    - Set `SIZE=` to 40M
    - save & exit
 11. sudo reboot
     - reconnect again
### Greenhouse stuff itself
 1.	sudo apt-get install i2c-tools
### More to come
 - ~~log2ram~~
 - pigpiod or similar for software PWM without an active script
 - actuall SW setup for light control
 - filesystem to read-only once fully established
