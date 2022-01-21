import datetime
from datetime import date
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

def format_date(myDate):
    return myDate.strftime("%Y-%m-%d")

def get_today():
    return format_date(date.today())

def get_tomorrow():
    tomorrow = date.today() + datetime.timedelta(days=1)
    return format_date(tomorrow)

def get_years(y_interval):
    return (dt.now() - relativedelta(years=y_interval))