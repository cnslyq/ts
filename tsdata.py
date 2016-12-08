from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.pylog as pl
import py.pyutil as pu
import sys

if len(sys.argv) < 2:
	print("please input function name (init/hist/daily)")
	sys.exit(1)

ENGINE = 'mysql://root:123456@127.0.0.1/mysql?charset=utf8'
INIT_LIST = ['py.stock']
HISTORY_LIST = ['py.trade', 'py.tops', 'py.invest']
DAILY_LIST = ['py.trade', 'py.tops', 'py.invest']
WEEKLY_LIST = ['py.tops', 'py.invest']
MONTHLY_LIST = ['py.tops', 'py.invest']
QUARTERLY_LIST = ['py.invest']

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

def init():
	pl.log("data initialization start...")
	for item in INIT_LIST:
		pl.log(item + " initialization start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.init(engine, session)
		pl.log(item + " initialization done")
	pl.log("data initialization done")
	
def history():
	if len(sys.argv) < 4:
		print("please input stardate and enddate ")  
		sys.exit(1)
	sdate = datetime.date(int(sys.argv[2][0:4]), int(sys.argv[2][4:6]), int(sys.argv[2][6:8]))
	edate = datetime.date(int(sys.argv[3][0:4]), int(sys.argv[3][4:6]), int(sys.argv[3][6:8]))
	
	pl.log("history data start...")
	for item in HISTORY_LIST:
		pl.log(item + " history start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.history(engine, session, sdate, edate)
		pl.log(item + " history done")
	pl.log("history data done")
	
def daily():
	today = datetime.date.today()
	# daily
	pl.log("daily task start...")
	for item in DAILY_LIST:
		pl.log(item + " daily start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.daily(engine, session, today)
		pl.log(item + " daily done")
	pl.log("daily task done")
	
	# TBD
	# weekly on Tuesday
	if 1 == today.weekday():
		cdate = today - datetime.timedelta(days=7)
		pl.log("weekly task start...")
		for item in WEEKLY_LIST:
			pl.log(item + " weekly start...")
			impstr = "import " + item + " as module"
			exec impstr
			module.weekly(engine, session, cdate)
			pl.log(item + " weekly done")
		pl.log("weekly task done")
	
	# TBD
	# monthly on the 1st of each month
	if 1 == today.day:
		ldate = pu.get_ldate(today)
		pl.log("monthly task start...")
		for item in MONTHLY_LIST:
			pl.log(item + " monthly start...")
			impstr = "import " + item + " as module"
			exec impstr
			module.monthly(engine, session, ldate["year"], ldate["month"])
			pl.log(item + " monthly done")
		pl.log("monthly task done")
		
		# TBD
		# quarterly on the 1st of June, April, July, October
		if today.month in (1, 4, 7, 10):
			pl.log("quarterly task start...")
			for item in QUARTERLY_LIST:
				pl.log(item + " quarterly start...")
				impstr = "import " + item + " as module"
				exec impstr
				module.quarterly(engine, session, ldate["year"], ldate["quarter"])
				pl.log(item + " quarterly done")
			pl.log("quarterly task done")
	

if sys.argv[1] == "init":
	init()
elif sys.argv[1] == "hist":
	history()
elif sys.argv[1] == "daily":
	daily()
else:
	print("wrong function name")
	sys.exit(1)
