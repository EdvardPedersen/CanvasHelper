Discord bot and library for interacting with Canvas

The bot supports subscribing to multiple courses in multiple channels.

# Dependencies

* canvasapi
* discord.py
* html2text
* ics

# How to use

Make a file `discord-token` with the access token for your discord bot.
Make a file `canvas-token` with the access token for Canvas.

Configure the courses and channels in `config.py`

Run bot.py

## To create attendance lists

Additional dependencies:

* openpyxl

Run create_attendance_list.py
