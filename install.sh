#!/bin/bash

# Basics
apt update
apt autoremove -y
# FIXME: need initramfs.conf auto over-write during following command
apt -o Dpkg::Options::="--force-overwrite" upgrade -y
apt install -y unattended-upgrades python3-pip
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure --priority=low unattended-upgrades
sed -i -e 's/#\?SystemMaxUse=\w*/SystemMaxUse=45M/g' /etc/systemd/journald.conf
systemctl restart systemd-journald
raspi-config nonint do_i2c 0

# log2ram: https://github.com/azlux/log2ram
# This is not secure, I believe there's a better way but FIXME
echo "deb http://packages.azlux.fr/debian/ bullseye main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
apt update
apt install -y rsync log2ram
sed -i -e 's/#\?SIZE=\w*/SIZE=50M/g' /etc/log2ram.conf

# pigpiod
apt install -y pigpio python3-pigpio
pigpiod

# fin
echo '==============================================='
echo "System reboot needed, please 'sudo reboot' now!"
echo '==============================================='

