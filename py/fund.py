import tushare as ts
import datetime
import tslog as tsl
import tsutil as tsu
import pandas as pd
import tsconf as tsc
import multiprocessing
import os

def init(engine, session):
	temp_info_mult(engine)
	# update fund_temp_info to fund_info
	tsl.log("call update_fund_info start...")
	session.execute('call update_fund_info')
	tsl.log("call update_fund_info done")
	
def daily(engine, session, cdate):
	nav_open(engine, cdate)
	ddate = cdate - datetime.timedelta(days=1)
	nav_close(engine, ddate)
	nav_grading(engine, ddate)

def monthly(engine, session, year, month):
	sdate=datetime.date(year, month, 1)
	edate=datetime.date.today() - datetime.timedelta(days=1)
	history(engine, session, sdate, edate)

def quarterly(engine, session, year, quarterly):
	init(engine, session)
	
def history(engine, session, sdate, edate):
	fund_nav_history_mult(engine, session, str(sdate), str(edate))

def fund_nav_history_mult(engine, session, sdate, edate):
	tbl = "fund_nav_history"
	tsl.log(tbl + " start...")
	codes = tsu.get_fund_codes(session)
	pn = len(codes) / tsc.FUND_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[tsc.FUND_PROCESS_NUM * i : tsc.FUND_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = fund_nav_history_worker, args=(engine, temp, sdate, edate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	tsl.log(tbl + " done")
	
def fund_nav_history_worker(engine, codes, sdate, edate):
	pid = os.getpid()
	tsl.log("pid %i start with %i codes..." % (pid, len(codes)))
	temp = []
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.get_nav_history(code[0], code[1], sdate, edate)
			if newdf is not None:
				newdf['symbol'] = code[0]
				df = df.append(newdf)
		except BaseException, e:
			if 'timed out' in str(e) or 'urlopen error' in str(e):
				temp.append(code)
			else:
				print e
				tsl.log("pid %i error for %s" % (pid, code))
	if len(df) != 0:
		df.to_sql('fund_nav_history',engine,if_exists='append')
	if len(temp) != 0:
		fund_nav_history_worker(engine, temp, sdate, edate)
	tsl.log("pid %i done with %i codes" % (pid, len(codes)))
	
def history_fund(engine, session, code):
	tsl.log("get data for code : " + code + " start...")
	sdate = datetime.date(2013, 1, 1)
	edate = datetime.date.today()
	df = ts.get_nav_history(code, start=str(sdate), end=str(edate))
	df.to_csv('/home/data/f_' + code + '.csv')
	tsl.log("get data for code : " + code + " done")

def temp_info_mult(engine):
	# get latest codes
	tsl.log("get latest codes start...")
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
	tsl.log("get latest codes done")
	
	# insert latest info into fund_temp_info
	session.execute("delete from fund_temp_info")
	tsl.log("fund_temp_info start...")
	pn = len(codes) / tsc.FUND_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[tsc.FUND_PROCESS_NUM * i : tsc.FUND_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = temp_info_worker, args=(engine, temp))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	tsl.log("fund_temp_info done")
	
def temp_info_worker(engine, codes):
	pid = os.getpid()
	tsl.log("pid %i start with %i codes..." % (pid, len(codes)))
	temp = []
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.get_fund_info(code)
			df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			if 'timed out' in str(e) or 'urlopen error' in str(e):
				temp.append(code)
			else:
				print e
				tsl.log("pid %i error for %s" % (pid, code))
	if len(df) != 0:
		df['pid'] = pid
		df.to_sql('fund_temp_info',engine,if_exists='append')
	if len(temp) != 0:
		temp_info_worker(engine, temp)
	tsl.log("pid %i done with %i codes" % (pid, len(codes)))

def nav_open(engine, cdate):
	tbl = "fund_nav_open"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_nav_open()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")

def nav_close(engine, cdate):
	tbl = "fund_nav_close"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_nav_close()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")

def nav_grading(engine, cdate):
	tbl = "fund_nav_grading"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_nav_grading()
		df = df.set_index('symbol', drop='true')
		df = df[df.nav_date==str(cdate)]
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
