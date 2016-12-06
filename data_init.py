import os
import py.pylog as pl

pl.log("data initialization start...")
py_list = ['stock_init.py', 'trade_init.py']
for item in py_list:
	os.system('python /home/ts/py/%s' % item)
pl.log("data initialization done")
