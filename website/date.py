from datetime import datetime

def convert_datetime(timestamp):
    now = datetime.now(timestamp.tzinfo)
    time_diff = now - timestamp

    if time_diff.total_seconds() < 60 * 60:  # Less than 60 minutes
        minutes = int(time_diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    elif time_diff.total_seconds() < 24 * 60 * 60:  # Less than 24 hours
        hours = int(time_diff.total_seconds() / 60 / 60)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    else:  # More than 24 hours
        days = int(time_diff.total_seconds() / 60 / 60 / 24)
        return f"{days} day{'s' if days != 1 else ''} ago"
    
def get_date(favorited_date):
    date = str(favorited_date)[0:10]
    return date[5:7]+date[7:]+"-"+date[0:4]