import discord
from discord.ext import tasks
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

from api import getZekrFromLetter, validateCountryCode, validateCity, getTime, getLetterFromTime, checkPrayerTime

load_dotenv()

mclient = MongoClient(getenv("MONGODB_URI"))
db = mclient.servers.channels

client = discord.Bot(debug_servers=[715756723142393908])

class SetupView(discord.ui.View):
	def __init__(self, *items, timeout=180, disable_on_timeout: bool=True, channelId):
		self.channelId = channelId
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
	
	@discord.ui.button(label="العربية", emoji="<:arabic:1016280852524711998>")
	async def arabicButton(self, button: discord.ui.Button, interaction: discord.interactions.Interaction):
		serverSettingsData = {
			"serverId": interaction.guild.id,
			"channelId": self.channelId,
			"language": "arabic"
		}

		freqButtonLow = discord.ui.Button(label="LOW")
		freqButtonMid = discord.ui.Button(label="MID")
		freqButtonHigh = discord.ui.Button(label="HIGH")

		async def freqButtonLowCallback(interaction):
			serverSettingsData["frequency"] = "low"
			await afterFreqQ(interaction)
			

		async def freqButtonMidCallback(interaction):
			serverSettingsData["frequency"] = "mid"
			await afterFreqQ(interaction)
			

		async def freqButtonHighCallback(interaction):
			serverSettingsData["frequency"] = "high"
			await afterFreqQ(interaction)
			
			
		freqButtonLow.callback = freqButtonLowCallback
		freqButtonMid.callback = freqButtonMidCallback
		freqButtonHigh.callback = freqButtonHighCallback

		freqView = discord.ui.View(freqButtonLow, freqButtonMid, freqButtonHigh)

		embed = discord.Embed(color=0xffffff, title="إعداد | الوقت بين كل ذكر", description="كم مرة تريد استقبال الأذكار")
		embed.add_field(name="Low", value="`كل ساعة`", inline=False)
		embed.add_field(name="Mid", value="`كل 30 دقيقة`", inline=False)
		embed.add_field(name="High", value="`كل 10 دقائق`", inline=False)

		await interaction.response.edit_message(embed=embed, view=freqView)

		async def afterFreqQ(interaction: discord.interactions.Interaction):
			ONButton = discord.ui.Button(label="ON", style=discord.ButtonStyle.primary)
			OFFButton = discord.ui.Button(label="OFF")


			async def ONButtonCallback(interaction):
				serverSettingsData["prayerRem"] = "on"
				await afterPR(interaction)

			async def OFFButtonCallback(interaction):
				serverSettingsData["prayerRem"] = "off"
				await afterPR(interaction)

			ONButton.callback = ONButtonCallback
			OFFButton.callback = OFFButtonCallback

			prayerRemView = discord.ui.View(ONButton, OFFButton)

			embed = discord.Embed(color=0xffffff, title="إعداد | تذكير الصلاة", description="هل تريد رسالة تذكير في وقت الصلاة")
			embed.add_field(name="القيمة الإفتراضية للمنطقة الزمنية:", value="`مكة`", inline=False)
			embed.add_field(name="لتغيير الدولة استخدم الأمر:", value="`/timezone country <country>`", inline=False)
			embed.add_field(name="لتغيير المدينة استخدم الأمر:", value="`/timezone city <city>`", inline=False)

			await interaction.response.edit_message(embed=embed, view=prayerRemView)

			async def afterPR(interaction):
				embed = discord.Embed(color=0xffffff, title="إعداد | نجاح", description="**لقد تم الإعداد بنجاح**", timestamp=datetime.now())
				embed.set_footer(text=f"Ran by: {interaction.user}", icon_url=interaction.user.avatar.url)

				for key, val in serverSettingsData.items():
					if key == "prayerRem":
						embed.add_field(name="paryer reminder", value=val, inline=False)
					else:
						embed.add_field(name=key, value=val, inline=False)

				db.insert_one(serverSettingsData)

				await interaction.response.edit_message(embed=embed, view=None)

	@discord.ui.button(label="English", emoji="<:english:1016280854693163038>")
	async def englishButton(self, button: discord.ui.Button, interaction: discord.interactions.Interaction):
		serverSettingsData = {
			"serverId": interaction.guild.id,
			"channelId": self.channelId,
			"language": "arabic"
		}

		freqButtonLow = discord.ui.Button(label="LOW")
		freqButtonMid = discord.ui.Button(label="MID")
		freqButtonHigh = discord.ui.Button(label="HIGH")

		async def freqButtonLowCallback(interaction):
			serverSettingsData["frequency"] = "low"
			await afterFreqQ(interaction)
			

		async def freqButtonMidCallback(interaction):
			serverSettingsData["frequency"] = "mid"
			await afterFreqQ(interaction)
			

		async def freqButtonHighCallback(interaction):
			serverSettingsData["frequency"] = "high"
			await afterFreqQ(interaction)
			
			
		freqButtonLow.callback = freqButtonLowCallback
		freqButtonMid.callback = freqButtonMidCallback
		freqButtonHigh.callback = freqButtonHighCallback

		freqView = discord.ui.View(freqButtonLow, freqButtonMid, freqButtonHigh)

		embed = discord.Embed(color=0xffffff, title="Setup | Azkar Sending Frequency", description="How frequently do you want to receive azkar")
		embed.add_field(name="Low", value="`Every 1 hour`", inline=False)
		embed.add_field(name="Mid", value="`Every 30 minutes`", inline=False)
		embed.add_field(name="High", value="`Every 10 minutes`", inline=False)

		await interaction.response.edit_message(embed=embed, view=freqView)

		async def afterFreqQ(interaction: discord.interactions.Interaction):
			ONButton = discord.ui.Button(label="ON", style=discord.ButtonStyle.primary)
			OFFButton = discord.ui.Button(label="OFF")


			async def ONButtonCallback(interaction):
				serverSettingsData["prayerRem"] = "on"
				await afterPR(interaction)

			async def OFFButtonCallback(interaction):
				serverSettingsData["prayerRem"] = "off"
				await afterPR(interaction)

			ONButton.callback = ONButtonCallback
			OFFButton.callback = OFFButtonCallback

			prayerRemView = discord.ui.View(ONButton, OFFButton)

			embed = discord.Embed(color=0xffffff, title="Setup | Prayer Reminder", description="Do you want to get a reminding message at prayer time")
			embed.add_field(name="Default timezone:", value="`Makkah`", inline=False)
			embed.add_field(name="Change country:", value="`/timezone country <country>`", inline=False)
			embed.add_field(name="Change city:", value="`/timezone city <city>`", inline=False)

			await interaction.response.edit_message(embed=embed, view=prayerRemView)

			async def afterPR(interaction):
				embed = discord.Embed(color=0xffffff, title="Setup | Success", description="**Your server is ready to go!**", timestamp=datetime.now())
				embed.set_footer(text=f"Ran by: {interaction.user}", icon_url=interaction.user.avatar.url)

				for key, val in serverSettingsData.items():
					if key == "prayerRem":
						embed.add_field(name="paryer reminder", value=val, inline=False)
					else:
						embed.add_field(name=key, value=val, inline=False)

				db.insert_one(serverSettingsData)

				await interaction.response.edit_message(embed=embed, view=None)

	async def on_timeout(self):
		self.clear_items()

