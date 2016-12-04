use mysql;

source ./sql/stock_proc.sql

call update_stock_info;

commit;
