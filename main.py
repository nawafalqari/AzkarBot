from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands, tasks
from os import getenv
from json import load, dump

import functions
import api

# Discord Client
client = commands.Bot()

# data vars
bot_token = getenv('TOKEN')
azkar_rooms_path = 'data/azkar_rooms.json'

# read "azkar_rooms.json"
with open(azkar_rooms_path, 'r') as azkar_rooms_file:
	ar_data = load(azkar_rooms_file)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
	if message.author.bot: return
	print(message.content)
	if message.content == 'hello':
		await message.reply('Hello')

@client.slash_command(name='set_zekr', description='Create a room for Azkar')
async def set_zekr(ctx):
	await ctx.defer()

	guild = ctx.guild
	guild_id = guild.id

	if guild_id in ar_data:
		channel = client.get_channel(ar_data[guild_id])
		if channel:
			return await ctx.followup.send(f'There is {functions.mention_channel(channel.id)} already')

	created_channel = await guild.create_text_channel('أذكار-Azkar')

	ar_data[guild.id] = created_channel.id
	with open(azkar_rooms_path, 'w') as azkar_rooms_file:
		dump(ar_data, azkar_rooms_file, indent=3)

	await ctx.followup.send(f'Created {functions.mention_channel(created_channel.id)} successfully')

@tasks.loop(seconds=5)
async def loop():
	zekr = api.zekr()
	
	for key, val in ar_data.items():
		channel = client.get_channel(val)
		if channel:
			await channel.send(f'{zekr["content"]}')

# loop.start()
client.run(bot_token)