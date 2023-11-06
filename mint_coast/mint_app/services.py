"""Здесь храним сервисы(функции и классы). Всё утилитарное/вспомогателльное, типа send_email"""
from .models import Ban
from datetime import datetime, timedelta
from pytz import timezone


def ban_user(user, end_date, reason='') -> bool:
    start_date = datetime.now(timezone('Europe/Moscow'))
    try:
        print(f'user: {user} start: {start_date} end: {end_date} reason: {reason}')
        Ban.objects.create(user=user, start_date=start_date, end_date=end_date, reason=reason)
        return True
    except Exception:
        return False


def unban_user(user) -> bool:
    try:
        ban = Ban.objects.get(user=user)
        ban.delete()
        return True
    except Exception:
        return False


def validate_user(first_name, last_name, username):
    return 3 < len(first_name) < 15 and 3 < len(last_name) < 15 and 3 < len(username) < 15
