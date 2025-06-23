#!/usr/bin/env bash
# Install Chrome
apt-get update && apt-get install -y wget gnupg
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
     > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable
# Start Flask
gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
