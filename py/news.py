import tushare as ts
import pylog as pl
import pyutil as pu
import datetime
import traceback

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
				contents = ['' for i in range(len(df))]
				titles = df.title.values
				types = df.type.values
				for i in range(len(df)):
					content = ts.notice_content(urls[i])
					if content is not None:
						contents[i] = content.encode('utf8')
					titles[i] = titles[i].encode('utf8')
					types[i] = types[i].encode('utf8')
				df['content'] = contents
				df['title'] = titles
				df['type'] = types
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
				contents[i] = content.encode('raw_unicode_escape')#.decode('utf8')
			# except UnicodeDecodeError:
			# 	pass
			except BaseException, e:
				# print e
				# pl.log(tbl + " error for " + urls[i])
				print i
				print urls[i]
				traceback.print_exc()
	df['content'] = contents
	df = df.sort_values('time')
	df = df.set_index('time', drop='true')
	df.to_sql(tbl,engine,if_exists='append')
	pl.log(tbl + " done")
