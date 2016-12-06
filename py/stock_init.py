from sqlalchemy import create_engine
import tushare as ts
import datetime

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')

print(str(datetime.datetime.today()) + " stock_industry initialization start...")
df = ts.get_industry_classified()
df.to_sql('stock_industry',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_industry initialization done")

print(str(datetime.datetime.today()) + " stock_concept initialization start...")
df = ts.get_concept_classified()
df.to_sql('stock_concept',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_concept initialization done")

print(str(datetime.datetime.today()) + " stock_area initialization start...")
df = ts.get_area_classified()
df.to_sql('stock_area',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_area initialization done")

print(str(datetime.datetime.today()) + " stock_sme initialization start...")
df = ts.get_sme_classified()
df.to_sql('stock_sme',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_sme initialization done")

print(str(datetime.datetime.today()) + " stock_gem initialization start...")
df = ts.get_gem_classified()
df.to_sql('stock_gem',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_gem initialization done")

print(str(datetime.datetime.today()) + " stock_risk_warning initialization start...")
df = ts.get_st_classified()
df.to_sql('stock_risk_warning',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_risk_warning initialization done")

print(str(datetime.datetime.today()) + " stock_hs300 initialization start...")
df = ts.get_hs300s()
df.to_sql('stock_hs300',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_hs300 initialization done")

print(str(datetime.datetime.today()) + " stock_sz50 initialization start...")
df = ts.get_sz50s()
df.to_sql('stock_sz50',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_sz50 initialization done")

print(str(datetime.datetime.today()) + " stock_zz500 initialization start...")
df = ts.get_zz500s()
df.to_sql('stock_zz500',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_zz500 initialization done")

print(str(datetime.datetime.today()) + " stock_stop_list initialization start...")
df = ts.get_terminated()
df.to_sql('stock_stop_list',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_stop_list initialization done")

print(str(datetime.datetime.today()) + " stock_pause_list initialization start...")
df = ts.get_suspended()
df.to_sql('stock_pause_list',engine,if_exists='replace')
print
print(str(datetime.datetime.today()) + " stock_pause_list initialization done")
