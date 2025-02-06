from discord.ext import commands

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self, ctx):
        """Shuts down the bot."""
        await ctx.send("Shutting down...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Control(bot))
