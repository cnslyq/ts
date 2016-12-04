import os

init_list = ['trade_daily.py']
for item in init_list:
	os.system('python ./py/%s' % item)
