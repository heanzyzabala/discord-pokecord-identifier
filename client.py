import os
import discord
import utility
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()

TOKEN = os.getenv('TOKEN')


@client.event
async def on_ready():
    utility.load()
    print('{0.user} is up'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.embeds and str(message.author.id) == '365975655608745985':
        embed = message.embeds[0].to_dict()
        if 'A wild pokémon has аppeаred!' in embed['title']:
            name = utility.find(embed['image']['url'])
            msg = f'It\'s {name}!'
            if name is None:
                msg = 'I\'m not familiar with this pokemon. I\'ll try and revisit this soon.'
                print(embed['image']['url'])
            else:
               print(f'Identified {name}') 
            e = discord.Embed(title=msg, color=discord.colour.Color.dark_red())
            await message.channel.send(embed=e)

client.run(TOKEN)
