
# Table of Contents
- [Overview](#overview)
- [Commands](#commands)
- [Requirements](#requirements)
- [Installation](#installation)
- [License](#license)

# Overview

This open-source Discord Fishing Game Bot offers a fun and interactive fishing experience for your Discord server. Players can catch fish, level up and earn money, and compete on leaderboards. The bot is designed to be easy to use and integrates seamlessly with Discord.


# Commands

## Player Commands 🎣

- **/fish**: Catch a random fish and earn rewards such as money and experience points.
- **/leaderboard [state]**: View the leaderboard, sorted by either 'money' or 'level'.
- **/levels**: Check your current level and league in the fishing game.
- **/money**: View the amount of money you have earned in the game.
- **/help**: Display a list of available commands for regular users.
  
## Moderator Commands 🛠️

- **/reset-fisher [player_id] [state]**: Reset a player's money or level. Use 'money' or 'level' as the state.
- **/delete-fisher [player_id]**: Delete a player's data using their ID.
- **/delete-all-fishers**: Delete all player data from the leaderboard.
- **/modhelp**: Display a list of available commands for moderators.

# Requirements

- A Discord Bot (create one using the [Discord developer portal](https://discord.com/developers/applications)).
- Python 3.11.2 or above ([Download Python](https://www.python.org/downloads)).
  - **Recommended version**: 3.11.2
- A Discord server that you own.
  - Make sure to "enable community" in your server if you haven't already! (Settings -> Enable Community)

# Installation

## Step 1: Install Dependencies

- Install the required packages using the command below:

```bash
pip install -r requirements.txt
```
> If you are on Windows, you might need to run command prompt as Administrator

## Step 02 :
- Create a .env file in the project directory and place your Discord Token in the TOKEN field:
```
TOKEN=''
```

## Step 03 :
- Execute the main.py file to start the bot.

```bash
python main.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.


