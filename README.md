###define table, initlize dictionary data\n
source /home/ts/db.sql

###get finance data through python interface\n
python /home/ts/data_init.py

###data process\n
source /home/ts/data_process.sql
