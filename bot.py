import json
import logging
from datetime import datetime as dt, timedelta

import interactions
from interactions.ext.files import command_send

import processing
from scraping import HandSpeak, LifePrint
import settings
from connections import query_database

client = interactions.Client(settings.token)

@client.event
async def on_ready():
    print('We have logged in.')

@client.command(
    name="wotd"
)
async def wotd(ctx):
    hs = HandSpeak()
    message = hs.wordOfTheDay(ctx.guild.id)

    file = interactions.File("wotd.mp4")
    await command_send(ctx, content = message, files = file)


client.start()