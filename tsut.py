from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import py.tslog as tsl
import py.tsconf as tsc
import sys

engine = create_engine(tsc.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

def call(mod, func, argv):
	st = datetime.datetime.today()
	tsl.log(mod + " " + func + " start...")
	params = []
	estr = "method(engine"
	for param in argv:
		# session
		if param == 's':
			estr += ", session"
		# date
		elif len(param) == 8:
			params.append(datetime.date(int(param[0:4]), int(param[4:6]), int(param[6:8])))
		# code
		elif len(param) == 6:
			params.append(param)
		# year, month, quarter, frequence
		else:
			params.append(int(param))
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
		print("please input module and func")
		sys.exit(1)
	mod = sys.argv[1]
	func = sys.argv[2]
	call('py.' + mod, func, sys.argv[3:])

