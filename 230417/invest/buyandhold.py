import numpy as np
from datetime import datetime
import pandas as pd

def bnh(df,col,start,end):

    if 'Date' in df.columns:
        df=df.set_index("Date")
        
    # 인덱스 시계열로 변경
    df.index=pd.to_datetime(df.index)
    start=datetime.strptime(start,'%Y%m%d').isoformat()
    end=datetime.strptime(end,'%Y%m%d').isoformat()
    df=df.loc[start:end]
    # 결측치,무한대 제외
    df=df.loc[~df.isin([np.nan , np.inf,-np.inf]).any(1)]

    df=df[[col]]
    
    df["daily_rtn"]=df[col].pct_change()
    df['st_rtn']=(1+df['daily_rtn']).cumprod()
    #df.index= df.index.astype('str')

    return df
    