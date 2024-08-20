"""
Fishing Game Module

This module provides functionality for managing players, their data, and loot in a fishing game. 
It includes classes and functions to handle player statistics, loot generation, and leaderboard management.
"""

# Packages and Libraries

## Built-In Modules
import json
import random
import os


PLAYERS_PATH: str = "players.json"

RARITY_PROBABILITIES: dict = {
    "Trash": 0.239,  # 26.9%
    "Common": 0.25,  # 25%
    "Uncommon": 0.20,  # 20%
    "Rare": 0.10,  # 10%
    "Epic": 0.08,  # 8%
    "Supreme": 0.08,  # 8%
    "Mythical": 0.05,  # 2%
    "Legendary": 0.001,  # 0.1%
}


class Loot:
    """
    Represents a loot item in the fishing game.

    Attributes:
        name (str): The name of the loot item.
        rarity (str): The rarity of the loot item.
        description (str): A description of the loot item.
        value (int): The value of the loot item (default is 0).
        xp_loot (int): The XP value of the loot item (default is 0).
        weight (float): The weight of the loot item (default is 0.0).
    """
    def __init__(
        self,
        name: str,
        rarity: str,
        description: str,
        value: int = 0,
        xp_loot: int = 0,
        weight: float = 0,
    ):
        """
        Initializes a Loot instance.

        Args:
            name (str): The name of the loot item.
            rarity (str): The rarity of the loot item.
            description (str): A description of the loot item.
            value (int, optional): The value of the loot item. Defaults to 0.
            xp_loot (int, optional): The XP value of the loot item. Defaults to 0.
            weight (float, optional): The weight of the loot item. Defaults to 0.0.
        """
        self.name = name
        self.description = description
        self.rarity = rarity
        self.value = value
        self.xp_loot = xp_loot
        self.weight = weight

    def value_loot_algo(self) -> int:
        """
        Calculates and updates the value of the loot item based on its rarity.

        Returns:
            int: The value of the loot item.
        """
        try:
            match self.rarity:
                case "Common":
                    self.value = random.randint(10, 50)
                case "Uncommon":
                    self.value = random.randint(51, 150)
                case "Rare":
                    self.value = random.randint(151, 500)
                case "Epic":
                    self.value = random.randint(501, 1500)
                case "Supreme":
                    self.value = random.randint(1501, 3000)
                case "Mythical":
                    self.value = random.randint(3001, 5000)
                case "Legendary":
                    self.value = random.randint(5001, 10_000)
                case "Trash":
                    self.value = random.randint(1, 9)
                case _:
                    self.value = 0
            return self.value
        except Exception as e:
            print(f"Error calculating value: {e}")
            return 0

    def xp_loot_algo(self) -> int:
        """
        Calculates and updates the XP value of the loot item based on its rarity.

        Returns:
            int: The XP value of the loot item.
        """
        try:
            match self.rarity:
                case "Common":
                    self.xp_loot = random.randint(50, 100)
                case "Uncommon":
                    self.xp_loot = random.randint(101, 250)
                case "Rare":
                    self.xp_loot = random.randint(251, 500)
                case "Epic":
                    self.xp_loot = random.randint(501, 1000)
                case "Supreme":
                    self.xp_loot = random.randint(1001, 2000)
                case "Mythical":
                    self.xp_loot = random.randint(2001, 3500)
                case "Legendary":
                    self.xp_loot = random.randint(3501, 5000)
                case "Trash":
                    self.xp_loot = 0
                case _:
                    self.xp_loot = 0
            return self.xp_loot
        except Exception as e:
            print(f"Error calculating XP: {e}")
            return 0

    def weight_algo(self) -> float:
        """
        Calculates and updates the weight of the loot item based on its rarity.

        Returns:
            float: The weight of the loot item.
        """
        try:
            match self.rarity:
                case "Common":
                    self.weight = round(random.uniform(1.0, 5.0), 2)
                case "Uncommon":
                    self.weight = round(random.uniform(5.1, 10.0), 2)
                case "Rare":
                    self.weight = round(random.uniform(10.1, 20.0), 2)
                case "Epic":
                    self.weight = round(random.uniform(20.1, 30.0), 2)
                case "Supreme":
                    self.weight = round(random.uniform(30.1, 40.0), 2)
                case "Mythical":
                    self.weight = round(random.uniform(40.1, 50.0), 2)
                case "Legendary":
                    self.weight = round(random.uniform(50.1, 60.0), 2)
                case "Trash":
                    self.weight = round(random.uniform(0.1, 0.9), 2)
                case _:
                    self.weight = 0.0
            return self.weight
        except Exception as e:
            print(f"Error calculating weight: {e}")
            return 0.0


