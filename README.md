###1. db init
    source tsdata_path/db.sql

###2. usage
- alias tsdata='python tsdata_path/tsdata.py'
- alias tsunit='python tsdata_path/tsunit.py'

####2.1 tsdata \[func] \[params]
func | desc | parms
----|------|----
init | data init | /
cron | cron task | /
hist | history date range data | startdate, enddate
hm | history month data | year, month
hq | history quarter data | year, quarter
hy | history year data | year
ha | all history data | /
real | real task | /
fund | fund history data | fundcode
stock | stock history data | stockcode

####2.2 tsunit \[module] \[freq] \[params]
freq | desc | params
i | data init | /
d | daily task | date
w | weekly task | date
m | monthly task | year, month
q | quarterly task | year, quarter
hd | histroy date range data | startdate, enddate
hm | history month data | year, month
hq | history quarter data | year, quarter
hy | history year data | year
ha | all history data | /
r | real task | /
