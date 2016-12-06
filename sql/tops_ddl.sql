drop table if exists tops_list;
create table tops_list(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`pchange` double,
	`amount` double,
	`buy` double,
	`sell` double,
	`bratio` double,
	`sratio` double,
	`reason` varchar(64),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table tops_list add index tops_list_date_idx (`date`);
alter table tops_list add index tops_list_code_idx (`code`);

drop table if exists tops_stock; 
create table tops_stock(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`count` int(2),
	`bamount` double,
	`samount` double,
	`net` double,
	`bcount` int(4),
	`scount` int(4),
	`freq` int(2),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table tops_stock add index tops_stock_date_idx (`date`);
alter table tops_stock add index tops_stock_code_idx (`code`);

drop table if exists tops_broker; 
create table tops_broker(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`broker` varchar(64),
	`count` int(2),
	`bamount` double,
	`bcount` int(4),
	`samount` double,
	`scount` int(4),
	`top3` varchar(64),
	`freq` int(2),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table tops_broker add index tops_broker_date_idx (`date`);


drop table if exists tops_inst_seat;
create table tops_inst_seat(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`bamount` double,
	`bcount` int(4),
	`samount` double,
	`scount` int(4),
	`net` double,
	`freq` int(2),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table tops_inst_seat add index tops_inst_seat_date_idx (`date`);
alter table tops_inst_seat add index tops_inst_seat_code_idx (`code`);

drop table if exists tops_inst_detail;
create table tops_inst_detail(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`bamount` double,
	`samount` double,
	`type` varchar(64),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table tops_inst_detail add index tops_inst_detail_date_idx (`date`);
alter table tops_inst_detail add index tops_inst_detail_code_idx (`code`);
