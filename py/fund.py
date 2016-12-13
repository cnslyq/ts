import tushare as ts
import datetime
import pylog as pl
import pyutil as pu

def init(engine, session):
	# get latest codes
	pl.log("get latest codes start...")
	codes = []
	df = ts.get_nav_open()
	print
	codes += [str(item) for item in df.symbol.values]
	df = ts.get_nav_close()
	print
	codes += [str(item) for item in df.symbol.values]
	df = ts.get_nav_grading()
	print
	codes += [str(item) for item in df.symbol.values]
	pl.log("get latest codes done")
	# insert latest info into fund_temp_info
	temp_info(engine, codes)
	# update fund_temp_info to fund_info
	pl.log("call update_fund_info start...")
	# session.execute('call update_fund_info')
	pl.log("call update_fund_info done")
	
def daily(engine, session, cdate):
	nav_open(engine, cdate)
	nav_close(engine, cdate)
	nav_grading(engine, cdate)

def monthly(engine, session, year, month):
	sdate=datetime.date(year, month, 1)
	edate=datetime.date.today() - datetime.timedelta(days=1)
	history(engine, session, sdate, edate)

def quarterly(engine, session, year, quarterly):
	init(engine, session)
	
def history(engine, session, sdate, edate):
	codes = pu.get_fund_codes(session)
	for code in codes:
		nav_history(code, sdate, edate)

def temp_info(engine, codes):
	tbl = "fund_temp_info"
	pl.log(tbl + " start...")
	cnt = 0
	first = True
	for code in codes:
		try:
			if cnt % 100 == 0:
				df = ts.get_fund_info(code).reset_index()
			else:
				newdf = ts.get_fund_info(code).reset_index()
				df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			print e
			pl.log(tbl + " error for " + code)
		if cnt % 100 == 99:
			pl.log("process %i codes" % cnt)
			if(first):
				df.to_sql(tbl,engine,if_exists='replace')
				first = False
			else:
				df.to_sql(tbl,engine,if_exists='append')
		cnt += 1
	if(first):
		df.to_sql(tbl,engine,if_exists='replace')
	else:
		df.to_sql(tbl,engine,if_exists='append')
	pl.log(tbl + " done")

def nav_open(engine, cdate):
	tbl = "fund_nav_open"
	pl.log(tbl + " start...")
	try:
		df = ts.get_nav_open()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")

def nav_close(engine, cdate):
	tbl = "fund_nav_close"
	pl.log(tbl + " start...")
	try:
		df = ts.get_nav_close()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")

def nav_grading(engine, cdate):
	tbl = "fund_nav_grading"
	pl.log(tbl + " start...")
	try:
		df = ts.get_nav_grading()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")

def nav_history(engine, code, sdate, edate):
	tbl = "fund_nav_history"
	pl.log(tbl + " start...")
	try:
		df = ts.get_nav_history(code, str(sdate), str(edate))
		df['symbol'] = code
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