@client.event
async def on_ready():
	print(f"{client.user}: Ready!")

	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help, لا إله الا الله"))

	lowAzkarFrequency.start()
	midAzkarFrequency.start()
	highAzkarFrequency.start()

@client.command(description="Get bot commands")
async def help(ctx: discord.commands.context.ApplicationContext):
	embed = discord.Embed(color=0xffffff, title="Help")

	embed.add_field(name="Invite & Support", value="[Support Server](https://discord.gg/Az8McWNAcg)\n[Invite](https://discord.com/api/oauth2/authorize?client_id=720282117900075038&permissions=339008&scope=bot%20applications.commands)", inline=False)
	embed.add_field(name="Commands", value="""
	`/setup`: Setup azkar room for your server
	`/channel <channel>`: Change azkar room
	`/frequency <mode>`: Change azkar sending frequency
	`/language <language>`: Change bot language
	`/prayerreminder <mode>`: Turn prayer reminder on/off
	`/help`: Show this message
	""", inline=False)

	return await ctx.respond(embed=embed)

@client.command(description="Setup azkar channel for your server!")
@discord.option("channel", discord.TextChannel, description="The channel which is used to send azkar")
async def setup(ctx: discord.commands.context.ApplicationContext, channel: discord.TextChannel):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if not isinstance(channel, discord.channel.TextChannel):
		return await ctx.respond("Error: Can't use a category")
	if db.find_one({"serverId": ctx.guild.id}) is not None:
		return await ctx.respond("Error: you already ran `/setup` in this server, you can update your server settings using `/settings <option> <value>`")

	view = SetupView(channelId=channel.id)
	embed = discord.Embed(color=0xffffff, title="Setup | Language", description="Which language do you want me to use in this server")

	return await ctx.respond(view=view, embed=embed)

