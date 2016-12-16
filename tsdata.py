from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.pylog as pl
import py.pyutil as pu
import py.pyconfig as pc
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
	hs   ->  history_s
	real ->  real
'''
INPUT_LIST = ['init', 'hist', 'cron', 'hm', 'hq', 'hy', 'ha', 'hs', 'real']
INIT_LIST = ['py.stock', 'py.macro', 'py.fund']
HISTORY_LIST = ['py.trade', 'py.tops', 'py.invest', 'py.fund']
DAILY_LIST = ['py.trade', 'py.invest', 'py.fund', 'py.other']
WEEKLY_LIST = ['py.tops', 'py.invest']
MONTHLY_LIST = ['py.stock', 'py.macro', 'py.tops', 'py.invest', 'py.basic', 'py.fund', 'py.other']
QUARTERLY_LIST = ['py.invest', 'py.basic', 'py.fund']
HISTORY_M_LIST = ['py.invest', 'py.other']
HISTORY_Q_LIST = ['py.invest', 'py.basic']
HISTORY_Y_LIST = ['py.other']
HISTORY_A_LIST = ['py.invest']
HISTORY_S_LIST = ['py.trade']
REAL_LIST = ['py.news']

engine = create_engine(pc.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

names = locals()
def call(inp, *params):
	st = datetime.datetime.today()
	pl.log(inp + " data start...")
	estr = "func(engine, session"
	for i in range(len(params)):
		estr += ", params[%i]" % i
	estr += ")"
	c = compile(estr,'','exec')
	list = names['%s_LIST' % inp.upper()]
	for item in list:
		pl.log(item + " start...")
		obj = __import__(item, fromlist=True)
		func = getattr(obj, inp)
		# func(engine, session)
		exec c
		pl.log(item + " done")
	et = datetime.datetime.today()
	pl.log(inp + " data done cost time : " + str(et - st))

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
	
def hs():
	if len(sys.argv) < 4:
		print("please input code, year ")
		sys.exit(1)
	call('history_s', sys.argv[2], sys.argv[3])
	
def real():
	call('real')
	
def cron(cdate = datetime.date.today()):
	# process today's data
	call('daily', cdate)
	
	# process last week's data every Monday(?)
	if 1 == cdate.isoweekday():
		call('weekly', cdate - datetime.timedelta(days=7))
	
	# process last month's data on the 1st of each month
	if 1 == cdate.day:
		ldate = pu.get_ldate(cdate, -1)
		call('monthly', ldate["year"], ldate["month"])
	
	# process last quarter's data on the 2nd of March, June, September and December
	if 2 == cdate.day and cdate.month in (3, 6, 9, 12):
		ldate = pu.get_ldate(cdate, -5)
		call('quarterly', ldate["year"], ldate["quarter"])

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("please input function name (init/hist/cron/hm/hq/hy/ha/hs)")
		sys.exit(1)
	inp = sys.argv[1]
	if inp in INPUT_LIST:
		func = getattr(td, inp)
		func()
	else:
		print("wrong function name")
		sys.exit(1)
