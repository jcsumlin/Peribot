# Peribot - Modular Discord Bot

Highly customizable discord bot made with love in the US

 ![Python Versions](https://img.shields.io/badge/python-3.6-blue?style=for-the-badge)
 ![Discord.py Version](https://img.shields.io/badge/discord.py-1.2.5-blue?style=for-the-badge)
 ![Issues](https://img.shields.io/github/issues/jcsumlin/Peribot?style=for-the-badge)
 ![Patreon](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.herokuapp.com%2Fbotboi&style=for-the-badge)

## Getting Started
### [Docs](https://github.com/jcsumlin/Peribot)
There are several branches for various environments (Heroku, Docker, Master (python console)). Pick the branch that you want to pull down and clone it to your machine.
I highly recommend that you use the docker environment since it is the most up to date and easiest to setup.
### Starting your own instance of Peribot

What things you need to install the software and how to install them. As long as you have python 3.6 installed you can install the remaining requirements through the requirements.txt file

```bash
pip install -r requirements.txt
```

Copy the auth.ini.example to a new file named auth.ini and fill in the bot token and any other keys you may want to use.

If you ware using this bot on linux you'll want to install FFMpeg `sudo apt install ffmpeg` for the music cog to work. Windows users will not have to do anything. The Exe for FFMpeg is included in the repository already.

Then all you need to do is run `sh start.sh`


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration Bobby Bot


## ToDo:
 - [ ] Convert Giveaway cog to use database