@client.command(description="Change azkar channel")
@discord.option("channel", discord.TextChannel)
async def channel(ctx: discord.commands.context.ApplicationContext, channel):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if db.find_one({"serverId": ctx.guild.id}) is None:
		return await ctx.respond("Error: Run `/setup` first!")

	db.update_one({"serverId": ctx.guild.id}, {
		"$set": {
			"channelId": channel.id
		}
	})

	return await ctx.respond(f"Azkar channel was changed to {channel.mention}")

@client.command(description="Change bot language")
@discord.option("language", description="Language", choices=["Arabic", "English"])
async def language(ctx: discord.commands.context.ApplicationContext, language):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if db.find_one({"serverId": ctx.guild.id}) is None:
		return await ctx.respond("Error: Run `/setup` first!")

	language = language.lower()
	db.update_one({"serverId": ctx.guild.id}, {
		"$set": {
			"language": language
		}
	})

	return await ctx.respond(f"Changed language to {language}")

@client.command(description="Change azkar sending frequency")
@discord.option("frequency", description="azkar frequency", choices=["Low", "Mid", "High"])
async def frequency(ctx: discord.commands.context.ApplicationContext, frequency):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if db.find_one({"serverId": ctx.guild.id}) is None:
		return await ctx.respond("Error: Run `/setup` first!")

	frequency = frequency.lower()
	db.update_one({"serverId": ctx.guild.id}, {
		"$set": {
			"frequency": frequency
		}
	})

	return await ctx.respond(f"Changed frequency to {frequency}")

@client.command(description="Set prayer reminder ON/OFF")
@discord.option("value", description="ON/OFF", choices=["ON", "OFF"])
async def prayerreminder(ctx: discord.commands.context.ApplicationContext, value):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if db.find_one({"serverId": ctx.guild.id}) is None:
		return await ctx.respond("Error: Run `/setup` first!")

	value = value.lower()
	db.update_one({"serverId": ctx.guild.id}, {
		"$set": {
			"prayerRem": value
		}
	})

	return await ctx.respond(f"Turned prayer reminder `{value}`")

@client.command(description="Edit country + city timezone for your server!")
@discord.option("country", required=True, description="timezone country, like: EG, SA, GB")
@discord.option("city", required=True, description="timezone city")
async def timezone(ctx: discord.commands.context.ApplicationContext, country, city):
	await ctx.defer()

	if not ctx.author.guild_permissions.administrator:
		return await ctx.respond("Error: You don't have enough permissions")
	if (serverSettings := db.find_one({"serverId": ctx.guild.id})) is None:
		return await ctx.respond("Error: Run `/setup` first!")
	
	country = country.upper()
	countryValidation, countryName = validateCountryCode(country)

	if not countryValidation:
		return await ctx.respond("Error: Invalid country code, example: `EG` -> Egypt, `SA` -> Saudi Arabia")

	else:
		db.update_one({"serverId": ctx.guild.id}, {
			"$set": {
				"country": country
			}
		})


	city = city.lower()
	cityValidation = validateCity(serverSettings.get(country), city)

	if not cityValidation:
		return await ctx.respond("Error: Invalid city!")

	else:
		db.update_one({"serverId": ctx.guild.id}, {
			"$set": {
				"city": city
			}
		})

	return await ctx.respond(f"Your server's timezone was updated to {countryName}/{city.title()}")

