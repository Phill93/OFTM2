from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_age(birthday: date):
    today = date.today()
    age = relativedelta(today, birthday).years
    return age
