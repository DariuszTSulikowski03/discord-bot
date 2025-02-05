import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime
from utils import validate_coupon, calculate_points, get_leaderboard, award_prizes

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ID of #championship-typers

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot Ready
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    print(f"{bot.user} has connected to {guild.name}!")
    daily_reminder.start()  # Start daily reminder task

# Command: Submit Coupon
@bot.command(name="submit", help="Wyślij swój kupon.")
async def submit(ctx, link: str, amount: float, odds: float, bet_type: str):
    # Check if user has the required role
    if not any(role.name == "zweryfikowany" for role in ctx.author.roles):
        await ctx.send("❌ Nie masz wymaganej roli @zweryfikowany.")
        return

    # Validate coupon
    validation_result = validate_coupon(link, amount, odds, bet_type)
    if not validation_result["success"]:
        await ctx.send(validation_result["message"])
        return

    # Calculate points
    points = calculate_points(amount, odds, bet_type)

    # Save submission to database (mocked here)
    # db.save_submission(ctx.author.id, link, amount, odds, bet_type, points)

    # Congratulate user
    await ctx.send(f"✅ Gratulacje! Zdobyłeś {points} punktów za ten zakład.")

    # Update leaderboard
    rank_data = get_leaderboard(ctx.author.id)
    await ctx.send(f"🏆 Twoja pozycja: #{rank_data['position']} z {rank_data['points']} punktami!")

# Task: Daily Reminder
@tasks.loop(hours=24)
async def daily_reminder():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    await channel.send("⏰ Przypomnienie: Wyślij swój kupon dzisiaj, aby zdobyć punkty!")

# Task: End of Contest Announcement
@tasks.loop(count=1)
async def end_of_contest():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    # Get leaderboard
    leaderboard = get_leaderboard()

    # Announce winners
    top_users = leaderboard[:20]
    prize_pool = 3500
    prize_per_user = prize_pool / len(top_users)

    announcement = f"🎉 KONIEC MISTRZOSTW TYPERÓW!\n"
    announcement += f"Całkowita pula nagród: {prize_pool} PLN w darmowych zakładach.\n"
    announcement += "Najlepsi typerzy:\n"
    for idx, user in enumerate(top_users, start=1):
        announcement += f"{idx}. {user['username']} - {user['points']} punktów\n"

    announcement += f"\nNajlepszy typer miesiąca: {leaderboard[0]['username']} (@TYPER OF THE MONTH - FEBRUARY)"
    await channel.send(announcement)

# Run the bot
bot.run(TOKEN)