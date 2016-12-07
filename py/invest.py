import tushare as ts
import datetime
import pylog as pl

def history(engine, session, sdate, edate):
	margin_sh_smry(engine, sdate, edate)
	margin_sh_dtl(engine, sdate, edate)
	margin_sz_smry(engine, sdate, edate)
	
	

def daily(engine, session):
	ddate = str(datetime.date.today() - datetime.timedelta(days=1))
	# if not ts.is_holiday(str(ddate)):
	if True:
		margin_sh_smry(engine, ddate, ddate)
		margin_sh_dtl(engine, ddate, ddate)
		margin_sz_smry(engine, ddate, ddate)
		margin_sz_dtl(engine, ddate)
	else:
		pl.log("yesterday is a holiday")
	
def weekly(engine, session):
	today = datetime.date.today()
	forecast(engine, today.year, (today.month-1) / 3 + 1)
	
def monthly(engine, session):
	dinfo = get_dateinfo()
	lifted(engine, dinfo[0], dinfo[1])
	new_stock(engine)
	
def quarterly(engine, session):
	dinfo = get_dateinfo()
	forecast_history(engine, dinfo[0], dinfo[2])
	fund_hold(engine, dinfo[0], dinfo[2])

def get_dateinfo():
	today = datetime.date.today()
	year = today.year
	month = today.month - 1
	if today.month == 1:
		year -= 1
		month += 12
	quarter = month / 3
	return [year, month, quarter]

def margin_sh_smry(engine, sdate, edate):
	pl.log("invest_margin_sh_smry start...")
	df = ts.sh_margins(sdate, edate)
	if len(df) > 0:
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sh_smry',engine,if_exists='append')
	print
	pl.log("invest_margin_sh_smry done")

def margin_sh_dtl(engine, sdate, edate):
	pl.log("invest_margin_sh_dtl start...")
	df = ts.sh_margin_details(sdate, edate)
	if len(df) > 0:
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sh_dtl',engine,if_exists='append')
	print
	pl.log("invest_margin_sh_dtl done")

def margin_sz_smry(engine, sdate, edate):
	pl.log("invest_margin_sz_smry start...")
	df = ts.sz_margins(sdate, edate)
	if len(df) > 0:
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sz_smry',engine,if_exists='append')
	print
	pl.log("invest_margin_sz_smry done")

def margin_sz_dtl(engine, ddate):
	pl.log("invest_margin_sz_dtl start...")
	df = ts.sz_margin_details(ddate)
	if len(df) > 0:
		df = df.set_index('opDate', drop='true')
		df.to_sql('invest_margin_sz_dtl',engine,if_exists='append')
	print
	pl.log("invest_margin_sz_dtl done")

def lifted(engine, year, month):
	pl.log("invest_lifted start...")
	df = ts.xsg_data(year, month)
	df = df.set_index('code', drop='true')
	df.to_sql('invest_lifted',engine,if_exists='append')
	pl.log("invest_lifted done")

def new_stock(engine):
	pl.log("invest_new_stock start...")
	df = ts.new_stocks()
	df['date'] = today
	df = df.set_index('code', drop='true')
	df.to_sql('invest_new_stock',engine,if_exists='append')
	print
	pl.log("invest_new_stock done")

def forecast(engine, year, quarter):
	pl.log("invest_forecast start...")
	df = ts.forecast_data(year, quarter)
	df['year'] = year
	df['quarter'] = quarter
	df = df.set_index('code', drop='true')
	df.to_sql('invest_forecast',engine,if_exists='replace')
	print
	pl.log("invest_forecast done")

def forecast_history(engine, year, quarter):
	pl.log("invest_forecast_history start...")
	df = ts.forecast_data(year, quarter)
	df['year'] = year
	df['quarter'] = quarter
	df = df.set_index('code', drop='true')
	df.to_sql('invest_forecast_history',engine,if_exists='append')
	print
	pl.log("invest_forecast_history done")

def fund_hold(engine, year, quarter):
	pl.log("invest_fund_hold start...")
	df = ts.fund_holdings(year, quarter)
	df = df.set_index('code', drop='true')
	df.to_sql('invest_fund_hold',engine,if_exists='append')
	print
	pl.log("invest_fund_hold done")
