import tushare as ts
import pylog as pl

def monthly(engine, session, year, month):
	stock(engine)
	
def quarterly(engine, session, year, quarter):
	performance(engine, year, quarter)
	profit(engine, year, quarter)
	operation(engine, year, quarter)
	# growth(engine, year, quarter)
	debt(engine, year, quarter)
	cashflow(engine, year, quarter)

def history_q(engine, session, year, quarter):
	quarterly(engine, session, year, quarter)

def stock(engine):
	tbl = "basic_stock"
	pl.log(tbl + " start...")
	try:
		df = ts.get_stock_basics()
		df.to_sql(tbl,engine,if_exists='replace')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")

def performance(engine, year, quarter):
	tbl = "basic_performance"
	pl.log(tbl + " start...")
	try:
		df = ts.get_report_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
	
def profit(engine, year, quarter):
	tbl = "basic_profit"
	pl.log(tbl + " start...")
	try:
		df = ts.get_profit_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
	
def operation(engine, year, quarter):
	tbl = "basic_operation"
	pl.log(tbl + " start...")
	try:
		df = ts.get_operation_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
	
# bug : line 1113: htmlParseStartTag: invalid element name
def growth(engine, year, quarter):
	tbl = "basic_growth"
	pl.log(tbl + " start...")
	try:
		df = ts.get_growth_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
	
def debt(engine, year, quarter):
	tbl = "basic_debt"
	pl.log(tbl + " start...")
	try:
		df = ts.get_debtpaying_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")
	
def cashflow(engine, year, quarter):
	tbl = "basic_cashflow"
	pl.log(tbl + " start...")
	try:
		df = ts.get_cashflow_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		pl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		pl.log(tbl + " error")


