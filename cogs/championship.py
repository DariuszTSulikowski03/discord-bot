from discord.ext import commands

class Championship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="championship_test")
    async def championship_test(self, ctx):
        await ctx.send("✅ Komenda mistrzostw działa!")

async def setup(bot):
    await bot.add_cog(Championship(bot))
