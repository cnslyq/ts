import tushare as ts
import tslog as tsl
import datetime

def daily(engine, session, cdate):
	futures_ifs(engine, cdate)
	if cdate.isoweekday() != 7:
		global_index(engine, cdate)
		day_boxoffice(engine, cdate)

def history_m(engine, session, year, month):
	ddate='%i-%.2i' % (year, month)
	month_boxoffice(engine, ddate)

def history_y(engine, session, year):
	shibor(engine, year)
	shibor_quote(engine, year)
	shibor_ma(engine, year)
	lpr(engine, year)
	lpr_ma(engine, year)

def monthly(engine, session, year, month):
	sdate = str(datetime.date(year, month, 1))
	shibor(engine, year, sdate)
	# shibor_quote(engine, year, sdate)
	shibor_ma(engine, year, sdate)
	lpr(engine, year, sdate)
	lpr_ma(engine, year, sdate)
	ddate='%i-%.2i' % (year, month)
	month_boxoffice(engine, ddate)

def day_boxoffice(engine, cdate):
	tbl = "day_boxoffice"
	tsl.log(tbl + " start...")
	try:
		df = ts.day_boxoffice()
		df['date'] = cdate - datetime.timedelta(days=1)
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")

def month_boxoffice(engine, ddate=None):
	tbl = "month_boxoffice"
	tsl.log(tbl + " start...")
	try:
		df = ts.month_boxoffice(ddate)
		df['date'] = ddate
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")

def shibor(engine, year, sdate=None):
	tbl = "shibor"
	tsl.log(tbl + " start...")
	try:
		df = ts.shibor_data(year)
		if sdate is not None:
			df = df[df.date >= sdate]
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")
	
# no 2016 data ??
def shibor_quote(engine, year, sdate=None):
	tbl = "shibor_quote"
	tsl.log(tbl + " start...")
	try:
		df = ts.shibor_quote_data(year)
		if sdate is not None:
			df = df[df.date >= sdate]
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")

def shibor_ma(engine, year, sdate=None):
	tbl = "shibor_ma"
	tsl.log(tbl + " start...")
	try:
		df = ts.shibor_ma_data(year)
		if sdate is not None:
			df = df[df.date >= sdate]
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")

def lpr(engine, year, sdate=None):
	tbl = "lpr"
	tsl.log(tbl + " start...")
	try:
		df = ts.lpr_data(year)
		if sdate is not None:
			df = df[df.date >= sdate]
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")
	
def lpr_ma(engine, year, sdate=None):
	tbl = "lpr_ma"
	tsl.log(tbl + " start...")
	try:
		df = ts.lpr_ma_data(year)
		if sdate is not None:
			df = df[df.date >= sdate]
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")
	
def futures_ifs(engine, cdate):
	tbl = "futures_ifs"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_intlfuture()
		df['date'] = cdate
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")

def global_index(engine, cdate):
	tbl = "global_index"
	tsl.log(tbl + " start...")
	try:
		df = ts.global_realtime()
		df['date'] = cdate
		df.to_sql(tbl,engine,if_exists='append')
		tsl.log(tbl + " done")
	except BaseException, e:
		print e
		tsl.log(tbl + " error")