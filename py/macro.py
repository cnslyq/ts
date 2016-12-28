import tushare as ts
import tslog as tsl
from sqlalchemy import create_engine

def init(engine, session):
	tbl = "macro_deposit"
	tsl.log(tbl + " start...")
	df = ts.get_deposit_rate()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_loan"
	tsl.log(tbl + " start...")
	df = ts.get_loan_rate()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_rrr"
	tsl.log(tbl + " start...")
	df = ts.get_rrr()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_money_supply"
	tsl.log(tbl + " start...")
	df = ts.get_money_supply()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_money_supply_year"
	tsl.log(tbl + " start...")
	df = ts.get_money_supply_bal()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_gdp_year"
	tsl.log(tbl + " start...")
	df = ts.get_gdp_year()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_gdp_quarter"
	tsl.log(tbl + " start...")
	df = ts.get_gdp_quarter()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_gdp_for"
	tsl.log(tbl + " start...")
	df = ts.get_gdp_for()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_gdp_pull"
	tsl.log(tbl + " start...")
	df = ts.get_gdp_pull()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_gdp_contrib"
	tsl.log(tbl + " start...")
	df = ts.get_gdp_contrib()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_cpi"
	tsl.log(tbl + " start...")
	df = ts.get_cpi()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	
	tbl = "macro_ppi"
	tsl.log(tbl + " start...")
	df = ts.get_ppi()
	df.to_sql(tbl,engine,if_exists='replace')
	tsl.log(tbl + " done")
	

def monthly(engine, session, year, month):
	init(engine, session)