# cogs/odds.py
import discord
from discord.ext import commands
import requests
import os
import logging
from urllib.parse import urlparse, parse_qs, unquote

class OddsCog(commands.Cog, name="The Odds API"):
    def __init__(self, bot):
        self.bot = bot
        # Read API key from environment variable or use the provided key
        self.api_key = os.getenv("ODDS_API_KEY", "f0d255b08cbae82066c2c9dc2aae73d2")
        self.base_url = "https://api.the-odds-api.com/v4/sports"
    
    @commands.hybrid_command(
        name="odds",
        description="Wyświetla dostępne sporty lub kursy dla wybranego sportu."
    )
    async def odds(self, ctx, sport: str = None):
        if sport is None:
            # List available sports
            url = f"{self.base_url}?apiKey={self.api_key}"
            response = requests.get(url)
            if response.status_code != 200:
                await ctx.send("Nie udało się pobrać listy sportów. Spróbuj ponownie później.")
                return
            data = response.json()
            if not data:
                await ctx.send("Brak dostępnych sportów.")
                return
            embed = discord.Embed(title="Dostępne sporty", color=discord.Color.green())
            for item in data:
                name = item.get("title", "Brak nazwy")
                key = item.get("key", "brak")
                embed.add_field(name=name, value=f"Klucz: `{key}`", inline=False)
            await ctx.send(embed=embed)
        else:
            # Fetch odds for the given sport
            # Default parameters: regions=eu, markets=h2h, oddsFormat=decimal
            url = f"{self.base_url}/{sport}/odds/?apiKey={self.api_key}&regions=eu&markets=h2h&oddsFormat=decimal"
            response = requests.get(url)
            if response.status_code != 200:
                await ctx.send("Nie udało się pobrać kursów dla wybranego sportu. Upewnij się, że klucz sportu jest poprawny.")
                return
            data = response.json()
            if not data:
                await ctx.send("Brak danych o kursach dla tego sportu.")
                return
            embed = discord.Embed(title=f"Kursy dla sportu: {sport}", color=discord.Color.blue())
            # List the first few events for brevity
            for event in data[:5]:
                home_team = event.get("home_team", "Nieznany")
                away_team = event.get("away_team", "Nieznany")
                odds_str = ""
                # For each bookmaker, try to retrieve h2h market odds
                for bookmaker in event.get("bookmakers", []):
                    bookmaker_name = bookmaker.get("title", "Nieznany bukmacher")
                    for market in bookmaker.get("markets", []):
                        if market.get("key") == "h2h":
                            outcomes = market.get("outcomes", [])
                            outcomes_str = ", ".join([f"{o.get('name')}: {o.get('price')}" for o in outcomes])
                            odds_str += f"{bookmaker_name}: {outcomes_str}\n"
                if not odds_str:
                    odds_str = "Brak kursów"
                embed.add_field(name=f"{home_team} vs {away_team}", value=odds_str, inline=False)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OddsCog(bot))

