import tushare as ts
import pylog as pl

def daily(engine, session, cdate):
	tbl = "futures_ifs"
	pl.log(tbl + " start...")
	try:
		df = ts.get_intlfuture()
		df['date'] = code
		df.to_sql(tbl,engine,if_exists='append')
		pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error")


