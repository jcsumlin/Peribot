#!/usr/bin/env bash
#   /$$$$$$$                     /$$ /$$                   /$$
#  | $$__  $$                   |__/| $$                  | $$
#  | $$  \ $$ /$$$$$$   /$$$$$$  /$$| $$$$$$$   /$$$$$$  /$$$$$$
#  | $$$$$$$//$$__  $$ /$$__  $$| $$| $$__  $$ /$$__  $$|_  $$_/
#  | $$____/| $$$$$$$$| $$  \__/| $$| $$  \ $$| $$  \ $$  | $$
#  | $$     | $$_____/| $$      | $$| $$  | $$| $$  | $$  | $$ /$$
#  | $$     |  $$$$$$$| $$      | $$| $$$$$$$/|  $$$$$$/  |  $$$$/
#  |__/      \_______/|__/      |__/|_______/  \______/    \___/

docker build -t peribot .
&& docker run
--env PREFIX=!
--env REDDIT_CLIENT_ID=
--env TOKEN=
--env REDDIT_CLIENT_SECRET=
--env REDDIT_PASSWORD=
--env REDDIT_USERNAME=
--name peribot
peribot