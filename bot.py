import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from utils import (
    decode_jwt,
    extract_coupon_details,
    calculate_points,
    save_submission,
    get_leaderboard,
    add_player_to_pool,
    mark_coupon_submitted,
    get_players_without_submissions,
)
from datetime import time
import pytz

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    daily_reminder.start()

@bot.command(name="pomoc", help="Wyświetla zasady konkursu.")
async def pomoc(ctx):
    embed = discord.Embed(
        title="Zasady Konkursu",
        description="Prześlij swoje wygrane kupony, aby zdobywać punkty!",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name="kupon", help="Wyślij swój kupon.")
async def kupon(ctx, link: str):
    add_player_to_pool(ctx.author.id)

    try:
        token = link.split("id=")[1].split("&")[0]
    except IndexError:
        await ctx.send("❌ Nieprawidłowy link do kuponu.")
        return

    decoded_payload = decode_jwt(token)
    if not decoded_payload:
        await ctx.send("❌ Nieprawidłowy link do kuponu.")
        return

    coupon_details = extract_coupon_details(decoded_payload)
    points = calculate_points(coupon_details["amount_won"], coupon_details["odds"], coupon_details["bet_type"])

    save_submission(ctx.author.id, ctx.author.name, points)
    mark_coupon_submitted(ctx.author.id)

    await ctx.send(f"✅ Gratulacje! Zdobyłeś {points} punktów!")

@bot.command(name="topka", help="Pokaż ranking.")
async def topka(ctx):
    leaderboard_data = get_leaderboard()
    embed = discord.Embed(title="Ranking", color=discord.Color.gold())
    for idx, user in enumerate(leaderboard_data, start=1):
        embed.add_field(name=f"#{idx}", value=f"{user['username']}: {user['points']} punktów", inline=False)
    await ctx.send(embed=embed)

@tasks.loop(time=time(hour=20, minute=0, tzinfo=pytz.timezone("Europe/Warsaw")))
async def daily_reminder():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    for user_id in get_players_without_submissions():
        user = guild.get_member(user_id)
        if user:
            await user.send("⏰ Przypomnienie: Wyślij swój kupon dzisiaj!")

bot.run(TOKEN)
