import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import pytz

load_dotenv()

class CustomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        self.warsaw_tz = pytz.timezone('Europe/Warsaw')
        self.start_time = discord.utils.utcnow()

bot = CustomBot()

@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} gotowy do działania!")
    await bot.tree.sync()

if __name__ == "__main__":
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

    bot.run(os.getenv("DISCORD_TOKEN"))