class Player:
    """
    Represents a player in the fishing game.

    Attributes:
        user_id (int): The unique identifier for the player.
        money (int): The amount of money the player has.
        level (int): The current level of the player.
        league (str): The league the player belongs to based on their level.
    """
    def __init__(self, user_id: int, money: int = 0, level: int = 0, league: str = ""):
        """
        Initializes a Player instance.

        Args:
            user_id (int): The unique identifier for the player.
            money (int, optional): The amount of money the player has. Defaults to 0.
            level (int, optional): The current level of the player. Defaults to 0.
            league (str, optional): The league the player belongs to. Defaults to an empty string.
        """
        self.user_id = user_id
        self.money = money
        self.level = 0
        self.league = league

    def load_from_leaderboard(self) -> None:
        """
        Loads the player's data from the leaderboard file.
        Updates the player's attributes with data from the file.
        """
        try:
            with open(PLAYERS_PATH, "r") as file:
                players_data = json.load(file)
            for user in players_data["STATS"]:
                if user["user_id"] == self.user_id:
                    self.level = user["level"]
                    self.money = user["money"]
                    self.league = user["league"]
                    break
        except FileNotFoundError:
            print("Players stats file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file.")

    def level_check(self) -> None:
        """
        Determines and updates the player's league based on their level.
        The league is set according to predefined level thresholds.
        """
        try:
            match self.level:
                case level if 0 < level < 1000:
                    self.league = "Minnow"
                case level if 1000 <= level < 3000:
                    self.league = "Guppy"
                case level if 3000 <= level < 5000:
                    self.league = "Pond"
                case level if 5000 <= level < 10000:
                    self.league = "River"
                case level if 10000 <= level < 15000:
                    self.league = "Lake"
                case level if 15000 <= level < 20000:
                    self.league = "Stream"
                case level if 20000 <= level < 30000:
                    self.league = "Bay"
                case level if 30000 <= level < 40000:
                    self.league = "Ocean"
                case level if 40000 <= level < 50000:
                    self.league = "Deep Sea"
                case level if 50000 <= level < 70000:
                    self.league = "Trophy"
                case level if 70000 <= level < 100000:
                    self.league = "Champion"
                case level if level >= 100000:
                    self.league = "Legendary"
                case _:
                    self.league = "Unranked"
        except Exception as e:
            self.league = f"Error League not defined : {e}"

    def save_to_leaderboard(self) -> None:
        """
        Saves the player's current data to the leaderboard file.
        Creates a new file if it does not exist, and updates or adds the player's data.
        """
        # Check if the file exists
        if not os.path.isfile(PLAYERS_PATH):
            # Create an empty leaderboard if the file does not exist
            with open(PLAYERS_PATH, "w") as file:
                json.dump({"STATS": []}, file, indent=3)

        # Load existing leaderboard data
        with open(PLAYERS_PATH, "r") as file:
            players_data = json.load(file)

        new_entry = {
            "user_id": self.user_id,
            "money": self.money,
            "level": self.level,
            "league": self.league,
        }

        user_found = False
        for user in players_data["STATS"]:
            if user["user_id"] == self.user_id:
                # Update existing user's details
                user["money"] = self.money
                user["level"] = self.level
                user["league"] = self.league
                user_found = True
                break

        if not user_found:
            players_data["STATS"].append(new_entry)

        with open(PLAYERS_PATH, "w") as file:
            json.dump(players_data, file, indent=3)


def reset_fisher(player_tag: int, state: str) -> None | bool:
    """
    Resets a specific attribute of a player's data to zero.

    Args:
        player_tag (int): The unique identifier for the player.
        state (str): The attribute to reset (e.g., 'money', 'level').

    Returns:
        None or bool: Returns True if successful, None otherwise.
    """
    try:
        with open(PLAYERS_PATH, "r+") as file:
            players_data = json.load(file)
            for user in players_data["STATS"]:
                if user["user_id"] == player_tag:
                    if state.lower() == "money":
                        user["money"] = 0
                        break
                    elif state.lower() in ["level", "levels"]:
                        user["level"] = 0
                        break
                    else:
                        return None
            else:
                return None
            file.seek(0)
            json.dump(players_data, file, indent=3)
            file.truncate()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return None

