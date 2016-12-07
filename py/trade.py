import tushare as ts
import datetime
import pylog as pl
import pyutil as pu

def history(engine, session, sdate, edate):
	codes = pu.get_codes(session)
	for code in codes:
		pl.log("processs code : " + code)
		df = ts.get_k_data(code, start=str(sdate))
		if df is not None:
			df = df.set_index('code', drop='true')
			df.to_sql('trade_market_history', engine, if_exists='append')
		cdate = sdate
		while cdate < edate:
			if not ts.is_holiday(str(cdate)):
				df = ts.get_sina_dd(code, cdate, vol=5000)
				if df is not None:
					df = df.set_index('code', drop='true')
					df['date'] = cdate
					df.to_sql('trade_block', engine, if_exists='append')
			cdate += datetime.timedelta(days=1)

def daily(engine, session):
	today = datetime.date.today()
	# if not ts.is_holiday(str(today)):
	if True:
		pl.log("trade_index_today start...")
		df = ts.get_index()
		df = df.set_index('code', drop='true')
		df['date'] = today
		df.to_sql('trade_index_today', engine, if_exists='append')
		pl.log("trade_index_today done")

		pl.log("trade_market_today start...")
		df = ts.get_today_all()
		df = df.set_index('code', drop='true')
		df['date'] = today
		df.to_sql('trade_market_today', engine, if_exists='append')
		print
		pl.log("trade_market_today done")
		
		pl.log("trade_block start...")
		codes = pu.get_codes(session)
		for code in codes:
			df = ts.get_sina_dd(code, today, vol=5000)
			if df is not None:
				df = df.set_index('code', drop='true')
				df['date'] = today
				df.to_sql('trade_block', engine, if_exists='append')
		pl.log("trade_block done")
	else:
		pl.log("today is a holiday")


