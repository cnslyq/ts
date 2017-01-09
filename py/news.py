import tushare as ts
import tslog as tsl
import tsutil as tsu
import datetime
import pandas as pd
import tsconf as tsc
import multiprocessing
import os

def real(engine, session):
	news_real(engine)
	
def daily(engine, session, cdate):
	news_notices_mult(engine, session, str(cdate))
	news_sina_bar(engine)
	
def news_real(engine):
	tbl = "news_real"
	tsl.log(tbl + " start...")
	df = ts.get_latest_news()
	if df is None:
		tsl.log("no latest news")
		return
	st = datetime.datetime.today()
	et = st - datetime.timedelta(hours=2)
	st = '%02i-%02i %02i:00' % (st.month, st.day, st.hour)
	et = '%02i-%02i %02i:00' % (et.month, et.day, et.hour)
	df = df[df.time >= et]
	df = df[df.time < st]
	urls = df.url.values
	contents = ['' for i in range(len(df))]
	for i in range(len(df)):
		if 'blog.sina.com.cn' in urls[i]:
			continue
		try:
			content = ts.latest_content(urls[i])
			if content is not None:
				contents[i] = unicode(content)#.encode('raw_unicode_escape').decode('utf8')
		except BaseException, e:
			print e
			print urls[i]
	df['content'] = contents
	df = df.sort_values('time')
	df = df.set_index('time', drop='true')
	df.to_sql(tbl,engine,if_exists='append')
	tsl.log(tbl + " done")
	
def news_notices_mult(engine, session, ddate):
	tsl.log("news_notices start...")
	codes = tsu.get_stock_codes(session)
	pn = len(codes) / tsc.NEWS_PROCESS_NUM + 1
	ps = []
	for i in range(pn):
		temp = codes[tsc.NEWS_PROCESS_NUM * i : tsc.NEWS_PROCESS_NUM * (i + 1)]
		p = multiprocessing.Process(target = news_notices_worker, args=(engine, temp, ddate))
		p.daemon = True
		p.start()
		ps.append(p)
	for p in ps:
		p.join()
	tsl.log("news_notices done")
	
def news_notices_worker(engine, codes, ddate):
	pid = os.getpid()
	tsl.log("pid %i start with %i codes..." % (pid, len(codes)))
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.get_notices(code, ddate, True)
			if newdf is not None:
				newdf['code'] = code
				df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			print e
			tsl.log("pid %i error for %s" % (pid, code))
	if len(df) != 0:
		df = df.set_index('code', drop='true')
		df.to_sql('news_notices',engine,if_exists='append')
	tsl.log("pid %i done with %i codes" % (pid, len(codes)))
	
def news_sina_bar(engine):
	tbl = "news_sina_bar"
	tsl.log(tbl + " start...")
	df = ts.guba_sina(True)
	df = df.set_index('ptime', drop='true')
	df.to_sql(tbl,engine,if_exists='append')
	tsl.log(tbl + " done")
	