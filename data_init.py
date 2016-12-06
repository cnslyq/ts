import os
import datetime

print(str(datetime.datetime.today()) + " data initialization start...")
py_list = ['stock_init.py', 'trade_init.py']
for item in py_list:
	os.system('python /home/ts/py/%s' % item)
print(str(datetime.datetime.today()) + " data initialization done")