def delete_player(player_tag: int) -> None | bool:
    """
    Deletes a player's data from the leaderboard file.

    Args:
        player_tag (int): The unique identifier for the player.

    Returns:
        None or bool: Returns True if successful, None otherwise.
    """
    try:
        with open(PLAYERS_PATH, "r+") as file:
            players_data = json.load(file)
            for user in players_data["STATS"]:
                if user["user_id"] == player_tag:
                    players_data["STATS"].remove(user)
                    break
            else:
                return None
            file.seek(0)
            json.dump(players_data, file, indent=3)
            file.truncate()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return None

def delete_all_players() -> None | bool:
    """
    Deletes all player data from the leaderboard file.

    Returns:
        None or bool: Returns True if successful, None otherwise.
    """
    try:
        with open(PLAYERS_PATH, "r+") as file:
            players_data = json.load(file)
            players_data["STATS"] = []  # Clear all player data

            file.seek(0)
            json.dump(players_data, file, indent=3)
            file.truncate()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return None


CATCHES = [
    # TRASH
    Loot(
        "Plastic Bag",
        "Trash",
        "A discarded plastic bag floating in the water.",
    ),
    Loot(
        "Old Shoe",
        "Trash",
        "An old, worn-out shoe that's been thrown into the water.",
    ),
    Loot(
        "Broken Bottle",
        "Trash",
        "A shattered glass bottle, lost and forgotten.",
    ),
    Loot(
        "Rusty Can",
        "Trash",
        "A rusty can, once holding something edible.",
    ),
    Loot(
        "Fishing Line",
        "Trash",
        "A tangled mess of old fishing line.",
    ),
    Loot(
        "Wooden Plank",
        "Trash",
        "A piece of driftwood, worn smooth by the water.",
    ),
    Loot(
        "Empty Can",
        "Trash",
        "An empty can, discarded and forgotten.",
    ),
    Loot(
        "Discarded Net",
        "Trash",
        "An old fishing net, tangled and useless.",
    ),
    Loot(
        "Torn Bag",
        "Trash",
        "A bag ripped apart and left to float.",
    ),
    Loot(
        "Worn Tire",
        "Trash",
        "A worn-out tire, floating aimlessly.",
    ),
    # COMMON
    Loot(
        "Goldfish",
        "Common",
        "A small, shiny goldfish. Commonly found in ponds.",
    ),
    Loot(
        "Bluegill",
        "Common",
        "A small, panfish with a blueish tint, found in freshwater lakes.",
    ),
    Loot(
        "Sunfish",
        "Common",
        "A small, colorful fish often found in ponds and lakes.",
    ),
    Loot(
        "Perch",
        "Common",
        "A striped fish found in lakes and rivers.",
    ),
    Loot(
        "Tilapia",
        "Common",
        "A freshwater fish known for its mild flavor.",
    ),
    Loot(
        "Carp",
        "Common",
        "A large fish found in many rivers and ponds.",
    ),
    Loot(
        "Bass",
        "Common",
        "A popular sport fish found in lakes and rivers.",
    ),
    Loot(
        "Trout",
        "Common",
        "A common fish found in clear, cold streams and rivers.",
    ),
    Loot(
        "Catfish",
        "Common",
        "A bottom-dwelling fish with whisker-like barbels.",
    ),
    Loot(
        "Pike",
        "Common",
        "A long, predatory fish found in freshwater lakes.",
    ),
    # UNCOMMON
    Loot(
        "Catfish",
        "Uncommon",
        "A large fish with a whiskery face. Often found in rivers.",
    ),
    Loot(
        "Largemouth Bass",
        "Uncommon",
        "A predatory fish known for its large mouth and fighting spirit.",
    ),
    Loot(
        "Walleye",
        "Uncommon",
        "A freshwater fish with large eyes, known for its sharp teeth.",
    ),
    Loot(
        "Smallmouth Bass",
        "Uncommon",
        "A fish known for its fighting ability and small mouth.",
    ),
    Loot(
        "Northern Pike",
        "Uncommon",
        "A predatory fish with sharp teeth and a long body.",
    ),
    Loot(
        "Paddlefish",
        "Uncommon",
        "A fish known for its long, paddle-like snout.",
    ),
    Loot(
        "Muskellunge",
        "Uncommon",
        "A large, elusive predator found in North American lakes.",
    ),
    Loot(
        "Steelhead Trout",
        "Uncommon",
        "A migratory fish known for its strength and fighting ability.",
    ),
    Loot(
        "Sauger",
        "Uncommon",
        "A fish closely related to the walleye, found in rivers and lakes.",
    ),
    Loot(
        "Lake Sturgeon",
        "Uncommon",
        "A prehistoric fish known for its bony plates and long lifespan.",
    ),
    # RARE
    Loot(
        "Rainbow Trout",
        "Rare",
        "A colorful trout with vibrant stripes. A rare catch in clear lakes.",
    ),
    Loot(
        "Arapaima",
        "Rare",
        "A giant fish native to the Amazon River, known for its size.",
    ),
    Loot(
        "Tiger Trout",
        "Rare",
        "A hybrid trout known for its striking pattern.",
    ),
    Loot(
        "Golden Dorado",
        "Rare",
        "A powerful predator with a golden sheen.",
    ),
    Loot(
        "Grouper",
        "Rare",
        "A large fish with a robust body, found in tropical waters.",
    ),
    Loot(
        "Rohu",
        "Rare",
        "A large freshwater fish native to South Asia.",
    ),
    Loot(
        "Napoleon Wrasse",
        "Rare",
        "A large, colorful fish found in the Indo-Pacific region.",
    ),
    Loot(
        "Red Drum",
        "Rare",
        "A prized fish known for its distinctive red coloration.",
    ),
    Loot(
        "Swordfish",
        "Rare",
        "A large fish known for its long, sword-like bill.",
    ),
    Loot(
        "Bluefin Tuna",
        "Rare",
        "A large, fast tuna known for its blue coloration and high value.",
    ),
    # EPIC
    Loot(
        "Goliath Grouper",
        "Epic",
        "A massive, intimidating fish. Known for its strength and size.",
    ),
    Loot(
        "Manta Ray",
        "Epic",
        "A large, graceful ray known for its wide wingspan.",
    ),
    Loot(
        "Giant Squid",
        "Epic",
        "A colossal squid known for its size and elusive nature.",
    ),
    Loot(
        "Koi Fish",
        "Epic",
        "A large ornamental fish known for its vibrant colors and patterns.",
    ),
    Loot(
        "Great White Shark",
        "Epic",
        "A formidable predator known for its size and power.",
    ),
    Loot(
        "Orca",
        "Epic",
        "A powerful marine mammal known for its intelligence and hunting skills.",
    ),
    Loot(
        "Hammerhead Shark",
        "Epic",
        "A shark known for its distinctive hammer-shaped head.",
    ),
    Loot(
        "Beluga Sturgeon",
        "Epic",
        "A rare sturgeon known for its large size and valuable caviar.",
    ),
    Loot(
        "Blue Marlin",
        "Epic",
        "A large, fast fish known for its impressive bill and fighting ability.",
    ),
    Loot(
        "Megalodon Tooth",
        "Epic",
        "A fossilized tooth from the ancient and massive Megalodon shark.",
    ),
    # SUPREME
    Loot(
        "BoomFish",
        "Supreme",
        "BadaBOOOM.",
    ),
    Loot(
        "Electra",
        "Supreme",
        "A mythical fish said to harness the power of lightning.",
    ),
    Loot(
        "Inferno Fish",
        "Supreme",
        "A fish that supposedly burns with the fire of a thousand suns.",
    ),
    Loot(
        "Frost Dragon Fish",
        "Supreme",
        "A fish from the icy realms, known for its freezing breath.",
    ),
    Loot(
        "Celestial Koi",
        "Supreme",
        "A koi with scales that sparkle like the night sky.",
    ),
    Loot(
        "Tornado Fish",
        "Supreme",
        "A fish said to create whirlwinds in the water.",
    ),
    Loot(
        "Vortex Eel",
        "Supreme",
        "An eel known for its ability to create whirlpools.",
    ),
    Loot(
        "Phantom Ray",
        "Supreme",
        "A ray that appears and disappears like a ghost.",
    ),
    Loot(
        "Storm Shark",
        "Supreme",
        "A shark known to accompany thunderstorms.",
    ),
    Loot(
        "Phoenix Fish",
        "Supreme",
        "A mythical fish said to rise from the ashes.",
    ),
    # MYTHICAL
    Loot(
        "Diamond Fish",
        "Mythical",
        "That is Pricy.",
    ),
    Loot(
        "Leviathan",
        "Mythical",
        "A colossal sea creature from ancient legends.",
    ),
    Loot(
        "Kraken",
        "Mythical",
        "A giant squid-like creature feared by sailors.",
    ),
    Loot(
        "Hydra",
        "Mythical",
        "A multi-headed serpent with regenerative abilities.",
    ),
    Loot(
        "Triton's Trident Fish",
        "Mythical",
        "A fish said to be blessed by the god of the sea.",
    ),
    Loot(
        "Mermaid's Tear",
        "Mythical",
        "A gem said to be the tear of a mermaid, found in the sea.",
    ),
    Loot(
        "Eldritch Whale",
        "Mythical",
        "A whale from deep, dark corners of the ocean.",
    ),
    Loot(
        "Abyssal Fish",
        "Mythical",
        "A fish from the deepest, darkest depths of the sea.",
    ),
    Loot(
        "Celestial Jellyfish",
        "Mythical",
        "A glowing jellyfish said to be a gift from the stars.",
    ),
    Loot(
        "Astral Shark",
        "Mythical",
        "A shark with a celestial pattern across its body.",
    ),
    # LEGENDARY
    Loot(
        "Dragonfish",
        "Legendary",
        "A mythical fish with scales that shimmer like dragon scales. Extremely rare and valuable.",
    ),
    Loot(
        "Kraken",
        "Legendary",
        "A legendary sea monster known for its immense size and power.",
    ),
    Loot(
        "Poseidon's Trident",
        "Legendary",
        "A powerful trident said to be wielded by the god of the sea.",
    ),
    Loot(
        "Phoenix Fish",
        "Legendary",
        "A fish that rises from the ashes, said to bring good fortune.",
    ),
    Loot(
        "Leviathan",
        "Legendary",
        "An ancient sea creature of immense size and strength.",
    ),
    Loot(
        "Golden Sea Serpent",
        "Legendary",
        "A rare and majestic sea serpent covered in golden scales.",
    ),
    Loot(
        "Eldritch Kraken",
        "Legendary",
        "A monstrous kraken from the darkest depths of the ocean.",
    ),
    Loot(
        "Celestial Dragonfish",
        "Legendary",
        "A dragonfish with celestial powers and a mythical aura.",
    ),
    Loot(
        "Titanic Shark",
        "Legendary",
        "An enormous shark that rules the oceans with unmatched strength.",
    ),
    Loot(
        "Mystic Mermaid",
        "Legendary",
        "A mythical mermaid with unparalleled beauty and magical abilities.",
    ),
]

