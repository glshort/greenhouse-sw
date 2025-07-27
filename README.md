## Setup
 1.	sudo raspi-config, update, enable i2c
 2.	sudo apt-get update
 3.	sudo apt-get upgrade
 4.	sudo apt-get install unattended-upgrades
 5.	sudo dpkg-reconfigure --priority=low unattended-upgrades
 6.	sudo apt-get install i2c-tools
 7.	sudo vim.tiny /etc/systemd/journald.conf, uncomment #SystemMaxUse=, set to 1G
 8.	systemctl restart systemd-journald
 9.	sudo apt-get install python3-pip
 10.	More to come:
 11.	(log2ram)
 12.	(actually SW setup for light control)
 13.	(filesystem to read-only once fully established)
