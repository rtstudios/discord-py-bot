import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

import random
import asyncio
from datetime import date
import praw
import prayertimes
from discord.utils import get
from discord import FFmpegPCMAudio
import os
from os import system
import youtube_dl
import requests
import ffmpeg
import urllib.request
import re

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")
TOKEN = ""

# VARIABLE SETUP

diceList = [1, 2, 3, 4, 5, 6]

flipCoin = ["Heads", "Tails"]

responses = ["🎱 Yes", "🎱 No", "🎱 Maybe", "🎱 Try Again Later", "🎱 Perhaps", "🎱 My sources say no"]

prayerTimes = prayertimes.PrayTimes()

reddit = praw.Reddit(
  client_id="",
  client_secret="",
  user_agent="",
  username="",
  password="",
)
memes = reddit.subreddit("dankmemes")
catSubreddit = reddit.subreddit("catpictures")
dogSubreddit = reddit.subreddit("dogpictures")
monkeSubreddit = reddit.subreddit("Monke")

giveawayMembers = []

status = random.choice([discord.Status.online, discord.Status.do_not_disturb, discord.Status.idle])

# BOT EVENTS

@bot.event
async def on_ready():
  print('Logged in as:')
  print(bot.user.name)
  print("Online")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="discord.py"), status=status, afk=False)

@bot.event
async def on_message(message: discord.Message):
  dmChannel = bot.get_channel(724786109154066463)
  if message.author.id != 184408626306351104 and not message.author.bot and message.guild is None:
    embed = discord.Embed(title="Message received", description="**From** " + str(message.author.mention) + "\n \n" + str(message.content), color=0x0000ff)
    await dmChannel.send(embed=embed)
  await bot.process_commands(message)

# BOT COMMANDS

# Help command
@slash.slash(name="help", description="Provides a list of commands.")
async def help(ctx: SlashContext):
  helpText = """
  /help - Shows this message


  **Fun commands**

  /flipcoin - Flips a coin
  /rolldice - Rolls a dice
  /eightball [question] - Gives a random response to the given question
  /tp - Teleports mentioned person
  /russianroulette - Shoots (pings) a random user
  /meme - Sends a random meme from r/dankmemes
  /dog - Sends a random dog picture from r/dogpictures
  /cat - Sends a random cat picture from r/catpictures
  /monke - Sends a random ape picture from r/ape
  /math [operation] [number] [number] - Performs an operation on two numbers
  /prayertimes - Gives the prayer times
  /giveaway [time in minutes] [item] - Starts a giveaway
  /pp - Gives a random PP size
  /animate [mode] [message] - Animates a message
  /poll [reaction one] [reaction two] [question] - Creates a poll


  **Voice chat commands (requires "DJ" role)**

  /join - Bot join voice channel 
  /play [query] - Plays a song from YouTube with the given query 
  /leave - Bot leaves voice channel 
  /pause - Bot pauses current audio 
  /resume - Bot resumes current audio 


  **Moderation commands (requires "kool kid" role)**

  /mute [user] [reason] - Mutes a user indefinitely
  /unmute [user] - Unmutes user
  /cancel [user] [reason] - Kicks user from server
  /kill [user] [reason] - Bans user from server
  /cleanse [number] - Deletes a certain number of messages


  **Misc commands**

  /hello - Says hello and mentions author
  /invite [user] [game] - Bot invites a user to play a game via DMs
  /message [user id] [message] - Bot DMs given user
  /ping - Returns bot latency
  /who [user id] - Returns a user's information with the given ID
  """

  embed = discord.Embed(title="Commands", description=helpText, color=0x0000ff)
  await ctx.send(embed=embed)

# Says hello
@slash.slash(name="hello", description="Says hello!")
async def hello(ctx: SlashContext):
  await ctx.send("Hello " + str(ctx.author.mention) + "!")

# Flips a coin
@slash.slash(name="flipcoin", description="Flip a coin.")
async def flipcoin(ctx: SlashContext):
  embed = discord.Embed(title=":coin:", description="You got " + str(random.choice(flipCoin)), color=0x0000ff)
  await ctx.send(embed=embed)

