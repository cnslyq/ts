####define table, initlize dictionary data
source /home/ts/db.sql

####get finance data through python interface
python /home/ts/data_init.py

####data process
source /home/ts/data_process.sql
