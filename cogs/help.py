import discord
from discord.ext import commands

class HelpCog(commands.Cog, name="Pomoc"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Wyświetla listę dostępnych komend")
    async def help(self, ctx):
        embed = discord.Embed(title="Lista komend", color=discord.Color.green())
        
        for cog_name, cog in self.bot.cogs.items():
            cmds = cog.get_commands()
            if cmds:
                command_list = "\n".join([f"**!{cmd.name}** - {cmd.help}" for cmd in cmds if not cmd.hidden])
                embed.add_field(name=cog_name, value=command_list, inline=False)
        
        embed.set_footer(text="Wpisz !help [komenda] by zobaczyć szczegóły")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
