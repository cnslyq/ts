from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import tushare as ts
import datetime
import pylog as pl

today = datetime.date.today()

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session()

pl.log("trade_index_today start...")
df = ts.get_index()
df = df.set_index('code', drop='true')
df['date'] = today
df.to_sql('trade_index_today', engine, if_exists='append')
pl.log("trade_index_today done")

pl.log("trade_market_today start...")
df = ts.get_today_all()
df = df.set_index('code', drop='true')
df['date'] = today
df.to_sql('trade_market_today', engine, if_exists='append')
print
pl.log("trade_market_today done")

pl.log("trade_block start...")
# codes = [item[0] for item in ts.get_area_classified().values]
codes = session.query("code").from_statement(text("select code from stock_info")).all()
codes = [item[0].encode('utf8') for item in codes]
for code in codes:
  df = ts.get_sina_dd(code, today, vol=5000)
  if df is not None:
    df = df.set_index('code', drop='true')
    df['date'] = today
    df.to_sql('trade_block', engine, if_exists='append')
pl.log("trade_block done")
