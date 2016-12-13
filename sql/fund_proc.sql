DELIMITER $$

DROP PROCEDURE IF EXISTS update_fund_info;

CREATE PROCEDURE update_fund_info()
BEGIN

update fund_info t1, fund_temp_info t2
   set a.symbol = b.symbol,
       a.jjqc = b.jjqc,
       a.jjjc = b.jjjc,
       a.clrq = b.clrq,
       a.ssrq = b.ssrq,
       a.xcr = b.xcr,
       a.ssdd = b.ssdd,
       a.Type1Name = b.Type1Name,
       a.Type2Name = b.Type2Name,
       a.Type3Name = b.Type3Name,
       a.jjgm = b.jjgm,
       a.jjfe = b.jjfe,
       a.jjltfe = b.jjltfe,
       a.jjferq = b.jjferq,
       a.quarter = b.quarter,
       a.glr = b.glr,
       a.tgr = b.tgr,
       a.update_date = now()
 where t1.symbol = t2.symbol;

insert into fund_info(symbol, jjqc, jjjc, clrq, ssrq, xcr, ssdd, Type1Name, Type2Name, Type3Name, jjgm, jjfe, jjltfe, jjferq, quarter, glr, tgr, update_date)
select a.symbol, a.jjqc, a.jjjc, a.clrq, a.ssrq, a.xcr, a.ssdd, a.Type1Name, a.Type2Name, a.Type3Name, a.jjgm, a.jjfe, a.jjltfe, a.jjferq, a.quarter, a.glr, a.tgr, now()
  from fund_temp_info a
 where not exists(select 1 from fund_info b where a.symbol = b.symbol);

commit;

END$$

DELIMITER ;