# Rolls a dice
@slash.slash(name="rolldice", description="Roll a dice.")
async def rolldice(ctx: SlashContext):
  embed = discord.Embed(title="🎲", description="You got a " + str(random.choice(diceList)), color=0x0000ff)
  await ctx.send(embed=embed)

# Magic 8 Ball
@slash.slash(name="eightball", description="Answers from the beyond!", options=[
  create_option(name="question", description="Ask your question.", required=True, option_type=3)
])
async def eightball(ctx: SlashContext, question):
  embed = discord.Embed(title=question, description=str(random.choice(responses)), color=0x0000ff)
  await ctx.send(embed=embed)

# Teleport command
@slash.slash(name="tp", description="Teleport someone to a random location!", options=[
  create_option(name="person", description="Who do you want to teleport?", required=True, option_type=3)
])
async def tp(ctx: SlashContext, person):
  embed = discord.Embed(title="Teleported!", description=str(person) + " teleported to " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)) + ", " + str(random.randrange(-1000, 1000)), color=0x0000ff)
  await ctx.send(embed=embed)

# Picks out a random server member
@slash.slash(name="russianroulette", description="Ping a random server member!")
async def russianroulette(ctx: SlashContext):
  user = random.choice(ctx.channel.guild.members)
  await ctx.send(f"{ctx.author.mention} *shot* {user.mention}")

# Sends a meme from reddit
@slash.slash(name="meme", description="Sends a random meme from r/dankmemes")
async def meme(ctx: SlashContext):
  posts = memes.hot(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/dankmemes", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a cat image from reddit
@slash.slash(name="cat", description="Sends a random picture from r/catpictures")
async def cat(ctx: SlashContext):
  posts = catSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/catpictures", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a dog image from reddit
@slash.slash(name="dog", description="Sends a random picture from r/dogpictures")
async def dog(ctx: SlashContext):
  posts = dogSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/dogpictures", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# Sends a monke image from reddit
@slash.slash(name="monke", description="Sends a random meme from r/monke")
async def monke(ctx: SlashContext):
  posts = monkeSubreddit.top(limit=100)
  random_post_number = random.randint(0,100)
  for i, post in enumerate(posts):
    if i == random_post_number:
      embed = discord.Embed(title="r/Monke", color=0x0000ff)
      embed.set_image(url=str(post.url))
      await ctx.send(embed=embed)

# This command solves math problems
@slash.slash(name="math", description="Solve a math problem", options=[
  create_option(name="operation", description="add, subtract, multiply, or divide?", required=True, option_type=3),
  create_option(name="number1", description="What's the first number?", required=True, option_type=3),
  create_option(name="number2", description="What's the second number??", required=True, option_type=3)
])
async def math(ctx: SlashContext, operation, number1, number2):
  if operation == "add":
    await ctx.send(str(number1) + " + " + str(number2) + " = " + str(int(number1) + int(number2)))
  elif operation == "subtract":
    await ctx.send(str(number1) + " - " + str(number2) + " = " + str(int(number1) - int(number2)))
  elif operation == "multiply":
    await ctx.send(str(number1) + " * " + str(number2) + " = " + str(int(number1) * int(number2)))
  elif operation == "divide":
    await ctx.send(str(number1) + " / " + str(number2) + " = " + str(int(number1) / int(number2)))

# Bot joins the voice channel
@slash.slash(name="join", description="Bot joins the voice channel.")
@commands.has_role("DJ")
async def join(ctx: SlashContext):
  author = ctx.author
  channel = author.voice.channel
  vc = await channel.connect()
  embed = discord.Embed(title="Connected", description="Hello" + "\n \n" + "Action requested by " + str(ctx.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Plays audio with the given query
@slash.slash(name="play", description="Bot plays a YouTube video with the given query.", options=[
  create_option(name="query", description="What do you want to listen to?", required=True, option_type=3),
])
@commands.has_role("DJ")
async def play(ctx: SlashContext, *, query):
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  videoTitle = ""
  voice = get(bot.voice_clients, guild=ctx.guild)
  songThere = os.path.isfile("song.mp3")

  def repeat():
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: repeat())
    voice.volume = 100
    voice.is_playing()

  try:
    if songThere:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Something went wrong :/")
    return

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    searchQuery = query.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searchQuery)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    result = "https://www.youtube.com/watch?v=" + video_ids[0]
    
    info_dict = ydl.extract_info(result, download=False)
    videoTitle = info_dict.get('title', None)
    videoThumbnail = info_dict.get('thumbnail', None)
    
    embedShortly = discord.Embed(title="Downloading", description=videoTitle + "\n \n" + "Audio requested by " + str(ctx.author.mention), color=0x00ff00)
    await ctx.send(embed=embedShortly)

    ydl.download([result])
    
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, 'song.mp3')
  
  voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: repeat())
  voice.volume = 100
  voice.is_playing()
  embedPlaying = discord.Embed(title="Now playing", description=videoTitle + "\n \n" + "Audio requested by " + str(ctx.author.mention), color=0x0000ff)
  embedPlaying.set_image(url=videoThumbnail)
  await ctx.send(embed=embedPlaying)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=videoTitle), status=status, afk=False)

