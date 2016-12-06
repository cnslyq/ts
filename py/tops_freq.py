import tushare as ts
import datetime
import pylog as pl

def tops(freq, engine):
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
