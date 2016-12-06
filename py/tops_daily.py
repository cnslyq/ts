from sqlalchemy import create_engine
import tushare as ts
import pylog as pl

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')

pl.log("tops_inst_detail start...")
df = ts.inst_detail()
df = df.set_index('code', drop='true')
df.to_sql('tops_inst_detail', engine, if_exists='append')
print
pl.log("tops_inst_detail done")