@client.command(description="Server status")
async def status(ctx: discord.commands.context.ApplicationContext):
	if (serverSettings := db.find_one({"serverId": ctx.guild.id})) is None:
		return await ctx.respond("Error: Run `/setup` first!")

	greenEmj = "<:online:1017019759033864292>"
	redEmj = "<:dnd:1017019761592381532>"
	arabicEmj = "<:arabic:1016280852524711998>"
	englishEmj = "<:english:1016280854693163038>"

	serverChannel = client.get_channel(serverSettings["channelId"])

	embed = discord.Embed(color=0xffffff, title="Server Status")
	if serverChannel:
		embed.add_field(name="Channel:", value=f"{greenEmj}{serverChannel.mention}", inline=False)
	else:
		embed.add_field(name="Channel:", value=f"{redEmj}{serverSettings['channelId']} (deleted channel)", inline=False)

	embed.add_field(name="Language:", value=f"{arabicEmj if serverSettings['language'] == 'arabic' else englishEmj}{serverSettings['language'].title()}", inline=False)

	embed.add_field(name="Frequency:", value=f"{serverSettings['frequency'].upper()}", inline=False)

	embed.add_field(name="Prayer Reminder:", value=f"{serverSettings['prayerRem'].upper()}", inline=False)

	if not serverSettings.get("country") or not serverSettings.get("city"):
		embed.add_field(name="Country:", value="Saudi Arabia")
		embed.add_field(name="City:", value="Makkah")
	else:
		embed.add_field(name="Country:", value=f"{serverSettings['country']}")
		embed.add_field(name="City:", value=f"{serverSettings['city'].title()}")

	embed.set_footer(text=f"Guild ID: {ctx.guild.id}")

	return await ctx.respond(embed=embed)

@tasks.loop(hours=1)
async def lowAzkarFrequency():
	servers = db.find({"frequency": "low"})

	for server in servers:
		if not server.get("country") or not server.get("city"):
			server["country"] = "SA"
			server["city"] = "makkah"

		time = getTime(server["country"], server["city"])
		letter = getLetterFromTime(time)
		zekr = getZekrFromLetter(letter or 't')

		serverChannel = client.get_channel(server["channelId"])
		if serverChannel:
			message = await serverChannel.send(zekr)
			await message.add_reaction("♥")

@tasks.loop(minutes=30)
async def midAzkarFrequency():
	servers = db.find({"frequency": "mid"})

	for server in servers:
		if not server.get("country") or not server.get("city"):
			server["country"] = "SA"
			server["city"] = "makkah"

		time = getTime(server["country"], server["city"])
		letter = getLetterFromTime(time)
		zekr = getZekrFromLetter(letter or 't')

		serverChannel = client.get_channel(server["channelId"])
		if serverChannel:
			message = await serverChannel.send(zekr)
			await message.add_reaction("♥")

@tasks.loop(minutes=10)
async def highAzkarFrequency():
	servers = db.find({"frequency": "high"})

	for server in servers:
		if not server.get("country") or not server.get("city"):
			server["country"] = "SA"
			server["city"] = "makkah"

		time = getTime(server["country"], server["city"])
		letter = getLetterFromTime(time)
		zekr = getZekrFromLetter(letter or 't')

		serverChannel = client.get_channel(server["channelId"])
		if serverChannel:
			message = await serverChannel.send(zekr)
			await message.add_reaction("♥")

@tasks.loop(minutes=1)
async def prayerReminder():
	servers = db.find({"prayerRem": "on"})

	for server in servers:
		if not server.get("country") or not server.get("city"):
			server["country"] = "SA"
			server["city"] = "makkah"
		
		time = getTime(server["country"], server["city"])
		prayerCheck = checkPrayerTime(time, server["country"], server["city"])

		serverChannel = client.get_channel(server["channelId"])

		if serverChannel:
			if prayerCheck:
				message = await serverChannel.send(prayerCheck)
				message.add_reaction("♥")

client.run(getenv("TOKEN"))