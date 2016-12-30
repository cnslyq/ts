import tushare as ts
import datetime
import tslog as tsl
import tsutil as tsu
import pandas as pd
import multiprocessing
import os

def history(engine, session, sdate, edate):
	tops_list_mult(engine, sdate, edate)
	
def tops_list_mult(engine, sdate, edate):
	tsl.log("tops_list start...")
	ps = []
	dayno = 10
	pn = (edate - sdate).days / dayno + 1
	sd = sdate
	ed = sd + datetime.timedelta(days=dayno-1)
	for i in range(pn):
		if i == pn - 1:
			ed = edate
		p = multiprocessing.Process(target = tops_list_worker, args=(engine, sd, ed))
		p.daemon = True
		p.start()
		ps.append(p)
		sd = ed + datetime.timedelta(days=1)
		ed += datetime.timedelta(days=dayno)
	for p in ps:
		p.join()
	tsl.log("tops_list done")
	
def tops_list_worker(engine, sdate, edate):
	pid = os.getpid()
	tsl.log("pid %i start with %s ~ %s..." % (pid, str(sdate), str(edate)))
	cdate = sdate
	df = pd.DataFrame()
	while cdate <= edate:
		if not tsu.is_holiday(cdate):
			try:
				newdf = ts.top_list(str(cdate))
				if df is not None:
					df = df.append(newdf, ignore_index=True)
			except BaseException, e:
				print e
				tsl.log("pid %i error on %s" % (pid, str(cdate)))
		cdate += datetime.timedelta(days=1)
	if len(df) != 0:
		df = df.set_index('code', drop='true')
		df.to_sql('tops_list',engine,if_exists='append')
	tsl.log("pid %i done with %s ~ %s" % (pid, str(sdate), str(edate)))

def weekly(engine, session, cdate):
	if 5 == cdate.isoweekday():
		tops(engine, 5)
	elif 1 == cdate.isoweekday():
		sdate = cdate - datetime.timedelta(days=7)
		edate = cdate - datetime.timedelta(days=3)
		history(engine, session, sdate, edate)
	else:
		tsl.log("no weekly task for module : tops")

def monthly(engine, session, year, month):
	tops(engine, 30)

def tops(engine, freq):
	today = datetime.date.today()
	
	tsl.log("tops_stock start...")
	try:
		df = ts.cap_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('code', drop='true')
		df.to_sql('tops_stock',engine,if_exists='append')
		print
		tsl.log("tops_stock done")
	except BaseException, e:
		print
		print e
		tsl.log("tops_stock error")
	
	tsl.log("tops_broker start...")
	try:
		df = ts.broker_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('date', drop='true')
		df.to_sql('tops_broker',engine,if_exists='append')
		print
		tsl.log("tops_broker done")
	except BaseException, e:
		print
		print e
		tsl.log("tops_broker error")
	
	tsl.log("tops_inst_seat start...")
	try:
		df = ts.inst_tops(freq)
		df['date'] = today
		df['freq'] = freq
		df = df.set_index('code', drop='true')
		df.to_sql('tops_inst_seat',engine,if_exists='append')
		print
		tsl.log("tops_inst_seat done")
	except BaseException, e:
		print
		print e
		tsl.log("tops_inst_seat error")
	
	# TBD
	# no data, should be a bug
	'''
	if freq == 5:
		tsl.log("tops_inst_detail start...")
		try:
			df = ts.inst_detail()
			df = df.set_index('code', drop='true')
			df.to_sql('tops_inst_detail', engine, if_exists='append')
			print
			tsl.log("tops_inst_detail done")
		except BaseException, e:
			print
			print e
			tsl.log("tops_inst_detail error")
	'''
