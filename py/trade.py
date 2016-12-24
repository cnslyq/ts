import tushare as ts
import datetime
import pylog as pl
import pyutil as pu
import pandas as pd
import pyconfig as pc
import multiprocessing
import os

def history(engine, session, sdate, edate):
	codes = pu.get_stock_codes(session)
	cnt = 0
	for code in codes:
		# pl.log("processs code : " + code)
		try:
			df = ts.get_k_data(code, start=str(sdate), end=str(edate))
			df = df.set_index('code', drop='true')
			df.to_sql('trade_market_history', engine, if_exists='append')
		except BaseException, e:
			print e
			pl.log("trade_market_history error for %s" % code)
		cnt += 1
		if cnt % pc.TRADE_PROCESS_NUM is 0:
			pl.log("process %i codes" % cnt)
	trade_block_mult(engine, codes, sdate, edate)

def history_stock(engine, session, code):
	pl.log("get data for code : " + code + " start...")
	sdate = datetime.date(2013, 1, 1)
	edate = datetime.date.today()
	df = ts.get_k_data(code, start=str(sdate), end=str(edate))
	df.to_csv('/home/data/s_' + code + '.csv',columns=['date','open','close','high','low','volume'])
	pl.log("get data for code : " + code + " done")

def daily(engine, session, cdate):
	if not pu.is_holiday(cdate):
		pl.log("trade_index_today start...")
		try:
			df = ts.get_index()
			df = df.set_index('code', drop='true')
			df['date'] = cdate
			df.to_sql('trade_index_today', engine, if_exists='append')
			pl.log("trade_index_today done")
		except BaseException, e:
			print e
			pl.log("trade_index_today error")
		
		pl.log("trade_market_today start...")
		try:
			df = ts.get_today_all()
			df = df.set_index('code', drop='true')
			df['date'] = cdate
			df.to_sql('trade_market_today', engine, if_exists='append')
			print
			pl.log("trade_market_today done")
		except BaseException, e:
			print
			print e
			pl.log("trade_market_today error")
		
		codes = pu.get_stock_codes(session)
		trade_block_mult(engine, codes, cdate, cdate)
	else:
		pl.log("today is a holiday")

def trade_block_mult(engine, codes, sdate, edate):
	pl.log("trade_block start...")
	pn = len(codes) / pc.TRADE_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[pc.TRADE_PROCESS_NUM * i : pc.TRADE_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = trade_block_worker, args=(engine, temp, sdate, edate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	pl.log("trade_block done")
	
def trade_block_worker(engine, codes, sdate, edate):
	pid = os.getpid()
	pl.log("pid %i start with %i codes..." % (pid, len(codes)))
	df = pd.DataFrame()
	cdate = sdate
	while cdate <= edate:
		if not pu.is_holiday(cdate):
			temp = []
			for code in codes:
				try:
					newdf = ts.get_sina_dd(code, cdate, vol=10000)
					if newdf is not None:
						newdf['date'] = cdate
						df = df.append(newdf, ignore_index=True)
				except BaseException, e:
					if 'timed out' in str(e) or 'urlopen error' in str(e):
						temp.append(code)
					else:
						print e
						pl.log("pid %i error for %s on %s" % (pid, code, str(cdate)))
			if len(df) != 0:
				df = df.set_index('code', drop='true')
				df.to_sql('trade_block',engine,if_exists='append')
			if len(temp) != 0:
				trade_block_worker(engine, temp, cdate, cdate)
			cdate += datetime.timedelta(days=1)
	pl.log("pid %i done with %i codes" % (pid, len(codes)))
