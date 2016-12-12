import tushare as ts
import pylog as pl
from sqlalchemy import create_engine

def init(engine, session):
	ENGINE = 'mysql://root:123456@127.0.0.1/test?charset=utf8'
	engine = create_engine(ENGINE)
	
	tbl = "macro_deposit"
	pl.log(tbl + " start...")
	df = ts.get_deposit_rate()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_loan"
	pl.log(tbl + " start...")
	df = ts.get_loan_rate()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_rrr"
	pl.log(tbl + " start...")
	df = ts.get_rrr()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_money_supply"
	pl.log(tbl + " start...")
	df = ts.get_money_supply()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_money_supply_year"
	pl.log(tbl + " start...")
	df = ts.get_money_supply_bal()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_gdp_year"
	pl.log(tbl + " start...")
	df = ts.get_gdp_year()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_gdp_quarter"
	pl.log(tbl + " start...")
	df = ts.get_gdp_quarter()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_gdp_for"
	pl.log(tbl + " start...")
	df = ts.get_gdp_for()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_gdp_pull"
	pl.log(tbl + " start...")
	df = ts.get_gdp_pull()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_gdp_contrib"
	pl.log(tbl + " start...")
	df = ts.get_gdp_contrib()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_cpi"
	pl.log(tbl + " start...")
	df = ts.get_cpi()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	
	tbl = "macro_ppi"
	pl.log(tbl + " start...")
	df = ts.get_ppi()
	df.to_sql(tbl,engine,if_exists='replace')
	pl.log(tbl + " done")
	

def monthly(engine, session, year, month):
	init(engine, session)