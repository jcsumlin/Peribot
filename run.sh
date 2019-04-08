#!/usr/bin/bash
#   /$$$$$$$                     /$$ /$$                   /$$
#  | $$__  $$                   |__/| $$                  | $$
#  | $$  \ $$ /$$$$$$   /$$$$$$  /$$| $$$$$$$   /$$$$$$  /$$$$$$
#  | $$$$$$$//$$__  $$ /$$__  $$| $$| $$__  $$ /$$__  $$|_  $$_/
#  | $$____/| $$$$$$$$| $$  \__/| $$| $$  \ $$| $$  \ $$  | $$
#  | $$     | $$_____/| $$      | $$| $$  | $$| $$  | $$  | $$ /$$
#  | $$     |  $$$$$$$| $$      | $$| $$$$$$$/|  $$$$$$/  |  $$$$/
#  |__/      \_______/|__/      |__/|_______/  \______/    \___/

FAILS=0

while true
do
  sleep 0.5
  python3 main.py # your program
  EXIT=$?
  ((FAILS++))

  if [[ $FAILS -gt 10 ]]
  then
    echo "[$(date)] failed to many times. aborting ..."
    exit 1
  fi

  echo "[$(date)] bot exited with code $EXIT. restarting ..."

done