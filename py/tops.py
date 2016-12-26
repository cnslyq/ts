import tushare as ts
import datetime
import pylog as pl
import pyutil as pu

def history(engine, session, sdate, edate):
	cdate = sdate
	pl.log("tops_list start...")
	while cdate <= edate:
		if not pu.is_holiday(cdate):
			try:
				df = ts.top_list(str(cdate))
				if df is not None:
					df = df.set_index('code', drop='true')
					df.to_sql('tops_list',engine,if_exists='append')
			except BaseException, e:
				print e
				pl.log("tops_list error on " + str(cdate))
		cdate += datetime.timedelta(days=1)
	pl.log("tops_list done")

def weekly(engine, session, cdate):
	tops(engine, 5)
	sdate = cdate - datetime.timedelta(days=4)
	edate = cdate
	history(engine, session, sdate, edate)

def monthly(engine, session, year, month):
	tops(engine, 30)

def tops(engine, freq):
	today = datetime.date.today()
	
	pl.log("tops_stock start...")
	try:
		df = ts.cap_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('code', drop='true')
		df.to_sql('tops_stock',engine,if_exists='append')
		print
		pl.log("tops_stock done")
	except BaseException, e:
		print
		print e
		pl.log("tops_stock error")
	
	pl.log("tops_broker start...")
	try:
		df = ts.broker_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('date', drop='true')
		df.to_sql('tops_broker',engine,if_exists='append')
		print
		pl.log("tops_broker done")
	except BaseException, e:
		print
		print e
		pl.log("tops_broker error")
	
	pl.log("tops_inst_seat start...")
	try:
		df = ts.inst_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('code', drop='true')
		df.to_sql('tops_inst_seat',engine,if_exists='append')
		print
		pl.log("tops_inst_seat done")
	except BaseException, e:
		print
		print e
		pl.log("tops_inst_seat error")
	
	# TBD
	# no data, should be a bug
	'''
	if freq == 5:
		pl.log("tops_inst_detail start...")
		try:
			df = ts.inst_detail()
			df = df.set_index('code', drop='true')
			df.to_sql('tops_inst_detail', engine, if_exists='append')
			print
			pl.log("tops_inst_detail done")
		except BaseException, e:
			print
			print e
			pl.log("tops_inst_detail error")
	'''
