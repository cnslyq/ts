use mysql;

source /home/ts/sql/stock_proc.sql

call update_stock_info;

commit;
