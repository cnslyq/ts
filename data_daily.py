from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import tushare as ts
import py.pylog as pl
import conf

today = datetime.date.today()
print("Current Date : " + str(today))

engine = create_engine(conf.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

# daily
# if not ts.is_holiday(str(today)):
if True:
	pl.log("daily task start...")
	for item in conf.DAILY_LIST:
		pl.log(item + " daily start...")
		importstring = "import " + item + " as module"
		exec importstring
		module.daily(engine, session)
		pl.log(item + " daily done")
	pl.log("daily task done")

'''
# weekly on Tuesday, TBD
if 1 == today.weekday():
	pl.log("weekly task start...")
	for item in conf.WEEKLY_LIST:
		pl.log(item + " weekly start...")
		importstring = "import " + item + " as module"
		exec importstring
		module.weekly(engine, session)
		pl.log(item + " weekly done")
	pl.log("weekly task done")
'''

# monthly on the 1st of each month
if 1 == today.day:
	pl.log("monthly task start...")
	for item in conf.MONTHLY_LIST:
		pl.log(item + " monthly start...")
		importstring = "import " + item + " as module"
		exec importstring
		module.monthly(engine, session)
		pl.log(item + " monthly done")
	pl.log("monthly task done")
