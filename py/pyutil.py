from sqlalchemy import text

def get_codes(session):
	codes = session.query("code").from_statement(text("select code from stock_info")).all()
	codes = [item[0].encode('utf8') for item in codes]
	return codes
