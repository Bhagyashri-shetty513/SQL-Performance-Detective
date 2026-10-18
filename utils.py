
def calculate_change(before, after):
    """Calculate percentage improvement from before to after."""
    if before == 0:
        return None
    return ((before - after) / before) * 100
