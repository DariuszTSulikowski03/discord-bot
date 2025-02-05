import discord
from discord.ext import commands
import logging

class ControlCog(commands.Cog, name="Zaawansowana kontrola"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", help="Wyłącza bota. [Właściciel]")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Wyłączam bota...")
        await self.bot.close()

    @commands.command(name="reload", help="Przeładowuje wskazany moduł (cog). [Właściciel]\nUżycie: !reload [nazwa_modulu]")
    @commands.is_owner()
    async def reload(self, ctx, cog: str = None):
        if not cog:
            await ctx.send("Podaj nazwę modułu do przeładowania.")
            return

        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Moduł {cog} został przeładowany.")
        except Exception as e:
            await ctx.send(f"Błąd podczas przeładowania modułu {cog}: {e}")

    @commands.command(name="status", help="Wyświetla status bota. [Właściciel]")
    @commands.is_owner()
    async def status(self, ctx):
        uptime = discord.utils.utcnow() - self.bot.start_time
        embed = discord.Embed(title="Status Bota", color=discord.Color.blurple())
        embed.add_field(name="Czas pracy", value=str(uptime), inline=False)
        embed.add_field(name="Liczba serwerów", value=len(self.bot.guilds), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ControlCog(bot))
