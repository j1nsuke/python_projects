import datetime
def is_weekday(date): # 週末＋祝日（2026年末分まで）を除外
    jpholidays = [
    datetime.date(2024, 1, 1), datetime.date(2024, 1, 8), datetime.date(2024, 2, 11), datetime.date(2024, 2, 12), datetime.date(2024, 3, 20), datetime.date(2024, 4, 29), datetime.date(2024, 5, 3), datetime.date(2024, 5, 4), datetime.date(2024, 5, 5), datetime.date(2024, 5, 6),
    datetime.date(2024, 7, 15), datetime.date(2024, 8, 11), datetime.date(2024, 8, 12), datetime.date(2024, 9, 16), datetime.date(2024, 9, 22), datetime.date(2024, 10, 14), datetime.date(2024, 11, 3), datetime.date(2024, 11, 4), datetime.date(2024, 11, 23), datetime.date(2024, 12, 23),
    datetime.date(2025, 1, 1), datetime.date(2025, 1, 13), datetime.date(2025, 2, 11), datetime.date(2025, 3, 20), datetime.date(2025, 4, 29), datetime.date(2025, 5, 3), datetime.date(2025, 5, 4), datetime.date(2025, 5, 5), datetime.date(2025, 5, 6),
    datetime.date(2025, 7, 21), datetime.date(2025, 8, 11), datetime.date(2025, 9, 15), datetime.date(2025, 9, 23), datetime.date(2025, 10, 13), datetime.date(2025, 11, 3), datetime.date(2025, 11, 23), datetime.date(2025, 11, 24), datetime.date(2025, 12, 23),
    datetime.date(2026, 1, 1), datetime.date(2026, 1, 12), datetime.date(2026, 2, 11), datetime.date(2026, 3, 20), datetime.date(2026, 4, 29), datetime.date(2026, 5, 3), datetime.date(2026, 5, 4), datetime.date(2026, 5, 5), datetime.date(2026, 5, 6),
    datetime.date(2026, 7, 20), datetime.date(2026, 8, 11), datetime.date(2026, 9, 21), datetime.date(2026, 9, 22), datetime.date(2026, 9, 23), datetime.date(2026, 10, 12), datetime.date(2026, 11, 3), datetime.date(2026, 11, 23), datetime.date(2026, 12, 23)
] 
    if date in jpholidays:
        return False
    else:
        return date.weekday() < 5