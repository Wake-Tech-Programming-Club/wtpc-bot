import discord
from discord.ext import commands
import random


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# FIXME: Fix Mypy(arg-type) error for these @bot.command() decorators
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def diceroll(ctx, sides=6):
    result = random.randint(1, sides)

    await ctx.send(result)
