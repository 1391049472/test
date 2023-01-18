import pandas as pd
from sqlalchemy import create_engine
import mplfinance as mpl
from tqdm import tqdm

def get_calendar_mysql(startdate,endate):
    Sign_order = "mysql+pymysql://utopia:1391049472@localhost/calendar"
    engine_ts = create_engine(Sign_order) 
    sql_sent = "SELECT DISTINCT * FROM Trade_calendar where cal_date between " + startdate + " AND " + endate
    res = pd.read_sql_query(sql_sent, engine_ts)
    return res


def get_from_mysql(database,date,stock_code): #可能会需要用到不同的数据（比如行情数据和停牌数据）
    Sign_order = "mysql+pymysql://utopia:1391049472@localhost/" + database
    engine_ts = create_engine(Sign_order)
    res = pd.DataFrame()
    for i in tqdm(range(len(date))):
        Today = date.iloc[i].cal_date
        Today_sql = "`" +Today+"`"
        sql_sent = "SELECT DISTINCT *  FROM " + Today_sql + " where ts_code = "+ stock_code#"'600031.SH'"
        df = pd.read_sql_query(sql_sent, engine_ts)
        res = pd.concat([res, df], axis=0)
    return res

calendar = get_calendar_mysql('20200115', '20200205')
print(calendar[calendar.is_open == 1])
print(calendar.iloc[0].cal_date)

calendar = calendar[calendar.is_open == 1]
df = get_from_mysql('daily_data', calendar, "'600031.SH'")
print(df)
df = df.loc[:, ['trade_date', 'open', 'high', 'low', 'close', 'vol']]
print(df)
df.rename(columns={
        'trade_date': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'vol': 'Volume'
    },
        inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_index()
df.set_index(['Date'], inplace=True)
print(df)
#cursor = Cursor(ax, horizOn = False, useblit=True, color='r', linewidth=1, linestyle='dotted')
a = mpl.plot(df, type='candle', volume=True) 
