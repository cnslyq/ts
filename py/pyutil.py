from sqlalchemy import text
import tushare as ts
import pylog as pl

cal = None
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

def get_codes(session, vip=False):
	sql = "select code from stock_info"
	if(vip):
		sql += " where is_hs300 = 1 or is_sz50 = 1 or is_zz500 = 1"
	codes = session.query("code").from_statement(text(sql)).all()
	codes = [item[0].encode('utf8') for item in codes]
	return codes

def is_tddate(session, date):
	global cal
	if cal is None:
		cal = session.query("date", "is_open").from_statement(text("select date, is_open from calendar")).all()
		cal = {item[0]:item[1] for item in cal}
	return cal[date]

def get_ldate(date):
	ldate = {}
	ldate["year"] = date.year
	ldate["month"] = date.month - 1
	if date.month == 1:
		ldate["year"] -= 1
		ldate["month"] += 12
	ldate["quarter"] = ldate["month"] / 3
	return ldate

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
		exec estr
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
