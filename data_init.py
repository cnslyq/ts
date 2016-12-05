import os

init_list = ['stock_init.py', 'trade_init.py']
for item in init_list:
	os.system('python /home/ts/py/%s' % item)
