# cogs/championship.py
import discord
from discord.ext import commands
from utils import *
from datetime import datetime
import re
import logging

class Championship(commands.Cog, name="Mistrzostwa Typerskie"):
    def __init__(self, bot):
        self.bot = bot
        self.submission_channel = "mistrzostwa-typerskie"
        self.required_role = "Zweryfikowany"
        self.emoji_map = {
            "solo": "⚔️",
            "ako": "🎯"
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.name != self.submission_channel:
            return

        # Walidacja podstawowa
        if not re.match(r'^\d+ \| https?://\S+', message.content):
            await message.delete()
            return await error_embed(message.channel, 
                "**Nieprawidłowy format!**\nPoprawny format: `[punkty] | [link]`\nPrzykład: `250 | https://example.com`")

        # Sprawdzenie uprawnień
        if not await self.check_requirements(message):
            return

        # Przetwarzanie zgłoszenia
        points, link = message.content.split('|', 1)
        result = await self.process_submission(message.author, link.strip(), int(points.strip()))
        
        if result['status'] == 'success':
            await self.send_success(message, result)
        else:
            await error_embed(message.channel, result['message'])

    async def check_requirements(self, message):
        # Sprawdzenie roli
        if not any(role.name == self.required_role for role in message.author.roles):
            await error_embed(message.channel, 
                f"Wymagana rola **{self.required_role}** do uczestnictwa!")
            return False

        # Limit dzienny
        last_sub = get_last_submission(message.author.id)
        if last_sub and is_same_day(last_sub, datetime.now(self.bot.warsaw_tz)):
            await error_embed(message.channel,
                "**Dzienny limit!**\nMożesz wysłać tylko jeden kupon dziennie!")
            return False

        return True

    async def process_submission(self, user, link, declared_points):
        try:
            # Dekodowanie kuponu
            coupon_data = parse_coupon_link(link)
            if not coupon_data:
                return {'status': 'error', 'message': 'Nieprawidłowy link do kuponu!'}

            # Obliczanie punktów
            calculated_points = calculate_points(
                coupon_data['amount_won'],
                coupon_data['odds'],
                coupon_data['bet_type']
            )

            # Weryfikacja zgodności
            if abs(declared_points - calculated_points) > 50:
                return {'status': 'error', 'message': 'Niezgodność punktów! Sprawdź obliczenia.'}

            # Zapis do bazy
            save_submission(
                user_id=user.id,
                username=user.display_name,
                points=calculated_points,
                bet_type=coupon_data['bet_type'],
                odds=coupon_data['odds']
            )

            return {
                'status': 'success',
                'points': calculated_points,
                'bet_type': coupon_data['bet_type']
            }

        except Exception as e:
            logging.error(f"Błąd przetwarzania: {e}")
            return {'status': 'error', 'message': 'Wewnętrzny błąd systemu!'}

    async def send_success(self, message, result):
        embed = discord.Embed(
            title=f"✅ Kupon zaakceptowany! {self.emoji_map.get(result['bet_type'], '')}",
            color=discord.Color.green(),
            description=f"**{message.author.display_name}** zdobywa:\n"
                        f"```🪙 {result['points']} punktów!```"
        )
        
        embed.add_field(
            name="Aktualna pozycja",
            value=f"```🏆 #{get_user_rank(message.author.id)} w rankingu```",
            inline=True
        )
        
        embed.add_field(
            name="Dzienne statystyki",
            value=f"```📅 {count_daily_submissions()} zgłoszeń dziś```",
            inline=True
        )

        embed.set_footer(text="Zobacz pełny ranking komendą !topka")
        await message.channel.send(embed=embed)
        await message.add_reaction("🎉")

    @commands.hybrid_command(
        name="profil",
        description="Pokazuje twój profil zawodnika"
    )
    async def show_profile(self, ctx):
        user_data = get_user_profile(ctx.author.id)
        
        embed = discord.Embed(
            title=f"📊 Profil {ctx.author.display_name}",
            color=ctx.author.color
        )
        
        # Pasek postępu
        progress = user_data['points'] / 5000 * 100
        progress_bar = f"```css\n[{'█' * int(progress//5)}{' ' * (20 - int(progress//5))}] {user_data['points']}/5000```"
        
        embed.add_field(
            name="Postęp do nagrody",
            value=progress_bar,
            inline=False
        )
        
        embed.add_field(
            name="📨 Zgłoszenia",
            value=f"```Łącznie: {user_data['submissions']}\nŚrednio: {user_data['avg_points']}/dzień```",
            inline=True
        )
        
        embed.add_field(
            name="🏅 Osiągnięcia",
            value="\n".join(f"• {ach}" for ach in user_data['achievements'][:3]),
            inline=True
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Championship(bot))
