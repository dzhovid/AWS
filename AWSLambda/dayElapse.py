# from datetime import date
# # day1 = date (2017-8-18)
# # day2 = date (2017-10-26)
# # delta = day2 - day1
# # print(delta.days)

# your_timezone_aware_variable= datetime.now
# tz_info = your_timezone_aware_variable.tzinfo

# # Now we can subtract two variables using the same time zone info
# # For instance
# # Lets obtain the Now() datetime but for the tz_info we got before

# diff = datetime.now(tz_info)-your_timezone_aware_variable
from datetime import datetime

#from datetime import timedelta
now = datetime.now()
# date = date.replace(tzinfo=None)
print(type(now))