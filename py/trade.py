import tushare as ts
import datetime
import tslog as tsl
import tsutil as tsu
import pandas as pd
import tsconf as tsc
import multiprocessing
import os

def history(engine, session, sdate, edate):
	trade_hist_mult(engine, session, str(sdate), str(edate))
	# it takes too much time...
	# trade_block_mult(engine, session, sdate, edate)

def history_stock(engine, session, code):
	tsl.log("get data for code : " + code + " start...")
	sdate = datetime.date(2013, 1, 1)
	edate = datetime.date.today()
	df = ts.get_k_data(code, start=str(sdate), end=str(edate))
	df.to_csv('/home/data/s_' + code + '.csv',columns=['date','open','close','high','low','volume'])
	tsl.log("get data for code : " + code + " done")

def daily(engine, session, cdate):
	if not tsu.is_holiday(cdate):
		tsl.log("trade_index_today start...")
		try:
			df = ts.get_index()
			df = df.set_index('code', drop='true')
			df['date'] = cdate
			df.to_sql('trade_index_today', engine, if_exists='append')
			tsl.log("trade_index_today done")
		except BaseException, e:
			print e
			tsl.log("trade_index_today error")
		
		tsl.log("trade_market_today start...")
		try:
			df = ts.get_today_all()
			df = df.set_index('code', drop='true')
			df['date'] = cdate
			df.to_sql('trade_market_today', engine, if_exists='append')
			print
			tsl.log("trade_market_today done")
		except BaseException, e:
			print
			print e
			tsl.log("trade_market_today error")
		
		trade_block_mult(engine, session, cdate, cdate)
	else:
		tsl.log("today is a holiday")
	
def trade_hist_mult(engine, session, sdate, edate):
	tsl.log("trade_market_history start...")
	codes = tsu.get_stock_codes(session)
	pn = len(codes) / tsc.TRADE_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[tsc.TRADE_PROCESS_NUM * i : tsc.TRADE_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = trade_hist_worker, args=(engine, temp, sdate, edate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	tsl.log("trade_market_history done")
	
def trade_hist_worker(engine, codes, sdate, edate):
	pid = os.getpid()
	tsl.log("pid %i start with %i codes..." % (pid, len(codes)))
	for code in codes:
		try:
			df = ts.get_k_data(code, start=str(sdate), end=str(edate))
			df = df.set_index('code', drop='true')
			df.to_sql('trade_market_history', engine, if_exists='append')
		except BaseException, e:
			print e
			tsl.log("pid %i error for %s" % (pid, code))
	tsl.log("pid %i done with %i codes" % (pid, len(codes)))
	
def trade_block_mult(engine, session, sdate, edate):
	tsl.log("trade_block start...")
	codes = tsu.get_stock_codes(session)
	pn = len(codes) / tsc.TRADE_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[tsc.TRADE_PROCESS_NUM * i : tsc.TRADE_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = trade_block_worker, args=(engine, temp, sdate, edate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	tsl.log("trade_block done")
	
def trade_block_worker(engine, codes, sdate, edate):
	pid = os.getpid()
	tsl.log("pid %i start with %i codes..." % (pid, len(codes)))
	df = pd.DataFrame()
	cdate = sdate
	temp = {}
	while cdate <= edate:
		if not tsu.is_holiday(cdate):
			for code in codes:
				try:
					newdf = ts.get_sina_dd(code, cdate, vol=10000)
					if newdf is not None:
						newdf['date'] = cdate
						df = df.append(newdf, ignore_index=True)
				except BaseException, e:
					if 'timed out' in str(e) or 'urlopen error' in str(e):
						temp.setdefault(cdate, [])
						temp[cdate].append(code)
						pass
					else:
						print e
						tsl.log("pid %i error for %s on %s" % (pid, code, str(cdate)))
			if len(df) != 0:
				df = df.set_index('code', drop='true')
				df.to_sql('trade_block',engine,if_exists='append')
		cdate += datetime.timedelta(days=1)
	for ddate in temp:
		trade_block_worker(engine, temp[ddate], ddate, ddate)
	tsl.log("pid %i done with %i codes" % (pid, len(codes)))
