import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from methods import get_message

SUCCESS_MESSAGE = "success!"

load_dotenv()
CHANNEL_ID=os.getenv('CHANNEL_ID')
Intents = discord.Intents.all()
Intents.members = True
client = discord.Client(intents=Intents)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    alert_push.start()


@tasks.loop(seconds=60)
async def alert_push():
    message = get_message()
    if message!="":
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(message)



if __name__=="__main__":
    client.run(os.getenv('TOKEN'))