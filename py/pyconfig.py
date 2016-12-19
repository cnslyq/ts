ENGINE = 'mysql://root:123456@127.0.0.1/test?charset=utf8'

INPUT_LIST = ['init', 'hist', 'cron', 'hm', 'hq', 'hy', 'ha', 'hs', 'real']
INIT_LIST = ['py.stock', 'py.macro', 'py.fund']
HISTORY_LIST = ['py.trade', 'py.tops', 'py.invest', 'py.fund']
DAILY_LIST = ['py.trade', 'py.invest', 'py.fund', 'py.other', 'py.news']
WEEKLY_LIST = ['py.tops', 'py.invest']
MONTHLY_LIST = ['py.stock', 'py.macro', 'py.tops', 'py.invest', 'py.basic', 'py.fund', 'py.other']
QUARTERLY_LIST = ['py.invest', 'py.basic', 'py.fund']
HISTORY_M_LIST = ['py.invest', 'py.other']
HISTORY_Q_LIST = ['py.invest', 'py.basic']
HISTORY_Y_LIST = ['py.other']
HISTORY_A_LIST = ['py.invest']
HISTORY_STOCK_LIST = ['py.trade']
HISTORY_FUND_LIST = ['py.fund']
REAL_LIST = ['py.news']

STOCK_SWITCH = 1
MACRO_SWITCH = 1
FUND_SWITCH = 1
TRADE_SWITCH = 1
TOPS_SWITCH = 1
INVEST_SWITCH = 1
OTHER_SWITCH = 1
BASIC_SWITCH = 1
NEWS_SWITCH = 1

TRADE_GC_NUM = 256
FUND_GC_NUM = 256
INVEST_GC_NUM = 256

pcnames = locals()
