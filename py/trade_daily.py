from sqlalchemy import create_engine
import tushare as ts
import datetime

today = datetime.date.today()
print(datetime.datetime.today())
if not ts.is_holiday(str(today)):
  engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')

  df = ts.get_index()
  df['date'] = today
  df.to_sql('trade_today_index', engine, if_exists='append')
  print
  print('trade_today_index done')

  df = ts.get_today_all()
  df['date'] = today
  df.to_sql('trade_today_market', engine, if_exists='append')
  print
  print('trade_today_market done')
  
  start = datetime.datetime.today()
  codes = [item[0] for item in ts.get_area_classified().values]
  for code in codes:
    df = ts.get_sina_dd(code, today, vol=5000)
    if df is not None:
      df.to_sql('trade_block_trade', engine, if_exists='append')
  end = datetime.datetime.today()
  print('cost time : ' + str(end - start))
  
  print
  print('trade_block_trade done')
  
else:
  print('Today is a holiday ~')
