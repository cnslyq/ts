from sqlalchemy import create_engine
import tushare as ts
import datetime

today = datetime.date(2016, 12, 2)
start = datetime.datetime.today()
print(start)

engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')
codes = [item[0] for item in ts.get_area_classified().values]
print(len(codes))
for code in codes:
  df = ts.get_sina_dd(code, today, vol=5000)
  if df is not None:
    df.to_sql('trade_block_trade', engine, if_exists='append')
print
end = datetime.datetime.today()
print('cost time : ' + str(end - start))
print('trade_block_trade done')
