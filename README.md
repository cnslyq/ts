###1.create table and procedure, initlize dictionary data, 
    source /home/ts/db.sql

###2.usage
    alias tsdata='python tsdata_path/tsdata.py'
####init data
- tsdata init
####cron task
- tsdata cron
####history data
- date range : tsdata hist startdate enddate
- month data : tsdata hm year month
- quarter data : tsdata hq year quarter
- year data : tsdata hy year
- all data : tsdata ha
####real data
- tsdata real

