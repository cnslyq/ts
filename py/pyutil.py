from sqlalchemy import text

cal = None

def get_codes(session):
	codes = session.query("code").from_statement(text("select code from stock_ldate")).all()
	codes = [item[0].encode('utf8') for item in codes]
	return codes

def is_tddate(session, date):
	if cal is None:
		cal = session.query("date", "is_open").from_statement(text("select date, is_open from calendar")).all()
		cal = {item[0]:item[1] for item in cal}
	return cal[date]

def get_ldate(date):
	ldate = {}
	ldate["year"] = date.year
	ldate["month"] = date.month - 1
	if date.month == 1:
		ldate["year"] -= 1
		ldate["month"] += 12
	ldate["quarter"] = ldate["month"] / 3
	return ldate