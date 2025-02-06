import discord
from discord.ext import commands
from datetime import datetime
import re

class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kupon", help="Dodaj kupon i zdobywaj punkty.")
    @commands.has_role("zweryfikowany")
    async def coupon(self, ctx, points: int, link: str):
        """Allows a verified user to submit a coupon once per day with automatic point calculation."""
        user_id = ctx.author.id
        today = datetime.utcnow().date()

        # Check if user already submitted today
        last_submission = await self.bot.db.fetchone("SELECT last_submission FROM users WHERE user_id = ?", user_id)

        if last_submission and last_submission[0]:
            last_submission_date = datetime.strptime(last_submission[0], "%Y-%m-%d").date()
            if last_submission_date == today:
                return await ctx.send("⛔ Możesz zgłosić kupon **tylko raz dziennie**!")

        # Automatic point calculation based on bet type
        bet_type, multiplier = self.calculate_points(points, link)

        if not bet_type:
            return await ctx.send("❌ Nie udało się rozpoznać typu zakładu. Sprawdź link!")

        total_points = int(points * multiplier)

        # Update or insert points
        existing_user = await self.bot.db.fetchone("SELECT points FROM users WHERE user_id = ?", user_id)

        if existing_user:
            new_points = existing_user[0] + total_points
            await self.bot.db.execute("UPDATE users SET points = ?, last_submission = ? WHERE user_id = ?", new_points, today, user_id)
        else:
            await self.bot.db.execute("INSERT INTO users (user_id, points, last_submission) VALUES (?, ?, ?)", user_id, total_points, today)

        await ctx.send(f"✅ {ctx.author.mention} dodał kupon **{bet_type}**, zdobywając **{total_points} pkt**! [Kupon]({link})")

    def calculate_points(self, amount, link):
        """Determine bet type and point multiplier."""
        odds = self.extract_odds_from_link(link)
        if not odds:
            return None, None

        if "solo" in link.lower():
            return "SOLO", 2.0 if odds > 10.0 else 1.0
        elif "ako" in link.lower():
            return "AKO", 5.0 if odds > 10.0 else 2.5
        return None, None

    def extract_odds_from_link(self, link):
        """Extract odds from the provided link (mock function)."""
        match = re.search(r"odds=(\d+\.\d+)", link)
        return float(match.group(1)) if match else None

async def setup(bot):
    await bot.add_cog(RankingCog(bot))
