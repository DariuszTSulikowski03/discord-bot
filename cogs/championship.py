# cogs/championship.py
import discord
from discord.ext import commands
from utils import (
    error_embed,
    get_last_submission,
    is_same_day,
    parse_coupon_link,
    calculate_points,
    save_submission,
    get_user_rank,
    count_daily_submissions,
    get_user_profile
)
from datetime import datetime
import re
import logging

class Championship(commands.Cog, name="Mistrzostwa Typerskie"):
    def __init__(self, bot):
        self.bot = bot
        # Channel where submissions are accepted
        self.submission_channel = "mistrzostwa-typerskie"
        # Role required to submit
        self.required_role = "Zweryfikowany"
        # Map bet types to emoji for a better UI
        self.emoji_map = {
            "solo": "⚔️",
            "ako": "🎯"
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots and those not in the submission channel
        if message.author.bot or message.channel.name != self.submission_channel:
            return

        # Validate the message format: expected "[punkty] | [link]"
        if not re.match(r'^\d+ \| https?://\S+', message.content):
            await message.delete()
            await error_embed(message.channel, 
                "**Nieprawidłowy format!**\nPoprawny format: `[punkty] | [link]`\nPrzykład: `250 | https://example.com`")
            return

        # Check if the user meets role and daily submission requirements
        if not await self.check_requirements(message):
            return

        # Process the submission message
        try:
            points_str, link = message.content.split('|', 1)
            declared_points = int(points_str.strip())
        except Exception as e:
            logging.error(f"Błąd przy rozdzielaniu zgłoszenia: {e}")
            await error_embed(message.channel, "Błąd przetwarzania formatu zgłoszenia.")
            return

        result = await self.process_submission(message.author, link.strip(), declared_points)
        
        if result['status'] == 'success':
            await self.send_success(message, result)
        else:
            await error_embed(message.channel, result['message'])

    async def check_requirements(self, message):
        # Verify the user has the required role
        if not any(role.name == self.required_role for role in message.author.roles):
            await error_embed(message.channel, 
                f"Wymagana rola **{self.required_role}** do uczestnictwa!")
            return False

        # Verify the user has not already submitted today
        last_sub = get_last_submission(message.author.id)
        if last_sub and is_same_day(last_sub, datetime.now(self.bot.warsaw_tz)):
            await error_embed(message.channel,
                "**Dzienny limit!**\nMożesz wysłać tylko jeden kupon dzisiaj!")
            return False

        return True

    async def process_submission(self, user, link, declared_points):
        try:
            # Parse the coupon data from the link (e.g., decoding JWT)
            coupon_data = parse_coupon_link(link)
            if not coupon_data:
                return {'status': 'error', 'message': 'Nieprawidłowy link do kuponu!'}

            # Calculate the points based on the coupon data
            calculated_points = calculate_points(
                coupon_data['amount_won'],
                coupon_data['odds'],
                coupon_data['bet_type']
            )

            # Verify the declared points roughly match the calculated ones (tolerance of 50 points)
            if abs(declared_points - calculated_points) > 50:
                return {'status': 'error', 'message': 'Niezgodność punktów! Sprawdź obliczenia.'}

            # Save the submission to the database
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
            logging.error(f"Błąd przetwarzania zgłoszenia: {e}")
            return {'status': 'error', 'message': 'Wewnętrzny błąd systemu!'}

    async def send_success(self, message, result):
        # Create an embed to confirm a successful submission
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
        
        # Create a progress bar toward a reward (example threshold: 5000 points)
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
