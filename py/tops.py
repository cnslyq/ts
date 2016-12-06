import tops_freq

def weekly(session, engine):
	tops_freq.tops(5, engine)

def monthly(session, engine):
	tops_freq.tops(30, engine)
