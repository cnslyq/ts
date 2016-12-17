import tushare as ts
import datetime
import pylog as pl
import pyutil as pu
import gc
import pandas as pd
import pyconfig as pc

def init(engine, session):
	# get latest codes
	pl.log("get latest codes start...")
	codes = []
	df = ts.get_nav_open().symbol.values
	print
	codes.extend([str(item) for item in df])
	df = ts.get_nav_close().symbol.values
	print
	codes.extend([str(item) for item in df])
	df = ts.get_nav_grading().symbol.values
	print
	codes.extend([str(item) for item in df])
	pl.log("get latest codes done")
	# insert latest info into fund_temp_info
	# rmcodes = ['37001B', '16162A', '16300L']
	session.execute("delete from fund_temp_info")
	temp_info(engine, codes)
	# update fund_temp_info to fund_info
	pl.log("call update_fund_info start...")
	session.execute('call update_fund_info')
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
	tbl = "fund_nav_history"
	pl.log(tbl + " start...")
	codes = pu.get_fund_codes(session)
	cnt = 0
	for code in codes:
		nav_history(engine, code, codes[code], sdate, edate)
		cnt += 1
		if cnt % pc.FUND_GC_NUM is 0:
			pl.log("process %i codes" % cnt)
	pl.log(tbl + " done")

def temp_info(engine, codes):
	tbl = "fund_temp_info"
	temp = []
	pl.log(tbl + " start...")
	cnt = 0
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.get_fund_info(code)
			df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			print e
			pl.log(tbl + " error for " + code)
			if 'timed out' in str(e):
				temp.append(code)
		cnt += 1
		if cnt % pc.FUND_GC_NUM is 0:
			pl.log("process %i codes" % cnt)
			df.to_sql(tbl,engine,if_exists='append')
			del df
			gc.collect()
			df = pd.DataFrame()
	if df is not None:
		df.to_sql(tbl,engine,if_exists='append')
	pl.log(tbl + " done")
	if len(temp) != 0:
		temp_info(engine, temp)

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

def nav_history(engine, code, ismonetary, sdate, edate):
	tbl = "fund_nav_history"
	# pl.log(tbl + " start...")
	try:
		df = ts.get_nav_history(code, ismonetary, str(sdate), str(edate))
		if df is not None:
			df['symbol'] = code
			df.to_sql(tbl,engine,if_exists='append')
		# print
		# pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error for " + code)
