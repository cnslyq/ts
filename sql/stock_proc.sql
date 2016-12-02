USE mysql;

DELIMITER $$

DROP PROCEDURE IF EXISTS update_stock_info;

CREATE PROCEDURE update_stock_info()
BEGIN

declare done int default 0;
declare v_code varchar(8);
declare v_name varchar(16);
declare v_count int default 0;

declare cursor_name cursor for select a.code, a.name from stock_area a where not exists(select 1 from stock_info b where a.code = b.code);
declare continue handler for SQLSTATE '02000' set done = 1;  

open cursor_name;
fetch cursor_name into v_code, v_name;

while done <> 1 do
  select count(1) into v_count from stock_info where code = v_code;
  if v_count = 0 then
    insert into stock_info(code, name) values (v_code, v_name);
  end if;
  fetch cursor_name into v_code, v_name;
end while;
close cursor_name;

update stock_info t1, (
 select a.code as code,
           a1.id as area,
           d1.value as industry, 
           group_concat(d2.value) as concept, 
           if(d.index is null, 0, 1) as is_sme,
           if(e.index is null, 0, 1) as is_gem,
           if(f.index is null, 0, 1) as is_risk,
           if(g.index is null, 0, 1) as is_hs300,
           if(h.index is null, 0, 1) as is_sz50,
           if(i.index is null, 0, 1) as is_zz500,
           if(j.index is null, 0, 1) as is_stop,
           if(k.index is null, 0, 1) as is_pause,
           g.date as hs300_date,
           g.weight as hs300_weight,
           ifnull(j.oDate, k.oDate) as list_date,
           j.tDate as stop_date,
           k.tDate as pause_date
      from stock_area a
     inner join area a1 on a.area = a1.name
      left join stock_industry b on a.code = b.code
      left join dict d1 on d1.type = 'industry' and d1.name = b.c_name
      left join stock_concept c on a.code = c.code
      left join dict d2 on d2.type = 'concept' and d2.name = c.c_name
      left join stock_sme d on a.code = d.code
      left join stock_gem e on a.code = e.code
      left join stock_risk_warning f on a.code = f.code
      left join stock_hs300 g on a.code = g.code
      left join stock_sz50 h on a.code = h.code
      left join stock_zz500 i on a.code = i.code
      left join stock_stop_list j on a.code = j.code
      left join stock_pause_list k on a.code = k.code
     group by a.code
   ) t2
 set t1.area = t2.area,
     t1.industry = t2.industry, 
     t1.concept = t2.concept,
     t1.is_sme = t2.is_sme,
     t1.is_gem = t2.is_gem,
     t1.is_risk = t2.is_risk,
     t1.is_hs300 = t2.is_hs300,
     t1.is_sz50 = t2.is_sz50,
     t1.is_zz500 = t2.is_zz500,
     t1.is_stop = t2.is_stop,
     t1.is_pause = t2.is_pause,
     t1.hs300_date = t2.hs300_date,
     t1.hs300_weight = t2.hs300_weight,
     t1.list_date = t2.list_date,
     t1.stop_date = t2.stop_date,
     t1.pause_date = t2.pause_date,
     t1.update_date = now()
where t1.code = t2.code;

commit;

END$$

DELIMITER ;
