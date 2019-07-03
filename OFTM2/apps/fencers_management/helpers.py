from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_age(birthday: date):
    today = date.today()
    age = relativedelta(today, birthday).years
    return age

def calculate_birthday(start: date, age: int):
    birthday = start.today() - relativedelta(years=age)
    return birthday