import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

import random

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
TOKEN = "ODExMDE5MDcxODg1Mjc5MjYy.YCsGXg.gQDdN5jprthOH0iJMCEsta88AhI"

@bot.event
async def on_ready():
  print('Logged in as:')
  print(bot.user.name)
  print("Online")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="slash commands"), status=discord.Status.online, afk=False)

@slash.slash(name="helo", description="helo guise")
async def _helo(ctx: SlashContext):
  await ctx.send(content="helo!")

@slash.slash(name="rolldice", description="Roll a dice!")
async def _rolldice(ctx: SlashContext):
  await ctx.send(content="🎲 " + str(random.randrange(1, 6)))

@slash.slash(name="eightball", description="Get an answer from the beyond!", options=[create_option(
  name="question", description="Ask your question", required=True, option_type=3
)])
async def _eightball(ctx: SlashContext, question):
  embed = discord.Embed(title=question, description=random.choice(["🎱 Yes", "🎱 No", "🎱 Maybe", "🎱 Try again later", "🎱 That is a negative", "🎱 Perhaps"]), color=0x0000ff)
  await ctx.send(embed=embed)

bot.run(TOKEN)
