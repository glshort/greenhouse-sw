#!/usr/bin/bash

# Ideally, run via sudo

echo "Stopping greenhouse service"
systemctl stop greenhouse

echo "Updating greenhouse code"
git pull origin

echo "Starting greenhouse service"
systemctl start greenhouse

echo "All done"


