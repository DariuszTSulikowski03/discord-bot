import discord
from discord.ext import commands
import os
from utils import load_config
from database import Database
import logging

# Load bot configuration from config.json
CONFIG = load_config()
TOKEN = CONFIG.get("BOT_TOKEN")
PREFIX = CONFIG.get("PREFIX", "!")

# Define bot intents (message_content is required; members intent for ranking)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=PREFIX, intents=intents, **kwargs)
        self.db = None  # This will hold the database connection

    async def setup_hook(self):
        # Dynamically load all cogs from the "cogs" directory
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    logging.info(f"Loaded cog: {filename}")
                except Exception as e:
                    logging.error(f"Failed to load cog {filename}: {e}")

        # Initialize the database connection
        self.db = await Database.create("tournament.db")
        logging.info("Database initialized.")

    async def on_ready(self):
        print(f"{self.user.name} is now online!")
        await self.change_presence(activity=discord.Game(name="Managing the server"))

bot = CustomBot()

@bot.command()
async def reload(ctx, cog: str):
    """Reloads a specific cog dynamically."""
    try:
        await bot.unload_extension(f"cogs.{cog}")
        await bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded {cog} successfully!")
    except Exception as e:
        await ctx.send(f"Failed to reload {cog}: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
