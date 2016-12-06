import os
import py.pylog as pl
import conf

pl.log("data initialization start...")
for item in conf.INIT_LIST:
	os.system('python %s%s' % (conf.PY_PATH, item))
pl.log("data initialization done")
