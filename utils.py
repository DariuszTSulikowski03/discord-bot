# utils.py
def calculate_points(bet_type: str, odds: float, amount: float) -> int:
    bet_type = bet_type.lower()
    if bet_type == "solo":
        multiplier = 2 if odds > 10.0 else 1
    elif bet_type == "ako":
        multiplier = 5 if odds > 10.0 else 2.5
    else:
        multiplier = 1
    return int(amount * multiplier)
