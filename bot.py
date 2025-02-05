# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import pytz

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class CustomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading message content
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,  # We'll use our custom help command from cogs/help.py
            case_insensitive=True
        )
        self.warsaw_tz = pytz.timezone('Europe/Warsaw')
        self.start_time = discord.utils.utcnow()

bot = CustomBot()

@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} gotowy do działania!")
    # Sync slash commands if hybrid commands are used
    await bot.tree.sync()

if __name__ == "__main__":
    initial_extensions = [
        'cogs.championship',
        'cogs.admin',
        'cogs.help',
        'cogs.odds'  # New: integration with The Odds API
    ]
    
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logging.info(f"Załadowano moduł: {extension}")
        except Exception as e:
            logging.error(f"Błąd przy ładowaniu {extension}: {e}")

    bot.run(os.getenv("DISCORD_TOKEN"))
