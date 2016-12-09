import tushare as ts
import datetime
import pylog as pl
import pyutil as pu

def history(engine, session, sdate, edate):
	margin_sh_smry(engine, str(sdate), str(edate))
	margin_sh_dtl(engine, str(sdate), str(edate))
	margin_sz_smry(engine, str(sdate), str(edate))
	cdate = sdate
	while cdate <= edate:
		if pu.is_tddate(session, cdate):
			margin_sz_dtl(engine, str(cdate))
		cdate += datetime.timedelta(days=1)
	
def history_m(engine, session, year, month):
	lifted(engine, year, month)

def history_q(engine, session, year, quarter):
	quarterly(engine, session, year, quarter)

def daily(engine, session, cdate):
	ddate = cdate - datetime.timedelta(days=1)
	if pu.is_tddate(session, ddate):
		ddate = str(ddate)
		margin_sh_smry(engine, ddate, ddate)
		margin_sh_dtl(engine, ddate, ddate)
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
	forecast_history(engine, year, quarter)
	fund_hold(engine, year, quarter)

def margin_sh_smry(engine, sdate, edate):
	pl.log("invest_margin_sh_smry start...")
	try:
		df = ts.sh_margins(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sh_smry',engine,if_exists='append')
		print
		pl.log("invest_margin_sh_smry done")
	except BaseException, e:
		print
		print e
		pl.log("invest_margin_sh_smry error")

def margin_sh_dtl(engine, sdate, edate):
	pl.log("invest_margin_sh_dtl start...")
	try:
		df = ts.sh_margin_details(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sh_dtl',engine,if_exists='append')
		pl.log("invest_margin_sh_dtl done")
	except BaseException, e:
		print
		print e
		pl.log("invest_margin_sh_dtl error")
		
def margin_sz_smry(engine, sdate, edate):
	pl.log("invest_margin_sz_smry start...")
	try:
		df = ts.sz_margins(sdate, edate)
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sz_smry',engine,if_exists='append')
		pl.log("invest_margin_sz_smry done")
	except BaseException, e:
		print
		print e
		pl.log("invest_margin_sz_smry error")
		
def margin_sz_dtl(engine, ddate):
	pl.log("invest_margin_sz_dtl start...")
	try:
		df = ts.sz_margin_details(ddate)
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sz_dtl',engine,if_exists='append')
		print
		pl.log("invest_margin_sz_dtl done")
	except BaseException, e:
		print
		print e
		pl.log("invest_margin_sz_dtl error")
		
def lifted(engine, year, month):
	pu.to_sql(engine, 'invest_lifted', plist=[year, month])
	'''
	pl.log("invest_lifted start...")
	try:
		df = ts.xsg_data(year, month)
		df = df.set_index('code', drop='true')
		df.to_sql('invest_lifted',engine,if_exists='append')
		pl.log("invest_lifted done")
	except BaseException, e:
		print
		print e
		pl.log("invest_lifted error")
	'''
		
def new_stock(engine):
	pl.log("invest_new_stock start...")
	try:
		df = ts.new_stocks()
		df['date'] = datetime.date.today()
		df = df.set_index('code', drop='true')
		df.to_sql('invest_new_stock',engine,if_exists='append')
		print
		pl.log("invest_new_stock done")
	except BaseException, e:
		print
		print e
		pl.log("invest_new_stock error")
		
def forecast(engine, year, quarter):
	pl.log("invest_forecast start...")
	try:
		df = ts.forecast_data(year, quarter)
		df['year'] = year
		df['quarter'] = quarter
		df = df.set_index('code', drop='true')
		df.to_sql('invest_forecast',engine,if_exists='replace')
		print
		pl.log("invest_forecast done")
	except BaseException, e:
		print
		print e
		pl.log("invest_forecast error")
		
def forecast_history(engine, year, quarter):
	pl.log("invest_forecast_history start...")
	try:
		df = ts.forecast_data(year, quarter)
		df['year'] = year
		df['quarter'] = quarter
		df = df.set_index('code', drop='true')
		df.to_sql('invest_forecast_history',engine,if_exists='append')
		print
		pl.log("invest_forecast_history done")
	except BaseException, e:
		print
		print e
		pl.log("invest_forecast_history error")
		
def fund_hold(engine, year, quarter):
	pl.log("invest_fund_hold start...")
	try:
		df = ts.fund_holdings(year, quarter)
		df = df.set_index('code', drop='true')
		df.to_sql('invest_fund_hold',engine,if_exists='append')
		print
		pl.log("invest_fund_hold done")
	except BaseException, e:
		print
		print e
		pl.log("invest_fund_hold error")
