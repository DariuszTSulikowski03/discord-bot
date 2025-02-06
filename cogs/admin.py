import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name="resetranking", help="Reset ranking for all users")
    @commands.has_permissions(administrator=True)
    async def reset_ranking(self, ctx):
        await self.bot.db.execute('UPDATE users SET points = 0, submissions = 0')
        await ctx.send("✅ Ranking has been reset!")

    @commands.command(name="dodajpunkty", help="Adjust points for a specific user")
    @commands.has_permissions(administrator=True)
    async def adjust_points(self, ctx, user: discord.Member, points: int):
        await self.bot.db.execute('''
            UPDATE users 
            SET points = points + ?, submissions = submissions + 1 
            WHERE user_id = ?
        ''', points, user.id)
        await ctx.send(f"✅ Updated points for {user.display_name}. Adjustment: {points}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
