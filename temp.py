import os
import datetime

today = datetime.date.today()
tyear = today.year
tmonth = today.month
tquarter = (tmonth-1)/3 + 1

for year in range(2013, tyear):
	for month in range(1, 13):
		print 'month data : %i %i' % (year, month)
		os.system('python /home/ts/tsdata.py hm %i %i' % (year, month))
	for quarter in range(1, 5):
		print 'quarter data : %i %i' %(year, quarter)
		os.system('python /home/ts/tsdata.py hq %i %i' % (year, quarter))

for month in range(1, tmonth):
	print 'month data : %i %i' % (tyear, month)
	os.system('python /home/ts/tsdata.py hm %i %i' % (tyear, month))
for quarter in range(1, tquarter):
	print 'quarter data : %i %i' %(tyear, quarter)
	os.system('python /home/ts/tsdata.py hq %i %i' % (tyear, quarter))