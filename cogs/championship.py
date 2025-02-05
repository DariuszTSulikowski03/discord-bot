import discord
from discord.ext import commands
from datetime import datetime
import pytz
from utils import calculate_points

class Championship(commands.Cog, name="Turniej"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Brakuje wymaganego argumentu. Użyj !kupon [punkty] [link]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Nieprawidłowy argument. Upewnij się, że punkty są liczbą całkowitą.")
        else:
            await ctx.send(f"Wystąpił błąd: {error}")

    @commands.command(name="kupon", help="Dodaje zgłoszenie kuponu")
    async def kupon(self, ctx, punkty: int, *, link: str):
        REQUIRED_ROLE = "Zweryfikowany"
        if not any(role.name == REQUIRED_ROLE for role in ctx.author.roles):
            await ctx.send(f"Nie masz wymaganej roli '{REQUIRED_ROLE}'!")
            return

        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        warsaw_time = now_utc.astimezone(self.bot.warsaw_tz)
        today = warsaw_time.date()

        if ctx.author.id in self.bot.daily_submissions and self.bot.daily_submissions[ctx.author.id] == today:
            await ctx.send("Masz już zgłoszony kupon na dzisiaj!")
            return

        self.bot.user_points[ctx.author.id] = self.bot.user_points.get(ctx.author.id, 0) + punkty
        self.bot.daily_submissions[ctx.author.id] = today

        await ctx.send(f"Kupon przyjęty! Dodano {punkty} punktów.")

    @commands.command(name="ranking", help="Wyświetla aktualny ranking punktowy")
    async def ranking(self, ctx):
        sorted_users = sorted(self.bot.user_points.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(title="Ranking Punktowy", color=discord.Color.blue())
        for idx, (user_id, points) in enumerate(sorted_users[:10], 1):
            user = self.bot.get_user(user_id)
            name = user.display_name if user else "Nieznany użytkownik"
            embed.add_field(name=f"{idx}. {name}", value=f"{points} punktów", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="kalkulator", help="Oblicza punkty wg zasad")
    async def kalkulator(self, ctx, typ: str, odds: float, kwota: float):
        punkty = calculate_points(typ, odds, kwota)
        await ctx.send(f"**Kalkulator punktów**\n"
                       f"Typ: {typ}\n"
                       f"Kurs: {odds}\n"
                       f"Kwota: {kwota}\n"
                       f"**Wynik:** {punkty} punktów")

async def setup(bot):
    await bot.add_cog(Championship(bot))