# Bot pauses current audio
@slash.slash(name="pause", description="Bot pauses the playing audio.")
@commands.has_role("DJ")
async def pause(ctx: SlashContext):
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.pause()
  embed = discord.Embed(title="Paused", description="Audio has been paused" + "\n \n" + "Action requested by " + str(ctx.author.mention), color=0x0000ff)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="discord.py"), status=status, afk=False)
  await ctx.send(embed=embed)

# Bot resumes playing audio
@slash.slash(name="resume", description="Bot resumes the playing audio.")
@commands.has_role("DJ")
async def resume(ctx: SlashContext):
  voice = get(bot.voice_clients, guild=ctx.guild)
  voice.resume()
  embed = discord.Embed(title="Resumed", description="Audio has been resumed" + "\n \n" + "Action requested by " + str(ctx.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Bot disconnects from voice channel
@slash.slash(name="leave", description="Bot disconnects from the voice channel.")
@commands.has_role("DJ")
async def leave(ctx: SlashContext):
  voice = ctx.guild.voice_client
  await voice.disconnect(force = True)
  embed = discord.Embed(title="Disconnected", description="Goodbye" + "\n \n" + "Action requested by " + str(ctx.author.mention), color=0x0000ff)
  await ctx.send(embed=embed)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="discord.py"), status=status, afk=False)

# Returns the prayer times for that day
@slash.slash(name="prayertimes", description="Get the Islamic prayer times for the day.")
async def prayertimes(ctx: SlashContext):
  prayerTimesList = []
  times = prayerTimes.getTimes(date.today(), (42, 73), 5.7)
  for i in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
    prayerTimesList.append(str(i + ': ' + times[i.lower()]))
  prayerTimesStr = prayerTimesList[0] + "\n" + prayerTimesList[1] + "\n" + prayerTimesList[2] + "\n" + prayerTimesList[3] + "\n" + prayerTimesList[4] + "\n"
  embed = discord.Embed(title="Prayer times", description=prayerTimesStr, color=0x0000ff)
  await ctx.send(embed=embed)

# Starts a giveaway
@slash.slash(name="giveaway", description="Start a giveaway.", options=[
  create_option(name="duration", description="How long is the giveaway (in minutes)?", required=True, option_type=3),
  create_option(name="item", description="What are you giving away?", required=True, option_type=3),
])
async def giveaway(ctx: SlashContext, duration, *, item):
  embed = discord.Embed(title=item, description=str(ctx.author.mention) + " is giving away " + str(item) + "\n" + "\n" + "React below to enter!", color=0x0000ff)
  message = await ctx.send(embed=embed)
  await message.add_reaction("💩")
  reaction, user = await bot.wait_for('reaction_add')
  giveawayMembers.append(user)

  await asyncio.sleep(int(duration) * 60)

  winner = random.choice(giveawayMembers)
  winEmbed = discord.Embed(title="Winner", description=str(winner.mention + " has won " + item), color=0x0000ff)
  await ctx.send(embed=winEmbed)

