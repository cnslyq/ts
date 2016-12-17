import tushare as ts
import datetime
import pylog as pl
import pyutil as pu
import gc
import pandas as pd
import pyconfig as pc

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
		'''
		cdate = sdate
		while cdate <= edate:
			if not pu.is_holiday(cdate):
				try:
					df = ts.get_sina_dd(code, cdate, vol=10000)
					if df is not None:
						df = df.set_index('code', drop='true')
						df['date'] = cdate
						df.to_sql('trade_block', engine, if_exists='append')
				except BaseException, e:
					print e
					pl.log("trade_block error for %s on %s" % (code, str(cdate)))
			cdate += datetime.timedelta(days=1)
		'''
		cnt += 1
		if cnt % pc.TRADE_GC_NUM is 0:
			pl.log("process %i codes" % cnt)

def history_s(engine, session, code, year):
	pl.log("get data for code : " + code + " year : " + year + " start...")
	sdate = datetime.date(int(year), 1, 1)
	edate = datetime.date(int(year), 12, 31)
	df = ts.get_k_data(code, start=str(sdate), end=str(edate))
	df.to_csv('/home/data/' + code + '_' + year + '.csv',columns=['date','open','close','high','low','volume'])
	pl.log("get data for code : " + code + " year : " + year + " done")

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
		
		pl.log("trade_block start...")
		codes = pu.get_stock_codes(session)
		for code in codes:
			try:
				df = ts.get_sina_dd(code, cdate, vol=10000)
				if df is not None:
					df = df.set_index('code', drop='true')
					df['date'] = cdate
					df.to_sql('trade_block', engine, if_exists='append')
			except BaseException, e:
				print e
				pl.log("trade_block error for " + code)
		pl.log("trade_block done")
	else:
		pl.log("today is a holiday")


