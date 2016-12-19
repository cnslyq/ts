import tushare as ts
import datetime
import pylog as pl
import pyutil as pu
import gc
import pandas as pd
import pyconfig as pc

def history(engine, session, sdate, edate):
	margin_sh_smry(engine, str(sdate), str(edate))
	# no data, should be a bug
	# margin_sh_dtl(engine, str(sdate), str(edate))
	margin_sz_smry(engine, str(sdate), str(edate))
	cdate = sdate
	while cdate <= edate:
		if not pu.is_holiday(cdate):
			margin_sz_dtl(engine, str(cdate), log=False)
		cdate += datetime.timedelta(days=1)
	
def history_m(engine, session, year, month):
	lifted(engine, year, month)

def history_q(engine, session, year, quarter):
	forecast_history(engine, year, quarter)
	fund_hold(engine, year, quarter)

def history_a(engine, session):
	top10_holders(engine, session)

def daily(engine, session, cdate):
	ddate = cdate - datetime.timedelta(days=1)
	if not pu.is_holiday(ddate):
		ddate = str(ddate)
		margin_sh_smry(engine, ddate, ddate)
		# no data, should be a bug
		# margin_sh_dtl(engine, ddate, ddate)
		margin_sz_smry(engine, ddate, ddate)
		margin_sz_dtl(engine, ddate)
	else:
		pl.log("yesterday is a holiday")
	
def weekly(engine, session, cdate):
	today = datetime.date.today()
	forecast(engine, today.year, (today.month - 1) / 3 + 1)
	
def monthly(engine, session, year, month):
	lifted(engine, year, month)
	new_stock(engine)
	
def quarterly(engine, session, year, quarter):
	history_q(engine, session, year, quarter)
	top10_holders(engine, session, year, quarter)
	
def top10_holders(engine, session, year=None, quarter=None):
	tbl = "invest_top10_holders"
	pl.log(tbl + " start...")
	codes = pu.get_stock_codes(session)
	cnt = 0
	df = pd.DataFrame()
	for code in codes:
		try:
			newdf = ts.top10_holders(code, year, quarter)[1]
			newdf['code'] = code
			df = df.append(newdf, ignore_index=True)
		except BaseException, e:
			print e
			pl.log(tbl + " error for " + code)
		cnt += 1
		if cnt % pc.INVEST_GC_NUM is 0:
			df = df.set_index('code', drop='true')
			df.to_sql(tbl, engine, if_exists='append')
			pl.log("process %i codes" % cnt)
			del df
			gc.collect()
			df = pd.DataFrame()
	if df is not None:
		df = df.set_index('code', drop='true')
		df.to_sql(tbl, engine, if_exists='append')
	pl.log(tbl + " done")

def margin_sh_smry(engine, sdate, edate):
	tbl = "invest_margin_sh_smry"
	pl.log(tbl + " start...")
	try:
		df = ts.sh_margins(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")

def margin_sh_dtl(engine, sdate, edate):
	tbl = invest_margin_sh_dtl
	pl.log(tbl + " start...")
	try:
		df = ts.sh_margin_details(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error")
		
def margin_sz_smry(engine, sdate, edate):
	tbl = "invest_margin_sz_smry"
	pl.log(tbl + " start...")
	try:
		df = ts.sz_margins(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
		
def margin_sz_dtl(engine, ddate, log=True):
	tbl = "invest_margin_sz_dtl"
	if(log):
		pl.log(tbl + " start...")
	try:
		df = ts.sz_margin_details(ddate)
		df = df.set_index('opDate', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		if(log):
			pl.log(tbl + " done")
	except BaseException, e:
		print e
		pl.log(tbl + " error")
		
def lifted(engine, year, month):
	# pu.to_sql(engine, 'invest_lifted', plist=[year, month])
	tbl = "invest_lifted"
	pl.log(tbl + " start...")
	try:
		df = ts.xsg_data(year, month)
		df = df.set_index('code', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
		
def new_stock(engine):
	tbl = "invest_new_stock"
	pl.log(tbl + " start...")
	try:
		df = ts.new_stocks()
		df['date'] = datetime.date.today()
		df = df.set_index('code', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
		
def forecast(engine, year, quarter):
	tbl = "invest_forecast"
	pl.log(tbl + " start...")
	try:
		df = ts.forecast_data(year, quarter)
		if len(df) != 0:
			df['year'] = year
			df['quarter'] = quarter
			# df = df.set_index('code', drop='true')
			df = df.reset_index()
			df.to_sql(tbl,engine,if_exists='replace')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
		
def forecast_history(engine, year, quarter):
	tbl = "invest_forecast_history"
	pl.log(tbl + " start...")
	try:
		df = ts.forecast_data(year, quarter)
		df['year'] = year
		df['quarter'] = quarter
		df = df.set_index('code', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
		
def fund_hold(engine, year, quarter):
	tbl = "invest_fund_hold"
	pl.log(tbl + " start...")
	try:
		df = ts.fund_holdings(year, quarter)
		df = df.set_index('code', drop='true')
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
