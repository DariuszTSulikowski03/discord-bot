import discord
from discord.ext import commands
import logging

class AdminTools(commands.Cog, name="Narzędzia Administracyjne"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="podsumowanie", help="Pokazuje statystyki turnieju")
    @commands.has_permissions(administrator=True)
    async def championship_stats(self, ctx):
        total_users = len(self.bot.user_points)
        total_points = sum(self.bot.user_points.values())
        avg_points = total_points / total_users if total_users else 0
        
        embed = discord.Embed(title="Podsumowanie Turnieju", color=discord.Color.gold())
        embed.add_field(name="Uczestnicy", value=total_users)
        embed.add_field(name="Łączna liczba punktów", value=total_points)
        embed.add_field(name="Średnia punktów", value=f"{avg_points:.2f}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminTools(bot))
