from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import py.pylog as pl
import conf

engine = create_engine(conf.ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

pl.log("data initialization start...")
for item in conf.INIT_LIST:
	pl.log(item + " initialization start...")
	importstring = "import " + item + " as module"
	exec importstring
	module.init(engine, session)
	pl.log(item + " initialization done")
pl.log("data initialization done")
