from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Displays the help message."""
        help_message = """
**Available Commands:**
- `!ping` - Check bot latency
- `!start_tournament` - Start a tournament
- `!shutdown` - Shutdown the bot
- `!resetranking` - Reset ranking for all users (Admin)
- `!dodajpunkty <user> <points>` - Adjust points for a user (Admin)
- `!ranking [page]` - Display the tournament ranking
- `!reload <cog>` - Reload a specific cog
"""
        await ctx.send(help_message)

async def setup(bot):
    await bot.add_cog(Help(bot))
