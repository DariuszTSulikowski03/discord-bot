# cogs/help.py
import discord
from discord.ext import commands

class HelpCog(commands.Cog, name="Pomoc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Wyświetla listę dostępnych komend. Podaj nazwę komendy, aby uzyskać szczegóły.")
    async def help(self, ctx, command_name: str = None):
        if command_name:
            cmd = self.bot.get_command(command_name)
            if cmd:
                embed = discord.Embed(
                    title=f"Pomoc - {cmd.name}",
                    description=cmd.help or "Brak dodatkowych informacji.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Nie znaleziono takiej komendy.")
        else:
            embed = discord.Embed(title="Lista komend", color=discord.Color.green())
            for cog_name, cog in self.bot.cogs.items():
                cmds = cog.get_commands()
                if cmds:
                    command_list = "\n".join([f"!{cmd.name} - {cmd.help}" for cmd in cmds if not cmd.hidden])
                    embed.add_field(name=cog_name, value=command_list, inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
