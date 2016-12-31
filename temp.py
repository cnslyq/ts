import os
import datetime

today = datetime.date.today()
tyear = today.year
tmonth = today.month
tquarter = (tmonth-1)/3 + 1
'''
cmd_list = ['python -u /home/ts/tsdata.py hist 20130101 20130630 > /home/ts201301.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20130701 20131231 > /home/ts201302.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20140101 20140630 > /home/ts201401.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20140701 20141231 > /home/ts201402.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20150101 20150630 > /home/ts201501.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20150701 20151231 > /home/ts201502.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20160101 20160630 > /home/ts201601.log 2>&1 &',
			'python -u /home/ts/tsdata.py hist 20160701 20161130 > /home/ts201602.log 2>&1 &']
for cmd in cmd_list:
	print cmd
	os.system(cmd)
'''
ddic = {1:['0101','0331'],2:['0401','0630'],3:['0701','0930'],4:['1001','1231']}
for year in range(2013, tyear):
	print "year data : %i" % year
	print "quarter data : 1"
	os.system('python /home/ts/tsunit.py fund hd %i%s %i%s > /home/tsf%i01.log 2>&1' % (year, ddic[1][0], year, ddic[1][1], year))
	print "quarter data : 2"
	os.system('python /home/ts/tsunit.py fund hd %i%s %i%s > /home/tsf%i02.log 2>&1' % (year, ddic[2][0], year, ddic[2][1], year))
	print "quarter data : 3"
	os.system('python /home/ts/tsunit.py fund hd %i%s %i%s > /home/tsf%i03.log 2>&1' % (year, ddic[3][0], year, ddic[3][1], year))
	print "quarter data : 4"
	os.system('python /home/ts/tsunit.py fund hd %i%s %i%s > /home/tsf%i04.log 2>&1' % (year, ddic[4][0], year, ddic[4][1], year))