def fishing(catches: list) -> Loot:
    """
    Selects a loot item based on probability.

    Args:
        catches (list): List of Loot objects to choose from.

    Returns:
        Loot: A randomly selected loot item based on rarity probabilities.
    """
    # Calculate total probability
    total_prob = sum(RARITY_PROBABILITIES.values())

    # Ensure the total probability sums to 1
    assert abs(total_prob - 1.0) < 1e-6, "Total probability does not sum to 1."

    # Generate a random number to select rarity
    rand = random.random()

    # Determine the rarity based on the random number
    cumulative_prob = 0.0
    for rarity, prob in RARITY_PROBABILITIES.items():
        cumulative_prob += prob
        if rand < cumulative_prob:
            selected_rarity = rarity
            break

    # Filter catches by selected rarity
    filtered_catches = [loot for loot in catches if loot.rarity == selected_rarity]

    if filtered_catches != []:
        return random.choice(filtered_catches)
    else:
        print("No catch matches the selected rarity.")
        return None


def sort_leaderboard(state: str) -> list:
    """
    Sorts the leaderboard based on a specified attribute.

    Args:
        state (str): The attribute to sort by (e.g., 'money', 'level').

    Returns:
        list: A sorted list of player data.
    """
    with open(PLAYERS_PATH, "r") as file:
        players_data = json.load(file)
    leaderboard_list = []
    # Extract and sort the leaderboard by money in descending order
    if state.lower() == "money":
        for user in players_data["STATS"]:
            leaderboard_list.append([user["user_id"], user["money"]])
        leaderboard_list.sort(key=lambda x: x[1], reverse=True)
    # Extract and sort the leaderboard by level in descending order
    elif state.lower() in ["level", "levels"]:
        for user in players_data["STATS"]:
            leaderboard_list.append([user["user_id"], user["level"]])
        leaderboard_list.sort(key=lambda x: x[1], reverse=True)

    return leaderboard_list
