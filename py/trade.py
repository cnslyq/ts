import tushare as ts
import datetime
import pylog as pl
import pyutil as pu

def history(engine, session, sdate, edate):
	codes = pu.get_codes(session)
	cnt = 0
	for code in codes:
		# pl.log("processs code : " + code)
		try:
			df = ts.get_k_data(code, start=str(sdate), end=str(edate))
			if df is not None:
				df = df.set_index('code', drop='true')
				df.to_sql('trade_market_history', engine, if_exists='append')
		except BaseException, e:
			print e
			pl.log("trade_market_history error for %s" % code)
		
		cdate = sdate
		while cdate <= edate:
			if pu.is_tddate(session, cdate):
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
		cnt += 1
		if cnt % 100 == 0:
			pl.log("process %i codes" % cnt)

def daily(engine, session, cdate):
	if pu.is_tddate(session, cdate):
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
		codes = pu.get_codes(session)
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


