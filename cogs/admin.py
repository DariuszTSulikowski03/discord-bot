# cogs/admin.py
import discord
from discord.ext import commands
from utils import *
import logging

class AdminTools(commands.Cog, name="Narzędzia Administracyjne"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="podsumowanie",
        description="Pokazuje statystyki mistrzostw"
    )
    @commands.has_permissions(administrator=True)
    async def championship_stats(self, ctx):
        stats = get_championship_stats()
        
        embed = discord.Embed(
            title="📈 Statystyki Mistrzostw",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Ogólne",
            value=f"```Łączne zgłoszenia: {stats['total_submissions']}\n"
                  f"Średnia punktów/dzień: {stats['avg_daily']}\n"
                  f"Największy skok: +{stats['biggest_jump']}```",
            inline=False
        )
        
        embed.add_field(
            name="Top Typers",
            value="\n".join(
                f"{idx}. {user['name']} ({user['points']})" 
                for idx, user in enumerate(stats['top3'], 1)
            ),
            inline=True
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminTools(bot))
