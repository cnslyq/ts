import os

init_list = ['stock_init.py']
for item in init_list:
	os.system('python ./py/%s' % item)
