from sqlalchemy import text
import datetime

stockcodes = None
def get_stock_codes(session):
	global stockcodes
	if stockcodes is None:
		sql = "select code from stock_info"
		stockcodes = session.query("code").from_statement(text(sql)).all()
		stockcodes = [item[0].encode('utf8') for item in stockcodes]
	return stockcodes

def get_fund_codes(session):
	sql = "select symbol, IFNULL(type2 in (4002, 4003), 0) as ismonetary from fund_info"
	codes = session.query("symbol", "ismonetary").from_statement(text(sql)).all()
	codes = [[item[0].encode('utf8'),item[1]] for item in codes]
	return codes

holiday =  ('2013-01-01', '2013-01-02', '2013-01-03', '2013-02-11', '2013-02-12', 
			'2013-02-13', '2013-02-14', '2013-02-15', '2013-04-04', '2013-04-05', 
			'2013-04-29', '2013-04-30', '2013-05-01', '2013-06-10', '2013-06-11', 
			'2013-06-12', '2013-09-19', '2013-09-20', '2013-10-01', '2013-10-02', 
			'2013-10-03', '2013-10-04', '2013-10-07', 
			'2014-01-01', '2014-01-31', '2014-02-03', '2014-02-04', '2014-02-05', 
			'2014-02-06', '2014-04-07', '2014-05-01', '2014-05-02', '2014-06-02', 
			'2014-09-08', '2014-10-01', '2014-10-02', '2014-10-03', '2014-10-06', 
			'2014-10-07', 
			'2015-01-01', '2015-01-02', '2015-02-18', '2015-02-19', '2015-02-20', 
			'2015-02-23', '2015-02-24', '2015-04-06', '2015-05-01', '2015-06-22', 
			'2015-09-03', '2015-09-04', '2015-10-01', '2015-10-02', '2015-10-05', 
			'2015-10-06', '2015-10-07', 
			'2016-01-01', '2016-02-08', '2016-02-09', '2016-02-10', '2016-02-11', 
			'2016-02-12', '2016-04-04', '2016-05-02', '2016-06-09', '2016-06-10', 
			'2016-09-15', '2016-09-16', '2016-10-03', '2016-10-04', '2016-10-05', 
			'2016-10-06', '2016-10-07', 
			'2017-01-01', '2017-01-02', '2017-01-27', '2017-01-30', '2017-01-31', 
			'2017-02-01', '2017-02-02', '2017-04-03', '2017-04-04', '2017-05-01', 
			'2017-05-29', '2017-05-30', '2017-10-02', '2017-10-03', '2017-10-04', 
			'2017-10-05', '2017-10-06')
def is_holiday(date):
	today = date
	if isinstance(date, str):
		today = datetime.datetime.strptime(date, '%Y-%m-%d')
	return today.isoweekday() in [6, 7] or str(today) in holiday

def get_ldate(date, diff):
	ldate = {}
	ldate["year"] = date.year
	ldate["month"] = date.month - diff
	if ldate["month"] <= 0:
		ldate["year"] -= 1
		ldate["month"] += 12
	ldate["quarter"] = ldate["month"] / 3 + 1
	return ldate
	
def get_quarter_date(year, quarter):
	sdt = {1: '-01-01', 2: '-04-01', 3: '-07-01', 4: '-10-01'}
	edt = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}
	return ['%s%s'%(str(year), sdt[quarter]), '%s%s'%(str(year), edt[quarter])]
'''
import tushare as ts
import pylog as pl

tfmap = {'trade_market_history':'get_k_data',
		'trade_market_today':'get_today_all',
		'trade_index_today':'get_index',
		'trade_block':'get_sina_dd',
		'invest_profit':'profit_data',
		'invest_forecast_history':'forecast_data',
		'invest_forecast':'forecast_data',
		'invest_lifted':'xsg_data',
		'invest_fund_hold':'fund_holdings',
		'invest_new_stock':'new_stocks',
		'invest_margin_sh_smry':'sh_margins',
		'invest_margin_sh_dtl':'sh_margin_details',
		'invest_margin_sz_smry':'sz_margins',
		'invest_margin_sz_dtl':'sz_margin_details',
		'stock_industry':'get_industry_classified',
		'stock_concept':'get_concept_classified',
		'stock_area':'get_area_classified',
		'stock_sme':'get_sme_classified',
		'stock_gem':'get_gem_classified',
		'stock_risk_warning':'get_st_classified',
		'stock_hs300':'get_hs300s',
		'stock_sz50':'get_sz50s',
		'stock_zz500':'get_zz500s',
		'stock_stop_list':'get_terminated',
		'stock_pause_list':'get_suspended',
		'tops_list':'top_list',
		'tops_stock':'cap_tops',
		'tops_broker':'broker_tops',
		'tops_inst_seat':'inst_tops',
		'tops_inst_detail':'inst_detail'}

def to_sql(engine, table, idx='code', exist='append', plist=[], pdict={}, adata={}, log=True, errmsg=''):
	if(log):
		pl.log(table + " start...")
	try:
		func = getattr(ts, tfmap[table])
		estr = "df = func("
		for i in range(len(plist)):
			estr += "plist[%i], " % i
		for i in range(len(pdict)):
			estr += "%s=pdict[%i], " % (pdict[i], i)
		estr = estr[:-1]
		estr += ")"
		c = compile(estr,'','exec')
		exec c
		if len(df) == 0:
			pl.log(table + " has no data " + errmsg)
			return
		for key in adata:
			df[key] = adata[key]
		df = df.set_index(idx, drop='true')
		df.to_sql(table, engine, if_exists=exist)
		if(log):
			print
			pl.log(table + " done")
	except BaseException, e:
		print e
		pl.log(table + " error " + errmsg)
'''
