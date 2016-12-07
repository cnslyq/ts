import tushare as ts
import datetime
import pylog as pl

def history(engine, session, sdate, edate):
	cdate = sdate
	pl.log("tops_list start...")
	while cdate < edate:
		if not ts.is_holiday(str(cdate)):
			df = ts.top_list(str(cdate))
			if df is not None:
				df = df.set_index('code', drop='true')
				df.to_sql('tops_list',engine,if_exists='append')
		cdate += datetime.timedelta(days=1)
	pl.log("tops_list done")

def daily(engine, session):
	'''
	curr date	data date
	Monday
	Tuesday		last Friday
	Wednesday
	Thursday
	Friday
	Saturday
	Sunday
	'''
	ddate = datetime.date.today() - datetime.timedelta(days=7)
	pl.log("tops_list start...")
	df = ts.top_list(str(ddate))
	df = df.set_index('code', drop='true')
	df.to_sql('tops_list',engine,if_exists='append')
	pl.log("tops_list done")

def weekly(engine, session):
	tops(engine, 5)

def monthly(engine, session):
	tops(engine, 30)

def tops(engine, freq):
	today = datetime.date.today()
	
	pl.log("tops_stock start...")
	df = ts.cap_tops(freq)
	df['date'] = today
	df['freq'] = freq
	df = df.set_index('code', drop='true')
	df.to_sql('tops_stock',engine,if_exists='append')
	print
	pl.log("tops_stock done")
	
	pl.log("tops_broker start...")
	df = ts.broker_tops(freq)
	df['date'] = today
	df['freq'] = freq
	df = df.set_index('date', drop='true')
	df.to_sql('tops_broker',engine,if_exists='append')
	print
	pl.log("tops_broker done")
	
	pl.log("tops_inst_seat start...")
	df = ts.inst_tops(freq)
	df['date'] = today
	df['freq'] = freq
	df = df.set_index('code', drop='true')
	df.to_sql('tops_inst_seat',engine,if_exists='append')
	print
	pl.log("tops_inst_seat done")
	
	# TBD
	if freq == 5:
		pl.log("tops_inst_detail start...")
		df = ts.inst_detail()
		df = df.set_index('code', drop='true')
		df.to_sql('tops_inst_detail', engine, if_exists='append')
		print
		pl.log("tops_inst_detail done")