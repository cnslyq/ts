from sqlalchemy import create_engine
import tushare as ts
import datetime

def tops(freq):
  print('The frequence is %i' % freq)
  engine = create_engine('mysql://root:123456@127.0.0.1/mysql?charset=utf8')
  today = datetime.date.today()
  
  print(str(datetime.datetime.today()) + " tops_stock start...")
  df = ts.cap_tops(freq)
  df['date'] = today
  df['freq'] = freq
  df = df.set_index('code', drop='true')
  df.to_sql('tops_stock',engine,if_exists='append')
  print
  print(str(datetime.datetime.today()) + " tops_stock done")
  
  print(str(datetime.datetime.today()) + " tops_broker start...")
  df = ts.broker_tops(freq)
  df['date'] = today
  df['freq'] = freq
  df = df.set_index('date', drop='true')
  df.to_sql('tops_broker',engine,if_exists='append')
  print
  print(str(datetime.datetime.today()) + " tops_broker done")
  
  print(str(datetime.datetime.today()) + " tops_inst_seat start...")
  df = ts.inst_tops(freq)
  df['date'] = today
  df['freq'] = freq
  df = df.set_index('code', drop='true')
  df.to_sql('tops_inst_seat',engine,if_exists='append')
  print
  print(str(datetime.datetime.today()) + " tops_inst_seat done")
  
  if freq == 5:
    pass