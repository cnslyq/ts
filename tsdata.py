from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.tslog as tsl
import py.tsutil as tsu
import py.tsconf as tsc
import sys
import tsdata as td

'''
	INPUT    FUNCTION
	init ->  init
	hist ->  history
	cron ->  daily, weekly, monthly, quarterly
	hm   ->  history_m
	hq   ->  history_q
	hy   ->  history_y
	ha   ->  history_a
	stock->  history_stock
	fund ->  history_fund
	real ->  real
'''
engine = create_engine(tsc.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

names = tsc.names
def call(inp, *params):
	st = datetime.datetime.today()
	tsl.log(inp + " data start...")
	estr = "func(engine, session"
	for i in range(len(params)):
		estr += ", params[%i]" % i
	estr += ")"
	c = compile(estr,'','exec')
	list = names['%s_LIST' % inp.upper()]
	for item in list:
		name = '%s_SWITCH' % item.upper().split('.')[-1]
		if names[name]:
			tsl.log(item + " start...")
			obj = __import__(item, fromlist=True)
			func = getattr(obj, inp)
			exec c
			tsl.log(item + " done")
	et = datetime.datetime.today()
	tsl.log(inp + " data done cost time : " + str(et - st))

def init():
	call('init')
	
def hist():
	if len(sys.argv) < 4:
		print("please input startdate, enddate ")
		sys.exit(1)
	sdate = datetime.date(int(sys.argv[2][0:4]), int(sys.argv[2][4:6]), int(sys.argv[2][6:8]))
	edate = datetime.date(int(sys.argv[3][0:4]), int(sys.argv[3][4:6]), int(sys.argv[3][6:8]))
	call('history', sdate, edate)
	
def hm():
	if len(sys.argv) < 4:
		print("please input year, month ")
		sys.exit(1)
	call('history_m', int(sys.argv[2]), int(sys.argv[3]))
	
def hq():
	if len(sys.argv) < 4:
		print("please input year, quarter ")
		sys.exit(1)
	call('history_q', int(sys.argv[2]), int(sys.argv[3]))
	
def hy():
	if len(sys.argv) < 3:
		print("please input year ")
		sys.exit(1)
	call('history_y', int(sys.argv[2]))
	
def ha():
	call('history_a')
	
def stock():
	if len(sys.argv) < 3:
		print("please input stock code")
		sys.exit(1)
	call('history_stock', sys.argv[2])
	
def fund():
	if len(sys.argv) < 3:
		print("please input fund code")
		sys.exit(1)
	call('history_fund', sys.argv[2])
	
def real():
	call('real')
	
def cron(cdate = datetime.date.today()):
	print "***********************************************************************"
	tsl.log("%s cron task start..." % str(cdate))
	# process today's data
	call('daily', cdate)
	
	# process week's data
	if cdate.isoweekday() in (1, 5):
		call('weekly', cdate)
	
	# process last month's data on the 1st of each month
	if 1 == cdate.day:
		ldate = tsu.get_ldate(cdate, -1)
		call('monthly', ldate["year"], ldate["month"])
	
	# process last quarter's data on the 2nd of March, June, September and December
	if 2 == cdate.day and cdate.month in (3, 6, 9, 12):
		ldate = tsu.get_ldate(cdate, -5)
		call('quarterly', ldate["year"], ldate["quarter"])
	tsl.log("%s cron task done" % str(cdate))
	print "***********************************************************************"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("please input function name (init/hist/cron/hm/hq/hy/ha/stock/fund)")
		sys.exit(1)
	inp = sys.argv[1]
	if inp in tsc.INPUT_LIST:
		func = getattr(td, inp)
		func()
	else:
		print("wrong function name")
		sys.exit(1)
