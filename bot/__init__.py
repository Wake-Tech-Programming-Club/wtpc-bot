import os
import random
import time
from string import ascii_lowercase

import discord

__version__ = "0.1.0"


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


start_time = time.time()


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.environ["GUILD_ID"]))

    print(f"Logged in as {client.user}")


@tree.command()
async def info(interaction: discord.Interaction):
    """
    Gets information about the bot
    """
    await interaction.response.send_message(f"WTPC Bot **v{__version__}**")


# FIXME: Fix Mypy(arg-type) error for these @bot.command() decorators
@tree.command()
async def ping(interaction: discord.Interaction):
    """
    Returns "Pong!"
    """
    await interaction.response.send_message("Pong!")


@tree.command()
async def uptime(interaction: discord.Interaction):
    """
    Gets the uptime of the bot
    """
    uptime_hours = (time.time() - start_time) / 60 / 60

    await interaction.response.send_message(f"{round(uptime_hours, 2)} hours")


@tree.command()
async def diceroll(interaction: discord.Interaction, num_sides: int = 6):
    """
    Rolls a dice
    """
    result = random.randint(1, num_sides)

    return await interaction.response.send_message(result)


class PollModal(discord.ui.Modal, title="Create a Poll"):
    description: discord.ui.TextInput = discord.ui.TextInput(
        label="Description", default="Vote now!"
    )

    options: discord.ui.TextInput = discord.ui.TextInput(
        label="Options",
        placeholder="List each option on a new line",
        style=discord.TextStyle.long,
    )

    async def on_submit(self, interaction: discord.Interaction):
        options = self.options.value.splitlines()
        num_options = len(options)

        if not 2 <= num_options <= 26:
            return await interaction.response.send_message(
                "Must have between 2 and 26 options", ephemeral=True
            )

        message_content = f"{self.description.value}\n\n"

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

        await interaction.response.send_message(
            "Successfully created poll", ephemeral=True
        )


@tree.command()
async def poll(interaction: discord.Interaction):
    """
    Creates a poll
    """
    await interaction.response.send_modal(PollModal())
