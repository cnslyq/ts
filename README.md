###1.create table and procedure, initlize dictionary data, 
    source /home/ts/db.sql

###2.get finance data through python interface
python /home/ts/data_init.py

###3.usage
alias tsdata='python /home/ts/tsdata.py'
####a.cron task
tsdata cron
####b.fetch history data
date range : tsdata hist startdate enddate  
month data : tsdata hm year month  
quarter datat : tsdata hq year quarter  

