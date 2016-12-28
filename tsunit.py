from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.tslog as tsl
import py.tsconf as tsc
import sys

INPUT_DICT = {'i':3, 'd':4, 'w':4, 'm':5, 'q':5, 'hd':5, 'hm':5, 'hq':5, 'hy':4, 'ha':3, 'r':3}
FUNC_DICT = {'i':'init', 'd':'daily', 'w':'weekly', 'm':'month', 'q':'quarterly', 
			'hd':'history', 'hm':'history_m', 'hq':'history_q', 'hy':'history_y', 'ha':'history_a', 'r':'real'}

engine = create_engine(tsc.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

names = locals()
def call(mod, func, argv):
	st = datetime.datetime.today()
	tsl.log(mod + " " + func + " start...")
	params = []
	for param in argv:
		if len(param) == 8:
			params.append(datetime.date(int(param[0:4]), int(param[4:6]), int(param[6:8])))
		else:
			params.append(int(param))
	estr = "method(engine, session"
	for i in range(len(params)):
		estr += ", params[%i]" % i
	estr += ")"
	c = compile(estr,'','exec')
	obj = __import__(mod, fromlist=True)
	method = getattr(obj, func)
	exec c
	et = datetime.datetime.today()
	tsl.log(mod + " " + func + " done cost time : " + str(et - st))

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("please input module(trade/tops/...) and type(i/d/w/m/q/hd/hm/hq/hy/ha/r)")
		sys.exit(1)
	mod = sys.argv[1]
	type = sys.argv[2]
	if type in INPUT_DICT:
		if len(sys.argv) < INPUT_DICT[type]:
			print("wrong param numbers")
			sys.exit(1)
		else:
			call('py.' + mod, FUNC_DICT[type], sys.argv[3:])
	else:
		print("wrong type name")
		sys.exit(1)
