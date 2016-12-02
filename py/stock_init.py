from sqlalchemy import create_engine
import tushare as ts

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')

df = ts.get_industry_classified()
df.to_sql('stock_industry',engine,if_exists='replace')
print
print('stock_industry done')

df = ts.get_concept_classified()
df.to_sql('stock_concept',engine,if_exists='replace')
print
print('stock_concept done')

df = ts.get_area_classified()
df.to_sql('stock_area',engine,if_exists='replace')
print
print('stock_area done')

df = ts.get_sme_classified()
df.to_sql('stock_sme',engine,if_exists='replace')
print
print('stock_sme done')

df = ts.get_gem_classified()
df.to_sql('stock_gem',engine,if_exists='replace')
print
print('stock_gem done')

df = ts.get_st_classified()
df.to_sql('stock_risk_warning',engine,if_exists='replace')
print
print('stock_risk_warning done')

df = ts.get_hs300s()
df.to_sql('stock_hs300',engine,if_exists='replace')
print
print('stock_hs300 done')

df = ts.get_sz50s()
df.to_sql('stock_sz50',engine,if_exists='replace')
print
print('stock_sz50 done')

df = ts.get_zz500s()
df.to_sql('stock_zz500',engine,if_exists='replace')
print
print('stock_zz500 done')

df = ts.get_terminated()
df.to_sql('stock_stop_list',engine,if_exists='replace')
print
print('stock_stop_list done')

df = ts.get_suspended()
df.to_sql('stock_pause_list',engine,if_exists='replace')
print
print('stock_pause_list done')