# PP size
@slash.slash(name="pp", description="How big is your PP?")
async def pp(ctx: SlashContext):
  lengthOfPP = []
  lengthOfPPString = ""

  for i in range(random.randrange(1, 20)):
    lengthOfPP.append("=")

  embed = discord.Embed(title="Penis size", description="8" + lengthOfPPString.join(lengthOfPP) + "D", color=0x0000ff)
  await ctx.send(embed=embed)

# Override command
@bot.command(pass_context = True)
@commands.is_owner()
async def override(ctx, *, message):
  await ctx.send(message)
  await ctx.message.delete()

  user = bot.get_user(184408626306351104)
  message = discord.Embed(title="Override", description="**Name** " + str(ctx.message.author.name) + "\n" + "**User ID** " + str(ctx.message.author.id) + "\n" + "**Message** " + message, color=0x0000ff)
  await user.send(embed=message)

# Invites a user to play a game
@slash.slash(name="invite", description="Invite a friend to a game!", options=[
  create_option(name="user", description="Ping your friend", required=True, option_type=discord.Member),
  create_option(name="game", description="What game do you wanna play?", required=True, option_type=3),
])
async def invite(ctx: SlashContext, member: discord.Member, game):
  user = await member.create_dm()
  await user.send("Hello, " + ctx.author.mention + " invited you to play " + str(game))
  embed = discord.Embed(title="Invite sent", description="**From** " + str(ctx.author.mention) + "\n" + "**To** " + str(member.mention), color=0x0000ff)
  await ctx.send(embed=embed)

# Message command
@slash.slash(name="message", description="Message someone!", options=[
  create_option(name="user", description="Ping your friend", required=True, option_type=discord.Member),
  create_option(name="message", description="What do you wanna say?", required=True, option_type=3),
])
async def message(ctx: SlashContext, member: discord.Member, message):
  try:
    user = await member.create_dm()
    await user.send(message)
    embed = discord.Embed(title="Message sent", description=message + "\n \n**From** " + str(ctx.author.mention) + "\n" + "**To** " + member.mention, color=0x0000ff)
    await ctx.send(embed=embed)
  except:
    embed = discord.Embed(title="Messsage failed", description="Error 404: User not found.", color=0xff0000)
    await ctx.send(embed=embed)

# Mutes user
@slash.slash(name="mute", description="Mute a server member.", options=[
  create_option(name="member", description="Ping the member", required=True, option_type=discord.Member),
  create_option(name="reason", description="Why will they be muted?", required=True, option_type=3),
])
@commands.has_role("kool kid")
async def mute(ctx: SlashContext, member: discord.Member, reason):
  role = discord.utils.get(member.guild.roles, name="Muted")
  await member.add_roles(role)
  embed = discord.Embed(title="User muted", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(reason), color=0x0000ff)
  embed.set_image(url="https://media.tenor.com/images/ac7f9ffd8f172477e28ab284b1134b76/tenor.gif")
  await ctx.send(embed=embed)
  user = await member.create_dm()
  await user.send("You were muted for " + str(reason))

# Unmutes a user
@slash.slash(name="unmute", description="Unmute a server member.", options=[
  create_option(name="member", description="Ping the member", required=True, option_type=discord.Member),
])
@commands.has_role("kool kid")
async def unmute(ctx: SlashContext, member: discord.Member):
  roleMuted = discord.utils.get(member.guild.roles, name="Muted")
  await member.remove_roles(roleMuted)
  await ctx.send(str(member.mention) + " has been unmuted!")

# Kicks user
@slash.slash(name="cancel", description="Kick a server member.", options=[
  create_option(name="member", description="Ping the member", required=True, option_type=discord.Member),
  create_option(name="reason", description="Why will they be kicked?", required=True, option_type=3)
])
@commands.has_role("kool kid")
async def cancel(ctx: SlashContext, member: discord.Member, reason):
  await member.kick(reason=reason)
  embed = discord.Embed(title="User kicked", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(reason), color=0x0000ff)
  embed.set_image(url="https://media1.giphy.com/media/edP47TgaxmTy4OV2cW/giphy.gif")
  await ctx.send(embed=embed)
  user = await member.create_dm()
  await user.send("You were kicked for " + str(reason))

