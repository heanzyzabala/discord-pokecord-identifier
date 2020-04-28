import os
import discord
import utility
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()
context = utility.load()

TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    print('{0.user} is up'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.embeds:
        print(message.embeds[0].to_dict())

    if message.attachments:
        file = utility.save(message.attachments[0].url)
        name = utility.find(file, context)

        if name:
            await message.channel.send(name)

client.run(TOKEN)
