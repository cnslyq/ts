DELIMITER $$

DROP PROCEDURE IF EXISTS update_fund_info;

CREATE PROCEDURE update_fund_info()
BEGIN

update fund_info a, fund_temp_info b
   set a.symbol = b.symbol,
       a.jjqc = b.jjqc,
       a.jjjc = b.jjjc,
       a.clrq = b.clrq,
       a.ssrq = b.ssrq,
       a.xcr = b.xcr,
       a.ssdd = b.ssdd,
       a.type1 = (select d.value from dict d where d.type = 'fundtype1' and d.name = b.Type1Name),
       a.type2 = (select d.value from dict d where d.type = 'fundtype2' and d.name = b.Type2Name),
       a.type3 = (select d.value from dict d where d.type = 'fundtype3' and d.name = b.Type3Name),
       a.jjgm = b.jjgm,
       a.jjfe = b.jjfe,
       a.jjltfe = b.jjltfe,
       a.jjferq = b.jjferq,
       a.quarter = b.quarter,
       a.glr = b.glr,
       a.tgr = b.tgr,
       a.update_date = now()
 where a.symbol = b.symbol;

insert into fund_info(symbol, jjqc, jjjc, clrq, ssrq, xcr, ssdd, type1, type2, type3, jjgm, jjfe, jjltfe, jjferq, quarter, glr, tgr, update_date)
select a.symbol, a.jjqc, a.jjjc, a.clrq, a.ssrq, a.xcr, a.ssdd, d1.value, d2.value, d3.value, a.jjgm, a.jjfe, a.jjltfe, a.jjferq, a.quarter, a.glr, a.tgr, now()
  from fund_temp_info a
  left join dict d1 on d1.type = 'fundtype1' and a.Type1Name = d1.name
  left join dict d2 on d2.type = 'fundtype2' and a.Type2Name = d2.name
  left join dict d3 on d3.type = 'fundtype3' and a.Type3Name = d3.name
 where not exists(select 1 from fund_info b where a.symbol = b.symbol);

commit;

END$$

DELIMITER ;
