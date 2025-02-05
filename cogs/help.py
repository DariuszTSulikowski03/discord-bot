# cogs/help.py
import discord
from discord.ext import commands

class HelpCog(commands.Cog, name="Pomoc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Wyświetla pomoc dotyczącą komend bota."
    )
    async def help(self, ctx, command: str = None):
        if command:
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"Pomoc - {cmd.name}",
                    description=cmd.help or "Brak dodatkowych informacji.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Nie znaleziono komendy.")
        else:
            embed = discord.Embed(title="Lista Komend", color=discord.Color.green())
            for cog_name, cog in self.bot.cogs.items():
                commands_list = "\n".join([f"!{cmd.name} - {cmd.help}" for cmd in cog.get_commands() if not cmd.hidden])
                if commands_list:
                    embed.add_field(name=cog_name, value=commands_list, inline=False)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

