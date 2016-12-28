import tushare as ts
import tslog as tsl

def monthly(engine, session, year, month):
	stock(engine)
	
def quarterly(engine, session, year, quarter):
	performance(engine, year, quarter)
	profit(engine, year, quarter)
	operation(engine, year, quarter)
	growth(engine, year, quarter)
	debt(engine, year, quarter)
	cashflow(engine, year, quarter)

def history_q(engine, session, year, quarter):
	quarterly(engine, session, year, quarter)

def stock(engine):
	tbl = "basic_stock"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_stock_basics()
		df.to_sql(tbl,engine,if_exists='replace')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")

def performance(engine, year, quarter):
	tbl = "basic_performance"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_report_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
	
def profit(engine, year, quarter):
	tbl = "basic_profit"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_profit_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
	
def operation(engine, year, quarter):
	tbl = "basic_operation"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_operation_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
	
def growth(engine, year, quarter):
	tbl = "basic_growth"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_growth_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
	
def debt(engine, year, quarter):
	tbl = "basic_debt"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_debtpaying_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")
	
def cashflow(engine, year, quarter):
	tbl = "basic_cashflow"
	tsl.log(tbl + " start...")
	try:
		df = ts.get_cashflow_data(year,quarter)
		df = df.set_index('code', drop='true')
		df['year'] = year
		df['quarter'] = quarter
		df = df.fillna(0)
		df.to_sql(tbl,engine,if_exists='append')
		print
		tsl.log(tbl + " done")
	except BaseException, e:
		print
		print e
		tsl.log(tbl + " error")


