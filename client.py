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

    if message.embeds and str(message.author.id) == '365975655608745985':
        embed = message.embeds[0].to_dict()
        if 'A wild pokémon has аppeаred!' in embed['title']:
            file = utility.save(embed['image']['url'])
            name = utility.find(file, context)
            e = discord.Embed(title=f'It\'s {name}!', color=discord.colour.Color.dark_red())
            await message.channel.send(embed=e)

client.run(TOKEN)
