from datetime import datetime, timedelta , date

date = date.today()
print(type(date))

print(date + timedelta(2))

start_date = '2025-12-25'
yr , mn ,dy  = start_date.split('-')
print(yr ,mn , dy)

date_format = '%Y-%m-%d'
date_real  = datetime.strptime(start_date , date_format).date()
print(date_real)

print(date_real + timedelta(int(0)))