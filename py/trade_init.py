from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import tushare as ts
import datetime
import pylog as pl

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session()

sdate = datetime.date(2016, 12, 1)
edate = datetime.date.today()
# edate = datetime.date(2016, 12, 5)
pl.log("trade data initialization start...")
# codes = [item[0] for item in ts.get_area_classified().values]
codes = session.query("code").from_statement(text("select code from stock_info")).all()
codes = [item[0].encode('utf8') for item in codes]

for code in codes:
  df = ts.get_k_data(code, start=str(sdate))
  if df is not None:
    # print code
    df = df.set_index('code', drop='true')
    df.to_sql('trade_market_history', engine, if_exists='append')
  
  cdate = sdate
  while cdate <= edate:
    if not ts.is_holiday(str(cdate)):
      df = ts.get_sina_dd(code, cdate, vol=5000)
      if df is not None:
        df = df.set_index('code', drop='true')
        df['date'] = cdate
        df.to_sql('trade_block', engine, if_exists='append')
    cdate += datetime.timedelta(days=1)
pl.log("trade data initialization done")
