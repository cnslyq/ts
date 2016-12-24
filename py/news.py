import tushare as ts
import pylog as pl
import pyutil as pu
import datetime
import pandas as pd
import pyconfig as pc
import multiprocessing
import os

def real(engine, session):
	news_real(engine)
	
def daily(engine, session, cdate):
	news_notices_mult(engine, session, str(cdate))
	news_sina_bar(engine)
	
def news_real(engine):
	tbl = "news_real"
	pl.log(tbl + " start...")
	df = ts.get_latest_news()
	st = datetime.datetime.today()
	et = st - datetime.timedelta(hours=2)
	st = '%i-%i %02i:00' % (st.month, st.day, st.hour)
	et = '%i-%i %02i:00' % (et.month, et.day, et.hour)
	df = df[df.time >= et]
	df = df[df.time < st]
	urls = df.url.values
	contents = ['' for i in range(len(df))]
	for i in range(len(df)):
		if 'blog.sina.com.cn' in urls[i]:
			continue
		content = ts.latest_content(urls[i])
		if content is not None:
			try:
				contents[i] = unicode(content)#.encode('raw_unicode_escape').decode('utf8')
			except BaseException, e:
				print e
				print urls[i]
	df['content'] = contents
	df = df.sort_values('time')
	df = df.set_index('time', drop='true')
	df.to_sql(tbl,engine,if_exists='append')
	pl.log(tbl + " done")
	
def news_notices_mult(engine, session, ddate):
	pl.log("news_notices start...")
	codes = pu.get_stock_codes(session)
	pn = len(codes) / pc.NEWS_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[pc.NEWS_PROCESS_NUM * i : pc.NEWS_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = news_notices_worker, args=(engine, temp, ddate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	pl.log("news_notices done")
	
def news_notices_worker(engine, codes, ddate):
	pid = os.getpid()
	pl.log("pid %i start with %i codes..." % (pid, len(codes)))
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.get_notices(code, ddate, True)
			if newdf is not None:
				newdf['code'] = code
				df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			print e
			pl.log("pid %i error for %s" % (pid, code))
	if len(df) != 0:
		df = df.set_index('code', drop='true')
		df.to_sql('news_notices',engine,if_exists='append')
	pl.log("pid %i done with %i codes" % (pid, len(codes)))
	
def news_sina_bar(engine):
	tbl = "news_sina_bar"
	pl.log(tbl + " start...")
	df = ts.guba_sina(True)
	df = df.set_index('ptime', drop='true')
	df.to_sql(tbl,engine,if_exists='append')
	pl.log(tbl + " done")
	