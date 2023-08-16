#!/usr/bin/bash

# Ideally, run via sudo -E

echo "Stopping greenhouse service"
systemctl stop greenhouse

echo "Updating greenhouse code"
git pull origin

echo "Starting greenhouse service"
systemctl start greenhouse
systemctl status greenhouse


