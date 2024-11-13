# Import
from datetime import datetime, date, timedelta

if __name__ == "__main__":
    print("Results")
    print("-------")
    # Get current
    now = datetime.now()
    today = date.today()

    print(f"now {now}")
    print(f"today {today}")

    # Create time and date
    a_time = datetime(2024, 3, 14, 15, 30)
    a_date = date(2024, 3, 14)

    print(f"A time {a_time}")
    print(f"A date {a_date}")

    # Format date to string
    print(f"formatted datetime {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Add/subtract time
    print(f"7 days from today {now + timedelta(days=7)}")
    print(f"7 days before today {now - timedelta(days=7)}")
    print(f"Days elapsed since 2024-01-01 {today-date(2024,1,1)} ")