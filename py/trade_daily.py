from sqlalchemy import create_engine
import tushare as ts
import datetime

today = datetime.date.today()
if not ts.is_holiday(str(today)):
  engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')

  df = ts.get_index()
  df['date'] = today
  df.to_sql('trade_today_index',engine,if_exists='append')
  print
  print('trade_today_index done')

  df = ts.get_today_all()
  df['date'] = today
  df.to_sql('trade_today_market',engine,if_exists='append')
  print
  print('trade_today_market done')
else:
  print('Today is a holiday ~')
