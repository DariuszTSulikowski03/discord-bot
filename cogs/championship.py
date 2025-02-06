from discord.ext import commands

class Championship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start_tournament(self, ctx):
        """Starts a tournament."""
        await ctx.send("Tournament started!")

async def setup(bot):
    await bot.add_cog(Championship(bot))
