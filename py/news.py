import tushare as ts
import pylog as pl
import pyutil as pu
import datetime

def real(engine, session):
	news_real(engine)
	
def daily(engine, session, cdate):
	tbl = "news_notices"
	pl.log(tbl + " start...")
	ddate = str(cdate)
	codes = pu.get_stock_codes(session)
	cnt = 0
	for code in codes:
		# pl.log("process code : " + code)
		try:
			df = ts.get_notices(code, ddate)
			if df is not None:
				df['code'] = code
				df['content'] = ''
				urls = df.url.values
				titles = df.title.values
				types = df.type.values
				for i in range(len(df)):
					df['content'][i] = ts.notice_content(urls[i]).encode('utf8')
					df['title'][i] = titles[i].encode('utf8')
					df['type'][i] = types[i].encode('utf8')
				df = df.set_index('date', drop='true')
				df.to_sql(tbl,engine,if_exists='append')
		except BaseException, e:
			print e
			pl.log(tbl + " error for " + code)
		cnt += 1
		if cnt % 100 is 0:
			pl.log("process %i codes" % cnt)
	pl.log(tbl + " done")
	
def news_real(engine):
	tbl = "news_real"
	pl.log(tbl + " start...")
	try:
		df = ts.get_latest_news()
		st = datetime.datetime.today()
		et = st - datetime.timedelta(hours=2)
		st = '%i-%i %02i:00' % (st.month, st.day, st.hour)
		et = '%i-%i %02i:00' % (et.month, et.day, et.hour)
		df = df[df.time >= et]
		df = df[df.time < st]
		df['content'] = ''
		urls = df.url.values
		for i in range(len(df)):
			df['content'][i] = ts.latest_content(urls[i])
		df = df.sort_values('time')
		df = df.set_index('time', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error")