# Bans user
@slash.slash(name="kill", description="Ban a server member.", options=[
  create_option(name="member", description="Ping the member", required=True, option_type=discord.Member),
  create_option(name="reason", description="Why will they be banned?", required=True, option_type=3)
])
@commands.has_role("kool kid")
async def kill(ctx: SlashContext, member: discord.Member, reason):
  await member.ban(reason=reason)
  embed = discord.Embed(title="User banned", description="**User** " + str(member.mention) + "\n" + "**Reason** " + str(reason), color=0x0000ff)
  embed.set_image(url="https://media.giphy.com/media/jxqOV4sZ8eM5o4W16H/giphy.gif")
  await ctx.send(embed=embed)
  user = await member.create_dm()
  await user.send("You were banned for " + str(reason))

# Deletes messages
@slash.slash(name="cleanse", description="Delete a set number of messages.", options=[
  create_option(name="number", description="How many messages do you want to delete?", required=True, option_type=3)
])
@commands.has_role("kool kid")
async def cleanse(ctx: SlashContext, number):
  await ctx.channel.purge(limit=int(number))
  embed = discord.Embed(title="Cleansed", description="**This channel has been cleansed** \n" + str(number) + " messages have been deleted.", color=0x0000ff)
  embed.set_image(url="https://media.tenor.com/images/00fb44a75f05b234087ed5c1c93763e9/tenor.gif")
  await ctx.send(embed=embed)
  
# Animates message
@slash.slash(name="animate", description="Animate a message.", options=[
  create_option(name="mode", description="Horizontal or vertical?", required=True, option_type=3),
  create_option(name="message", description="What do you want to animate?", required=True, option_type=3),
])
async def animate(ctx: SlashContext, mode, message):
  if str(mode).lower() == "horizontal":
    messageSpaces = ""
    botMessage = await ctx.send(message)
    for i in range(20):
      messageSpaces += "⠀" * i
      await botMessage.edit(content = str(messageSpaces) + str(message))
      await asyncio.sleep(0.2)
  elif str(mode).lower() == "vertical":
    messageEnters = ""
    botMessage = await ctx.send(message)
    for i in range(10):
      messageEnters += "\n ⠀" * i
      await botMessage.edit(content = str(messageEnters) + str(message))
      await asyncio.sleep(0.2)

# Returns bot latency
@slash.slash(name="ping", description="Returns bot latency.")
async def ping(ctx: SlashContext):
  embed = discord.Embed(title = "Pong!", description = "**Latency** " + str(round(bot.latency * 1000)) + "ms", color=0x0000ff)
  await ctx.send(embed=embed)

# Returns user info
@slash.slash(name="who", description="Get user info.", options=[
  create_option(name="userid", description="What's the User ID? (you need developer mode enabled)", required=True, option_type=3),
])
async def who(ctx: SlashContext, userID):
  print("userID")
  user = await bot.fetch_user(int(userID))
  userInfo = "**User ID** " + str(user.id) + "\n" + "**Is Bot** " + str(user.bot) + "\n" + "**Created** " + str(user.created_at) + "\n"
  embed = discord.Embed(title = user.name + "#" + user.discriminator, description = userInfo, color=0x0000ff)
  embed.set_image(url=user.avatar_url)
  await ctx.send(embed=embed)

# Creates a poll
@slash.slash(name="poll", description="Create a poll!", options=[
  create_option(name="reaction1", description="What's the first response? (emoji)", required=True, option_type=3),
  create_option(name="reaction2", description="What's the second response? (emoji)", required=True, option_type=3),
  create_option(name="question", description="What's the question?", required=True, option_type=3),
])
async def poll(ctx: SlashContext, reactionOne, reactionTwo, question):
  embed = discord.Embed(title = "Poll", description = question, color=0x0000ff)
  message = await ctx.send(embed=embed)
  await message.add_reaction(reactionOne)
  await message.add_reaction(reactionTwo)

# Gives DJ and kool kid roles
@bot.command(pass_context = True)
@commands.is_owner()
async def roles(ctx):
  guild = ctx.guild
  koolKid = await guild.create_role(name="kool kid")
  dj = await guild.create_role(name="DJ")
  await ctx.author.add_roles(koolKid, dj)


bot.run(TOKEN)
