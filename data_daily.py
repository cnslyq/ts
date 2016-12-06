import os
import datetime
import tushare as ts
import py.pylog as pl

daily_list = ['trade_daily.py']
weekly_list = ['tops_weekly.py']
monthly_list = ['tops_monthly.py']
today = datetime.date.today()
print("Current Date : " + str(today))

# daily
if not ts.is_holiday(str(today)):
	pl.log("daily task start...")
	for item in daily_list:
		os.system('python /home/ts/py/%s' % item)
	pl.log("daily task done")

'''
# weekly on Tuesday, TBD
if 1 == today.weekday():
	pl.log("weekly task start...")
	for item in weekly_list:
		os.system('python /home/ts/py/%s' % item)
	pl.log("weekly task done")
'''

# monthly on the 1st of each month
if 1 == today.day:
	pl.log("monthly task start...")
	for item in monthly_list:
		os.system('python /home/ts/py/%s' % item)
	pl.log("monthly task done")
