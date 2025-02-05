import os
import jwt
import pytz
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    points = Column(Integer, default=0)

class CouponSubmission(Base):
    __tablename__ = "coupon_submissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)
    submitted = Column(Boolean, default=False)

if engine:
    Base.metadata.create_all(engine)

# Decode JWT Payload
def decode_jwt(token):
    try:
        decoded_payload = jwt.decode(token, options={"verify_signature": False})
        return decoded_payload
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None

# Extract Coupon Details
def extract_coupon_details(decoded_payload):
    return {
        "bet_type": decoded_payload.get("bet_type", "UNKNOWN"),
        "odds": float(decoded_payload.get("odds", 0)),
        "amount_won": float(decoded_payload.get("amount_won", 0))
    }

# Calculate Points
def calculate_points(amount_won, odds, bet_type):
    if bet_type == "SOLO":
        return amount_won * 1
    elif bet_type == "SOLO" and odds > 10:
        return amount_won * 2
    elif bet_type == "AKO":
        return amount_won * 2.5
    elif bet_type == "AKO" and odds > 10:
        return amount_won * 5
    return 0

# Save Submission to Database
def save_submission(user_id, username, points):
    if not engine:
        print("Database not configured.")
        return
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        user.points += points
    else:
        user = User(user_id=user_id, username=username, points=points)
        session.add(user)
    session.commit()
    session.close()

# Get Leaderboard
def get_leaderboard():
    if not engine:
        return [{"username": "User1", "points": 5000}, {"username": "User2", "points": 4500}]
    session = Session()
    leaderboard = session.query(User).order_by(User.points.desc()).limit(20).all()
    session.close()
    return [{"username": user.username, "points": user.points} for user in leaderboard]

# Track Daily Submissions
def add_player_to_pool(user_id):
    if not engine:
        return
    session = Session()
    today = datetime.now(pytz.timezone("Europe/Warsaw")).date()
    submission = session.query(CouponSubmission).filter_by(user_id=user_id, submission_date=today).first()
    if not submission:
        session.add(CouponSubmission(user_id=user_id, submission_date=today, submitted=False))
        session.commit()
    session.close()

def mark_coupon_submitted(user_id):
    if not engine:
        return
    session = Session()
    today = datetime.now(pytz.timezone("Europe/Warsaw")).date()
    submission = session.query(CouponSubmission).filter_by(user_id=user_id, submission_date=today).first()
    if submission:
        submission.submitted = True
        session.commit()
    session.close()

def get_players_without_submissions():
    if not engine:
        return []
    session = Session()
    today = datetime.now(pytz.timezone("Europe/Warsaw")).date()
    players = session.query(CouponSubmission).filter_by(submission_date=today, submitted=False).all()
    session.close()
    return [player.user_id for player in players]
