drop table if exists trade_history_market;
create table trade_history_market(
	`id` bigint(20) primary key not null auto_increment,
	`index` int(8),
	`date` date,
	`open` double,
	`close` double,
	`high` double,
	`low` double,
	`volume` bigint(20),
	`code` varchar(8),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table trade_history_market add index trade_history_market_date_idx (`date`);
alter table trade_history_market add index trade_history_market_code_idx (`code`);

drop table if exists trade_today_market; 
create table trade_today_market(
	`id` bigint(20) primary key not null auto_increment,
	`index` int(4),
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`changepercent` double,
	`trade` double,
	`open` double,
	`high` double,
	`low` double,
	`settlement` double,
	`volume` bigint(20),
	`turnoverratio` double,
	`amount` double,
	`per` double,
	`pb` double,
	`mktcap` double,
	`nmc` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table trade_today_market add index trade_today_market_date_idx (`date`);
alter table trade_today_market add index trade_today_market_code_idx (`code`);

drop table if exists trade_today_index; 
create table trade_today_index(
	`id` bigint(20) primary key not null auto_increment,
	`index` int(2),
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`change` double,
	`open` double,
	`preclose` double,
	`close` double,
	`high` double,
	`low` double,
	`volume` bigint(20),
	`amount` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table trade_today_index add index trade_today_index_date_idx (`date`);
alter table trade_today_index add index trade_today_index_code_idx (`code`);

drop table if exists trade_block_trade;
create table trade_block_trade(
	`id` bigint(20) primary key not null auto_increment,
	`index` int(4),
	`date` date,
	`code` varchar(8),
	`name` varchar(16),
	`time` varchar(8),
	`price` double,
	`volume` bigint(20),
	`preprice` double,
	`type` varchar(16),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
);
alter table trade_block_trade add index trade_block_trade_date_idx (`date`);
alter table trade_block_trade add index trade_block_trade_code_idx (`code`);


