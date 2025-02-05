# utils.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
import jwt
from datetime import datetime
import discord
from urllib.parse import urlparse, parse_qs, unquote
import logging

# Define database models
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    points = Column(Integer, default=0)
    last_submission = Column(DateTime)

class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    bet_type = Column(String)
    odds = Column(Float)
    points = Column(Integer)
    timestamp = Column(DateTime)

# Create database (adjust connection string for PostgreSQL if needed)
engine = create_engine('sqlite:///data/typers.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def calculate_points(amount_won, odds, bet_type):
    bet_type = bet_type.lower()
    if bet_type == "solo":
        return int(amount_won * (2 if odds >= 10.0 else 1))
    elif bet_type == "ako":
        return int(amount_won * (5 if odds >= 10.0 else 2.5))
    return 0

def save_submission(user_id, username, points, bet_type, odds):
    with db_session() as s:
        player = s.query(Player).get(user_id)
        if not player:
            player = Player(id=user_id, username=username)
            s.add(player)
        player.points += points
        player.last_submission = datetime.now()
        
        submission = Submission(
            user_id=user_id,
            bet_type=bet_type,
            odds=odds,
            points=points,
            timestamp=datetime.now()
        )
        s.add(submission)

def get_user_rank(user_id):
    with db_session() as s:
        players = s.query(Player).order_by(Player.points.desc()).all()
        return next((i+1 for i, p in enumerate(players) if p.id == user_id), None)

def count_daily_submissions():
    with db_session() as s:
        today = datetime.now().date()
        count = s.query(func.count(Submission.id)).filter(func.date(Submission.timestamp) == today).scalar()
        return count or 0

def get_user_profile(user_id):
    with db_session() as s:
        player = s.query(Player).get(user_id)
        if not player:
            return {
                'points': 0,
                'submissions': 0,
                'avg_points': 0,
                'achievements': []
            }
        submissions = s.query(Submission).filter(Submission.user_id == user_id).all()
        total_points = sum(sub.points for sub in submissions)
        submissions_count = len(submissions)
        avg_points = int(total_points / submissions_count) if submissions_count else 0
        achievements = []
        if player.points >= 1000:
            achievements.append("Pierwszy tysiąc!")
        if player.points >= 5000:
            achievements.append("Mega Typers!")
        return {
            'points': player.points,
            'submissions': submissions_count,
            'avg_points': avg_points,
            'achievements': achievements
        }

def get_championship_stats():
    with db_session() as s:
        total_submissions = s.query(func.count(Submission.id)).scalar() or 0
        avg_daily = total_submissions  # Simplified example
        biggest_jump = 100  # Placeholder value
        players = s.query(Player).order_by(Player.points.desc()).limit(3).all()
        top3 = [{'name': player.username, 'points': player.points} for player in players]
        return {
            'total_submissions': total_submissions,
            'avg_daily': avg_daily,
            'biggest_jump': biggest_jump,
            'top3': top3
        }

def get_leaderboard():
    with db_session() as s:
        players = s.query(Player).order_by(Player.points.desc()).all()
        return [{"username": player.username, "points": player.points} for player in players]

def get_last_submission(user_id):
    with db_session() as s:
        submission = s.query(Submission).filter(Submission.user_id == user_id).order_by(Submission.timestamp.desc()).first()
        return submission.timestamp if submission else None

def is_same_day(timestamp, now):
    return timestamp.date() == now.date()

def parse_coupon_link(link):
    try:
        parsed_url = urlparse(link)
        qs = parse_qs(parsed_url.query)
        token = qs.get('id', [None])[0]
        if not token and 'deeplink' in qs:
            deeplink_val = unquote(qs['deeplink'][0])
            nested_parsed = urlparse(deeplink_val)
            nested_qs = parse_qs(nested_parsed.query)
            token = nested_qs.get('id', [None])[0]
        if not token:
            logging.error("Nie znaleziono tokenu w linku.")
            return None
        decoded = jwt.decode(token, options={"verify_signature": False})
        logging.info(f"Decoded coupon payload: {decoded}")
        return {
            'bet_type': decoded.get("bet_type", "solo").lower(),
            'odds': float(decoded.get("odds", 1)),
            'amount_won': float(decoded.get("amount_won", 0))
        }
    except Exception as e:
        logging.error(f"Błąd przy parsowaniu linku: {e}")
        return None

async def error_embed(channel, message):
    embed = discord.Embed(
        title="❌ Błąd!",
        description=message,
        color=discord.Color.red()
    )
    await channel.send(embed=embed, delete_after=15
