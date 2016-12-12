import tushare as ts
import pylog as pl

def init(engine, session):
	pl.log("stock_industry start...")
	df = ts.get_industry_classified()
	df.to_sql('stock_industry',engine,if_exists='replace')
	print
	pl.log("stock_industry done")

	pl.log("stock_concept start...")
	df = ts.get_concept_classified()
	df.to_sql('stock_concept',engine,if_exists='replace')
	print
	pl.log("stock_concept done")

	pl.log("stock_area start...")
	df = ts.get_area_classified()
	df.to_sql('stock_area',engine,if_exists='replace')
	pl.log("stock_area done")

	pl.log("stock_sme start...")
	df = ts.get_sme_classified()
	df.to_sql('stock_sme',engine,if_exists='replace')
	pl.log("stock_sme done")

	pl.log("stock_gem start...")
	df = ts.get_gem_classified()
	df.to_sql('stock_gem',engine,if_exists='replace')
	pl.log("stock_gem done")

	pl.log("stock_risk_warning start...")
	df = ts.get_st_classified()
	df.to_sql('stock_risk_warning',engine,if_exists='replace')
	pl.log("stock_risk_warning done")

	pl.log("stock_hs300 start...")
	df = ts.get_hs300s()
	df.to_sql('stock_hs300',engine,if_exists='replace')
	pl.log("stock_hs300 done")

	pl.log("stock_sz50 start...")
	df = ts.get_sz50s()
	df.to_sql('stock_sz50',engine,if_exists='replace')
	pl.log("stock_sz50 done")

	pl.log("stock_zz500 start...")
	df = ts.get_zz500s()
	df.to_sql('stock_zz500',engine,if_exists='replace')
	pl.log("stock_zz500 done")

	pl.log("stock_stop_list start...")
	df = ts.get_terminated()
	df.to_sql('stock_stop_list',engine,if_exists='replace')
	pl.log("stock_stop_list done")

	pl.log("stock_pause_list start...")
	df = ts.get_suspended()
	df.to_sql('stock_pause_list',engine,if_exists='replace')
	pl.log("stock_pause_list done")
	
	pl.log("call update_stock_info start...")
	session.execute('call update_stock_info')
	pl.log("call update_stock_info done")

def monthly(engine, session, year, month):
	init(engine, session)