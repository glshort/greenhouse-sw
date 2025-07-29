#!/bin/bash

# Basics
apt -qy update
apt -qy autoremove
apt -qy -o Dpkg::Options::="--force-confnew" upgrade
apt -qy install unattended-upgrades python3-pip
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure --priority=low unattended-upgrades
sed -i -e 's/#\?SystemMaxUse=\w*/SystemMaxUse=45M/g' /etc/systemd/journald.conf
systemctl restart systemd-journald
raspi-config nonint do_i2c 0

# log2ram: https://github.com/azlux/log2ram
# This is not secure, I believe there's a better way but FIXME
echo "deb http://packages.azlux.fr/debian/ bullseye main" | sudo tee /etc/apt/sources.list.d/azlux.list
wget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -
apt update
apt install -qy rsync log2ram
sed -i -e 's/#\?SIZE=\w*/SIZE=50M/g' /etc/log2ram.conf

# pigpiod
apt install -qy pigpio python3-pigpio
systemctl enable pigpiod
systemctl start pigpiod

# greenhouse stuff
apt install -qy python3-tz
wget -qO update_lights.py 'https://github.com/glshort/greenhouse-sw/blob/main/update_lights.py?raw=true'
chmod 755 update_lights.py
chown root:root update_lights.py
mv update_lights.py /usr/local/sbin/update_lights
wget -qO greenhouse.cron 'https://github.com/glshort/greenhouse-sw/blob/main/greenhouse.cron?raw=true'
chmod 644 greenhouse.cron
chown root:root greenhouse.cron
mv greenhouse.cron /etc/cron.d/greenhouse

# fin
reboot

