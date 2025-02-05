import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import pytz
import asyncio

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
        self.user_points = {}
        self.daily_submissions = {}

bot = CustomBot()

@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} gotowy do działania!")
    # Sync the app commands (if you're using them)
    await bot.tree.sync()

async def main():
    initial_extensions = [
        'cogs.championship',
        'cogs.help',
        # Uncomment or remove the following line if you have (or do not have) a control cog
        # 'cogs.control',
        'cogs.admin'
    ]
    
    async with bot:
        # Load each extension asynchronously
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                logging.info(f"Załadowano moduł: {extension}")
            except Exception as e:
                logging.error(f"Błąd przy ładowaniu {extension}: {e}")
        # Start the bot with the provided token
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
