import discord
from .constants import GUILD_ID
from string import ascii_lowercase
import random


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))

    print(f"Logged in as {client.user}")


# FIXME: Fix Mypy(arg-type) error for these @bot.command() decorators
@tree.command()
async def ping(interaction: discord.Interaction):
    """
    Returns "Pong!"
    """
    await interaction.response.send_message("Pong!")


@tree.command()
async def diceroll(interaction: discord.Interaction, num_sides: int = 6):
    """
    Rolls a dice
    """
    result = random.randint(1, num_sides)

    return await interaction.response.send_message(result)


@tree.command()
async def poll(interaction: discord.Interaction, *, description: str, options_str: str):
    """
    Creates a poll. Options should be a comma-separated list
    """
    options = options_str.split(",")
    num_options = len(options)

    if not 2 <= num_options <= 26:
        return await interaction.response.send_message(
            "Must have between 2 and 26 options", ephemeral=True
        )

    message_content = f"{description}\n\n"

    for i, option in enumerate(options):
        message_content += (
            f":regional_indicator_{ascii_lowercase[i]}: {option.strip()}\n"
        )

    # FIXME: Make sure we're in a text channel before doing this
    message = await interaction.channel.send(message_content)

    for i in range(0, num_options):
        # Maps letter index to the corresponding regional indicator symbol
        # (e.g., 0 => 🇦)
        char = chr(i + 0x1F1E6)

        await message.add_reaction(char)

    await interaction.response.send_message("Successfully created poll", ephemeral=True)
