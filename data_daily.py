import os
import datetime
import tushare as ts
import py.pylog as pl
import conf

today = datetime.date.today()
print("Current Date : " + str(today))

# daily
if not ts.is_holiday(str(today)):
	pl.log("daily task start...")
	for item in conf.DAILY_LIST:
		os.system('python %s%s' % (conf.PY_PATH, item))
	pl.log("daily task done")

'''
# weekly on Tuesday, TBD
if 1 == today.weekday():
	pl.log("weekly task start...")
	for item in conf.WEEKLY_LIST:
		os.system('python %s%s' % (conf.PY_PATH, item))
	pl.log("weekly task done")
'''

# monthly on the 1st of each month
if 1 == today.day:
	pl.log("monthly task start...")
	for item in conf.MONTHLY_LIST:
		os.system('python %s%s' % (conf.PY_PATH, item))
	pl.log("monthly task done")
