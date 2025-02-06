import discord
from discord.ext import commands
from discord.ui import Button, View

class Paginator(View):
    def __init__(self, pages, timeout=60):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.current_page = 0

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.pages[self.current_page])

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.pages[self.current_page])

class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_top_users(self, limit=20, offset=0):
        return await self.bot.db.fetchall('''
            SELECT user_id, points, submissions 
            FROM users 
            ORDER BY points DESC 
            LIMIT ? OFFSET ?
        ''', limit, offset)

    @commands.command(name="ranking", help="Displays the extended tournament ranking")
    async def ranking(self, ctx, page: int = 1):
        per_page = 20
        offset = (page - 1) * per_page
        total_users_result = await self.bot.db.fetchone('SELECT COUNT(*) FROM users')
        total_users = total_users_result[0] if total_users_result else 0
        total_pages = (total_users + per_page - 1) // per_page if total_users else 1

        if page < 1 or page > total_pages:
            return await ctx.send("❌ Invalid page number!")

        # Build paginated embeds for each page
        pages = []
        for i in range(total_pages):
            embed = discord.Embed(
                title=f"🏆 Tournament Ranking - Page {i+1}/{total_pages}",
                color=discord.Color.gold(),
                description="Top participants"
            )
            top_users = await self.get_top_users(per_page, i * per_page)
            for idx, (user_id, points, subs) in enumerate(top_users, 1):
                user = ctx.guild.get_member(user_id) or await self.bot.fetch_user(user_id)
                emoji = ["🥇", "🥈", "🥉"][idx-1] if idx <= 3 else f"{idx}."
                avg = f"**Average:** {points/subs:.1f}" if subs > 0 else ""
                embed.add_field(
                    name=f"{emoji} {user.display_name if user else 'Unknown'}",
                    value=f"**Points:** {points}\n**Submissions:** {subs}\n{avg}",
                    inline=False
                )
            pages.append(embed)

        view = Paginator(pages)
        await ctx.send(embed=pages[page-1], view=view)

async def setup(bot):
    await bot.add_cog(RankingCog(bot))
