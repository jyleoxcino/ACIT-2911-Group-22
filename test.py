import datetime
from datetime import timedelta, date

first_date = "2023-05-31"
last_date = "2023-08-01"

first_date1 = datetime.datetime.strptime(first_date, "%Y-%m-%d")
last_date1 = datetime.datetime.strptime(last_date, "%Y-%m-%d")

date2 = (last_date1 - first_date1)
print(type(date2))
print(datetime.datetime.strptime(first_date, "%Y-%m-%d") + timedelta(days=7))

print(type(date2.days))
