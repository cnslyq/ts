drop table if exists trade_market_history;
create table trade_market_history(
	`id` bigint(20) primary key not null auto_increment,
	`date` date,
	`open` double,
	`close` double,
	`high` double,
	`low` double,
	`volume` bigint(20),
	`code` varchar(8),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table trade_market_history add index trade_market_history_date_idx (`date`);
alter table trade_market_history add index trade_market_history_code_idx (`code`);

drop table if exists trade_market_today; 
create table trade_market_today(
	`id` bigint(20) primary key not null auto_increment,
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
alter table trade_market_today add index trade_market_today_date_idx (`date`);
alter table trade_market_today add index trade_market_today_code_idx (`code`);

drop table if exists trade_index_today; 
create table trade_index_today(
	`id` bigint(20) primary key not null auto_increment,
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
alter table trade_index_today add index trade_index_today_date_idx (`date`);
alter table trade_index_today add index trade_index_today_code_idx (`code`);

drop table if exists trade_block;
create table trade_block(
	`id` bigint(20) primary key not null auto_increment,
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
alter table trade_block add index trade_block_date_idx (`date`);
alter table trade_block add index trade_block_code_idx (`code`);
