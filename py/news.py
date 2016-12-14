import tushare as ts
import pylog as pl
import datetime

def real(engine, session):
	news_real(engine)
	
def news_real(engine):
	tbl = "news_real"
	pl.log(tbl + " start...")
	try:
		df = ts.get_latest_news()
		st = datetime.datetime.today()
		et = st - datetime.timedelta(hours=2)
		st = '%i-%i %i:00' % (st.month, st.day, st.hour)
		et = '%i-%i %i:00' % (et.month, et.day, et.hour)
		df = df[df.time >= et]
		df = df[df.time < st]
		df = df.set_index('time', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error")
