import datetime as dt

start_date = dt.datetime(1901, 1, 1)
end_date = dt.datetime(2000, 12, 31)
day = dt.timedelta(days=1)

date = start_date
sundays = 0

while date <= end_date:
    if date.weekday() == 6 and date.day == 1:
        sundays += 1
    date = date + day

print(f'Solution to Project Euler 19 is {sundays}')