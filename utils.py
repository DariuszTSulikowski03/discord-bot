def calculate_points(typ, odds, kwota):
    """
    Calculate points based on the bet type, odds, and amount (kwota).

    For example:
    - For 'win', points = kwota * (odds - 1)
    - For 'draw', points = half of that value
    - For 'lose', points could be negative or 0
    """
    typ = typ.lower()
    if typ == 'win':
        return kwota * (odds - 1)
    elif typ == 'draw':
        return kwota * (odds - 1) / 2
    elif typ == 'lose':
        return -kwota
    else:
        # Unrecognized type returns 0 points.
        return 0
