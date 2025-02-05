def validate_coupon(link, amount, odds, bet_type):
    valid_types = ["SOLO", "SOLO_ODDS", "AKO", "AKO_ODDS"]
    if bet_type not in valid_types:
        return {"success": False, "message": "Nieprawidłowy rodzaj zakładu."}
    if amount <= 0:
        return {"success": False, "message": "Kwota musi być większa niż 0."}
    if odds <= 0:
        return {"success": False, "message": "Kurs musi być większy niż 0."}
    if not link.startswith("http"):
        return {"success": False, "message": "Link do kuponu jest nieprawidłowy."}
    return {"success": True}

def calculate_points(amount, odds, bet_type):
    if bet_type == "SOLO":
        return amount * 1
    elif bet_type == "SOLO_ODDS" and odds > 10:
        return amount * 2
    elif bet_type == "AKO":
        return amount * 2.5
    elif bet_type == "AKO_ODDS" and odds > 10:
        return amount * 5
    return 0

def get_leaderboard(user_id=None):
    # Mock data
    mock_leaderboard = [
        {"user_id": 1, "username": "Użytkownik1", "points": 5000},
        {"user_id": 2, "username": "Użytkownik2", "points": 4500},
        {"user_id": 3, "username": "Użytkownik3", "points": 4000},
    ]
    if user_id:
        for idx, user in enumerate(mock_leaderboard, start=1):
            if user["user_id"] == user_id:
                return {"position": idx, "points": user["points"]}
        return None
    return mock_leaderboard

def award_prizes():
    # Logic to distribute prizes (mocked here)
    pass