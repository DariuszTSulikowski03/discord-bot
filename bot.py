# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import pytz

# Load environment variables from .env
load_dotenv()

# Configure logging (you can adjust the level and format as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class CustomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required for accessing message content
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,  # We'll create custom help commands in our cogs if needed
            case_insensitive=True
        )
        self.warsaw_tz = pytz.timezone('Europe/Warsaw')
        self.start_time = discord.utils.utcnow()

# Instantiate the bot
bot = CustomBot()

@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} gotowy do działania!")
    # Sync slash commands (if using hybrid commands)
    await bot.tree.sync()

if __name__ == "__main__":
    # List of cogs (extensions) to load
    initial_extensions = [
        'cogs.championship',
        'cogs.admin'
    ]
    
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logging.info(f"Załadowano moduł: {extension}")
        except Exception as e:
            logging.error(f"Błąd przy ładowaniu {extension}: {e}")

    # Run the bot using the token from the .env file
    bot.run(os.getenv("DISCORD_TOKEN"))
