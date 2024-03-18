from datetime import datetime, timedelta
from collections import defaultdict


def weekend_checked(day: datetime) -> datetime:
    """Checks if a certain day is Saturday or Sunday and if it is, moving the date to next monday"""
    while day.weekday() in (5, 6):
        day += timedelta(days=1)
    return day


def birthday_next_week(birthday: datetime) -> bool | datetime:
    """Checks if person`s birthday is during next 7 days"""
    if birthday.month == 2 and birthday.day == 29:
        birthday = birthday.replace(
            day=28
        )  # Celebrating February 29`s birthday in February 28
    todays_date = datetime.today().date()
    bday_this_year = datetime(todays_date.year, birthday.month, birthday.day).date()

    if bday_this_year < todays_date and bday_this_year.weekday not in (
        5,
        6,
    ):  # Checking the next year as well
        bday_next_year = weekend_checked(
            bday_this_year.replace(year=bday_this_year.year + 1)
        )
        if (
            timedelta(days=0) <= bday_next_year - todays_date < timedelta(days=7)
        ):  # If there is 6 or less days until birthday
            return bday_next_year
    elif (
        timedelta(days=0)
        <= weekend_checked(bday_this_year) - todays_date
        < timedelta(days=7)
    ):
        return weekend_checked(bday_this_year)
    else:
        return False


def get_birthdays_per_week(users: list[dict]) -> None:
    """Prints list of people who you need to congratulate day by day"""
    to_celebrate = defaultdict(list)

    for user in users:
        birthday = birthday_next_week(user["birthday"])
        if birthday:  # If there is 6 or less days until birthday
            to_celebrate[birthday].append(user["name"])

    sorted_birthdays = sorted(to_celebrate)  # Sorting birthdays by ascending
    return [
        f"{birthday.strftime('%A')}: {', '.join(sorted(to_celebrate[birthday]))}"
        for birthday in sorted_birthdays
    ]  # Sorting lists of people as well
