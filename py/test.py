from sqlalchemy import create_engine
import tushare as ts
import datetime

today = datetime.date(2016, 12, 2)
print(datetime.datetime.today())

codes = [item[0] for item in ts.get_area_classified().values]
for code in codes:
  df = ts.get_sina_dd(code, today)
  df.to_sql('trade_block_trade', engine, if_exists='append')
print
print('trade_block_trade done')
