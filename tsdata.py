from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.pylog as pl
import py.pyutil as pu
import sys

if len(sys.argv) < 2:
	print("please input function name (init/hist/cron)")
	sys.exit(1)

ENGINE = 'mysql://root:123456@127.0.0.1/mysql?charset=utf8'
INIT_LIST = ['py.stock']
HISTORY_LIST = ['py.trade', 'py.tops', 'py.invest']
HISTORY_M_LIST = ['py.invest']
HISTORY_Q_LIST = ['py.invest']
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
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.init(engine, session)
		pl.log(item + " done")
	pl.log("data initialization done")
	
def history(sdate, edate):
	pl.log("history data start...")
	for item in HISTORY_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.history(engine, session, sdate, edate)
		pl.log(item + " done")
	pl.log("history data done")
	
def history_m(year, month):
	pl.log("history month data start...")
	for item in HISTORY_M_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.history_m(engine, session, year, month)
		pl.log(item + " done")
	pl.log("history month data done")
	
def history_q(year, quarter):
	pl.log("history quarter data start...")
	for item in HISTORY_Q_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.history_q(engine, session, year, quarter)
		pl.log(item + " done")
	pl.log("history quarter data done")
	
def cron(cdate):
	# process today's data
	ts_daily(cdate)
	
	# process last week's data every Tuesday(?)
	if 1 == cdate.weekday():
		ts_weekly(cdate - datetime.timedelta(days=7))
	
	# process last month's data on the 1st of each month
	if 1 == cdate.day:
		ldate = pu.get_ldate(cdate)
		ts_monthly(ldate["year"], ldate["month"])
		
		# process last quarter's data on the 1st of Janurary, April, July and October
		if cdate.month in (1, 4, 7, 10):
			ts_quarterly(ldate["year"], ldate["quarter"])

def ts_daily(cdate):
	pl.log("daily task start...")
	for item in DAILY_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.daily(engine, session, cdate)
		pl.log(item + " done")
	pl.log("daily task done")

def ts_weekly(ydate):
	pl.log("weekly task start...")
	for item in WEEKLY_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.weekly(engine, session, ydate)
		pl.log(item + " done")
	pl.log("weekly task done")

def ts_monthly(year, month):
	pl.log("monthly task start...")
	for item in MONTHLY_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.monthly(engine, session, year, month)
		pl.log(item + " done")
	pl.log("monthly task done")

def ts_quarterly(year, quarter):
	pl.log("quarterly task start...")
	for item in QUARTERLY_LIST:
		pl.log(item + " start...")
		impstr = "import " + item + " as module"
		exec impstr
		module.quarterly(engine, session, year, quarter)
		pl.log(item + " done")
	pl.log("quarterly task done")

if sys.argv[1] == "init":
	init()
elif sys.argv[1] == "hist":
	if len(sys.argv) < 4:
		print("please input startdate, enddate ")
		sys.exit(1)
	sdate = datetime.date(int(sys.argv[2][0:4]), int(sys.argv[2][4:6]), int(sys.argv[2][6:8]))
	edate = datetime.date(int(sys.argv[3][0:4]), int(sys.argv[3][4:6]), int(sys.argv[3][6:8]))
	history(sdate, edate)
elif sys.argv[1] == "hm":
	if len(sys.argv) < 4:
		print("please input year, month ")
		sys.exit(1)
	history_m(int(sys.argv[2]), int(sys.argv[3]))
elif sys.argv[1] == "hq":
	if len(sys.argv) < 4:
		print("please input year, quarter ")
		sys.exit(1)
	history_q(int(sys.argv[2]), int(sys.argv[3]))
elif sys.argv[1] == "cron":
	today = datetime.date.today()
	cron(today)
else:
	print("wrong function name")
	sys.exit(1)
