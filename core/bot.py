"""
Fishing Game Discord Bot

This module sets up and runs a Discord bot for a fishing game. 
It includes command handlers for various game functions and admin tasks.
"""

# Packages and Libraries

## Built-In Modules
import os
import datetime
import time
import platform

## External Modules
import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style, Back
from dotenv import load_dotenv  # Secure Enviorenemnt

## Local Modules
from .logic import *


def run_bot():
    """
    Sets up and runs the Discord bot.

    This function loads environment variables, initializes the bot with required configurations,
    and defines event handlers and commands. The bot responds to various commands and 
    manages player data, leaderboards, and admin functionalities.
    """
    # * Loading the Discord (TOKEN/KEY) with dotenv
    load_dotenv()
    discord_token = os.getenv("TOKEN")

    # * BOT configs
    intents = discord.Intents.all()
    intents.message_content = True
    client = commands.Bot(command_prefix="/", intents=intents)
    current_time = time.gmtime()

    # -----------------------------------------------------------------------------

    # * Launch Response
    @client.event
    async def on_ready():
        """
        Event handler for when the bot is ready.

        Logs bot information such as name, ID, and versions, and syncs slash commands.
        """
        prfx = (
            Back.BLACK
            + Fore.GREEN
            + time.strftime("%Y-%m-%d - %H:%M:%S UTC", current_time)
            + Back.RESET
            + Fore.WHITE
            + Style.BRIGHT
        )
        print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        try:
            synced = await client.tree.sync()
        except Exception as e:
            print(e)
        print(
            prfx
            + " Slash CMD's Synced "
            + Fore.YELLOW
            + str(len(synced))
            + " Commands"
            + Fore.WHITE
            + Style.BRIGHT
        )

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    # * Commands

    ##* Player Commands

    @client.tree.command(name="fish")
    async def fish(interaction: discord.Interaction):
        """
        Command to catch a random fish and earn rewards.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message with the caught fish details and updates player data.
        """
        user_id = interaction.user.id
        player_instance = Player(user_id=user_id)

        catch = fishing(CATCHES)  # random fish catch
        catch_weight = catch.weight_algo()
        catch_value = round((catch.xp_loot_algo() * catch_weight) / 2)
        catch_xp = catch.value_loot_algo()
        if catch is not None:
            player_instance.load_from_leaderboard()
            player_instance.level += catch_xp
            player_instance.money += catch_value
            player_instance.level_check()
            player_instance.save_to_leaderboard()

            embed = discord.Embed(
                color=discord.Color.purple(), title="You've Caught:", type="rich"
            )

            embed.add_field(
                name=f"{catch.name.capitalize()}\n{catch.description}",
                value=f"""
                Rarity : **{catch.rarity}**
                Weight : **{catch_weight} KG**
                Gold Earned : **{catch_value}$**
                XP Earned : **{catch_xp} XP**
                """,
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            await interaction.response.send_message(
                "No catch available. Please try again!", ephemeral=True
            )

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="leaderboard")
    async def leaderboard(interaction: discord.Interaction, state: str):
        """
        Command to view the leaderboard sorted by specified attribute.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.
            state (str): The attribute to sort by ('money' or 'level').

        Sends an embed message with the sorted leaderboard.
        """
        sorted_leaderboard = sort_leaderboard(state)

        leaderboard_str = ""
        if state.lower() == "money":
            for rank, (user_id, money) in enumerate(sorted_leaderboard, start=1):
                leaderboard_str += f"{rank}. <@{user_id}> - **{money}$**\n"

        elif state.lower() in ["level", "levels"]:
            for rank, (user_id, level) in enumerate(sorted_leaderboard, start=1):
                leaderboard_str += f"{rank}. <@{user_id}> - **{level} XP**\n"
        else:
            await interaction.response.send_message(
                "Invalid filter. Please use 'money' or 'level'.", ephemeral=True
            )
            return

        embed = discord.Embed(
            color=discord.Color.purple(),
            title="Leaderboard",
            description=f"Here is the current leaderboard sorted by {state.capitalize()} : ",
        )

        embed.add_field(
            name="Top Players",
            value=leaderboard_str or "No data available",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=False)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="levels")
    async def levels(interaction: discord.Interaction):
        """
        Command to view the player's current levels and league.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message with the player's level and league information.
        """
        user_id = interaction.user.id
        player_instance = Player(user_id=user_id)
        player_instance.load_from_leaderboard()

        embed = discord.Embed(
            color=discord.Color.purple(),
            title="Your Levels",
            description=f"**Levels XP :** {player_instance.level} XP\n**League :** {player_instance.league}",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="money")
    async def money(interaction: discord.Interaction):
        """
        Command to view the player's current amount of money.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message with the player's current money.
        """
        user_id = interaction.user.id
        player_instance = Player(user_id=user_id)
        player_instance.load_from_leaderboard()

        embed = discord.Embed(
            color=discord.Color.purple(),
            title="Your Money in the Bank",
            description=f"**Money :** {player_instance.money}$",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="help")
    async def help_command(interaction: discord.Interaction):
        """
        Command to display available commands for regular users.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message listing all regular user commands and their descriptions.
        """
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Fishing Game Commands",
            description="Here is a list of available commands for regular users:",
        )

        user_commands_info = {
            "fish": "Catch a random fish and earn rewards.",
            "leaderboard": "View the leaderboard, sorted by 'money' or 'level'.",
            "levels": "Check your current levels and league.",
            "money": "Check your current amount of money.",
        }

        for command, description in user_commands_info.items():
            embed.add_field(name=f"/{command}", value=description, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    ##* Admin Commands

    @client.tree.command(name="reset-fisher")
    async def reset_player_stats(
        interaction: discord.Interaction, player_tag: str, state: str
    ):
        """
        Command to reset a player's specified attribute.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.
            player_tag (int): The unique identifier for the player.
            state (str): The attribute to reset ('money' or 'level').

        Sends an embed message indicating the result of the reset operation.
        """
        error_embed = discord.Embed(
            color=discord.Color.red(),
            title="Something went wrong, please check the player ID and state entered.",
        )
        success_embed = discord.Embed(
            color=discord.Color.green(),
            title=f"Player with ID \"{player_tag}\" {state} was reset successfully.",
        )

        result = reset_fisher(int(player_tag), state)
        if result is None:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=success_embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="delete-fisher")
    async def delete_player_command(interaction: discord.Interaction, player_tag: str):
        """
        Command to delete a player's data.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.
            player_tag (int): The unique identifier for the player.

        Sends an embed message indicating the result of the deletion operation.
        """
        error_embed = discord.Embed(
            color=discord.Color.red(),
            title="Player not found. Please check the player ID entered.",
        )
        success_embed = discord.Embed(
            color=discord.Color.green(),
            title=f"Player with ID \"{player_tag}\" has been deleted successfully.",
        )

        result = delete_player(int(player_tag))
        if result is None:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=success_embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="delete-all-fishers")
    async def delete_all_fishers(interaction: discord.Interaction):
        """
        Command to delete all player data.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message indicating the result of the deletion operation.
        """
        error_embed = discord.Embed(
            color=discord.Color.red(),
            title="Failed to delete all players. Please try again.",
        )
        success_embed = discord.Embed(
            color=discord.Color.green(),
            title="All players data has been deleted successfully.",
        )

        result = delete_all_players()
        if result is None:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=success_embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    @client.tree.command(name="modhelp")
    async def mod_help_command(interaction: discord.Interaction):
        """
        Command to display available commands for moderators.

        Args:
            interaction (discord.Interaction): The interaction object containing user data.

        Sends an embed message listing all moderator commands and their descriptions.
        """
        embed = discord.Embed(
            color=discord.Color.orange(),
            title="Moderator Commands",
            description="Here is a list of available commands for moderators:",
        )

        mod_commands_info = {
            "reset-fisher": "Reset a player's money or level. Use 'money' or 'level' as the state.",
            "delete-fisher": "Delete a player's data using their ID.",
            "delete-all-fishers": "Delete all players' data.",
        }

        for command, description in mod_commands_info.items():
            embed.add_field(name=f"/{command}", value=description, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------------------------------------------------------------------------------

    # ##* Shutdown
    # @client.tree.command(name="shutdown")
    # async def shutdown(interaction:discord.Interaction):
    #     print(Fore.RED +'The bot is shutting down')
    #     await interaction.response.send_message(content='The bot '
    #                                            'is shutting down...')
    #     await client.close()

    # * Run the Bot
    client.run(token=discord_token)


if __name__ == "__main__":
    # Run the bot
    bot.run_bot()
