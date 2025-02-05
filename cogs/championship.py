# cogs/championship.py
import discord
from discord.ext import commands
import datetime

# In-memory storage for this simple version
user_points = {}         # Maps user ID to total points
daily_submissions = {}   # Maps user ID to the date of last coupon submission

def calculate_points(bet_type: str, odds: float, amount: float) -> int:
    bet_type = bet_type.lower()
    if bet_type == "solo":
        multiplier = 2 if odds > 10.0 else 1
    elif bet_type == "ako":
        multiplier = 5 if odds > 10.0 else 2.5
    else:
        multiplier = 1
    return int(amount * multiplier)

class Championship(commands.Cog, name="Turniej"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kupon", help="Dodaje zgłoszenie kuponu. Użyj: !kupon [punkty] [link]")
    async def kupon(self, ctx, punkty: int, link: str):
        # Sprawdź, czy użytkownik ma rolę "Zweryfikowany"
        if not any(role.name == "Zweryfikowany" for role in ctx.author.roles):
            await ctx.send("Nie masz wymaganej roli 'Zweryfikowany'!")
            return

        # Sprawdź, czy użytkownik już wysłał kupon dzisiaj
        today = datetime.date.today()
        if ctx.author.id in daily_submissions and daily_submissions[ctx.author.id] == today:
            await ctx.send("Masz już zgłoszony kupon na dzisiaj!")
            return

        # Dodaj podane punkty do wyniku użytkownika
        user_points[ctx.author.id] = user_points.get(ctx.author.id, 0) + punkty
        daily_submissions[ctx.author.id] = today

        await ctx.send(f"Kupon przyjęty! Dodano {punkty} punktów. Twój łączny wynik: {user_points[ctx.author.id]} punktów.")

    @commands.command(name="ranking", help="Wyświetla aktualny ranking punktowy.")
    async def ranking(self, ctx):
        if not user_points:
            await ctx.send("Ranking jest pusty.")
            return

        # Sortowanie użytkowników wg punktów malejąco
        sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="Ranking punktowy", color=discord.Color.gold())
        for idx, (user_id, points) in enumerate(sorted_users, start=1):
            user = self.bot.get_user(user_id)
            display_name = user.display_name if user else f"Użytkownik {user_id}"
            embed.add_field(name=f"#{idx}", value=f"{display_name}: {points} punktów", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="kalkulator", help="Oblicza punkty. Użyj: !kalkulator [typ] [odds] [kwota]\nPrzykład: !kalkulator AKO 11.0 50")
    async def kalkulator(self, ctx, typ: str, odds: float, kwota: float):
        points = calculate_points(typ, odds, kwota)
        await ctx.send(f"Obliczone punkty: {points} punktów.")

def setup(bot):
    bot.add_cog(Championship(bot))
