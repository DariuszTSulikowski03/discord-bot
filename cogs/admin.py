from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admin_test")
    async def admin_test(self, ctx):
        await ctx.send("✅ Komenda administracyjna działa!")

async def setup(bot):
    await bot.add_cog(Admin(bot))
