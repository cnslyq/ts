drop table if exists basic_stock;
create table basic_stock(
	`id` int(6) primary key not null auto_increment,
	`code` varchar(8),
	`name` varchar(16),
	`industry` varchar(16),
	`area` varchar(32),
	`pe` double,
	`outstanding` double,
	`totals` double,
	`totalAssets` double,
	`liquidAssets` double,
	`fixedAssets` double,
	`reserved` double,
	`reservedPerShare` double,
	`esp` double,
	`bvps` double,
	`pb` double,
	`timeToMarket` date,
	`undp` double,
	`perundp` double,
	`rev` double,
	`profit` double,
	`gpr` double,
	`npr` double,
	`holders` int(8),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_stock add index basic_stock_code_idx (`code`);

drop table if exists basic_performance; 
create table basic_performance(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`eps` double,
	`eps_yoy` double,
	`bvps` double,
	`roe` double,
	`epcf` double,
	`net_profits` double,
	`profits_yoy` double,
	`distrib` double,
	`report_date` varchar(8),
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_performance add index basic_performance_date_idx (`year`, `quarter`);
alter table basic_performance add index basic_performance_code_idx (`code`);

drop table if exists basic_profit; 
create table basic_profit(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`roe` double,
	`net_profit_ratio` double,
	`gross_profit_rate` double,
	`net_profits` double,
	`eps` double,
	`business_income` double,
	`bips` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_profit add index basic_profit_date_idx (`year`, `quarter`);
alter table basic_profit add index basic_profit_code_idx (`code`);

drop table if exists basic_operation; 
create table basic_operation(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`arturnover` double,
	`arturndays` double,
	`inventory_turnover` double,
	`inventory_days` double,
	`currentasset_turnover` double,
	`currentasset_days` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_operation add index basic_operation_date_idx (`year`, `quarter`);
alter table basic_operation add index basic_operation_code_idx (`code`);

drop table if exists basic_growth; 
create table basic_growth(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`mbrg` double,
	`nprg` double,
	`nav` double,
	`targ` double,
	`epsg` double,
	`seg` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_growth add index basic_growth_date_idx (`year`, `quarter`);
alter table basic_growth add index basic_growth_code_idx (`code`);

drop table if exists basic_debt; 
create table basic_debt(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`currentratio` double,
	`quickratio` double,
	`cashratio` double,
	`icratio` double,
	`sheqratio` double,
	`adratio` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_debt add index basic_debt_date_idx (`year`, `quarter`);
alter table basic_debt add index basic_debt_code_idx (`code`);

drop table if exists basic_cashflow; 
create table basic_cashflow(
	`id` bigint(20) primary key not null auto_increment,
	`year` int(4),
	`quarter` int(1),
	`code` varchar(8),
	`name` varchar(16),
	`cf_sales` double,
	`rateofreturn` double,
	`cf_nm` double,
	`cf_liabilities` double,
	`cashflowratio` double,
	`create_date` timestamp not null default CURRENT_TIMESTAMP
) ENGINE=InnoDB;
alter table basic_cashflow add index basic_cashflow_date_idx (`year`, `quarter`);
alter table basic_cashflow add index basic_cashflow_code_idx (`code`);
