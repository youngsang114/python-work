import numpy as np
import pandas as pd
from datetime import datetime

def momentum1(df,col='Close',start='20100101',end='20230101'):
    
    # 만약에 인덱스가 Date가 아니면? Date컬럼을 인덱스로 변경
    if 'Date' in df.columns:
        df=df.set_index("Date")
        
    # start,end를 시계열로 변경한다
    start=datetime.strptime(start,'%Y%m%d').isoformat()
    end=datetime.strptime(end,'%Y%m%d').isoformat()

    # 결측치와 이상치를 제거
    df=df.loc[~df.isin([np.nan,np.inf,-np.inf]).any(axis=1)]
    # 수정종가를 제외한 나머지 컬럼 삭제
    df=df[[col]]
    # 인덱스를 시계열로 변경
    df.index=pd.to_datetime(df.index,format="%Y-%m-%d")

    df=df.loc[start:end]

    # 'STD-YM'컬럼을 생성
    df['STD-YM']=list(map(lambda x: datetime.strftime(x,'%Y-%m'),df.index))


    return df

def momentum2(df):
    col=df.columns[0]

    # df2=df.loc[df['STD-YM'] !=df.shift(-1)['STD-YM']]
    # 월별 마지막날의 데이터만 추출

    df2= pd.DataFrame()
    # 리스트값을 만들어서 for문을 돌림
    _list=df["STD-YM"].unique()

    for i in _list:
        last_df=df.loc[df["STD-YM"] ==i].tail(1)
        df2 =pd.concat([df2, last_df])

    df2['BF_1M']=df2.shift(1)[col].fillna(0)
    df2['BF_12M']=df2.shift(12)[col].fillna(0)
    
    return df2

def momentum3(df1,df2):

    col=df1.columns[0]

    df1['trade']='' 
    for i in df2.index:
        signal=''

        # 절대 모멘텀 계산
        monentum_index= (df2.loc[i,"BF_1M"]/ df2.loc[i,"BF_12M"]) - 1
        
        # 절대 모멭넘 지표에 따라서 True / Fasle 로 구분
        flag = True if((monentum_index >0 ) and (monentum_index!=np.inf) and (monentum_index !=-np.inf)) else False

        if flag:
            signal ='buy'
        #print('날짜:',i, "모멘텀 인덱스 :", monentum_index, 'flag :',flag, 'signal :', signal)

        df1.loc[i,'trade']=signal

        df1['return']=1.0

    rtn=1.0
    buy=0.0
    sell=0

    # index의 데이터 값이 unique해서 
    for i in df1.index:         
        # 구매한 날을 체크, 구매가 지정
        if (df1.loc[i,"trade"] == "buy") and (df1.shift(1).loc[i,"trade"]== ""):
            buy=df1.loc[i,col]
            # print (buy)
            # 이 시점에 사고 그 값을 변수 buy 값에 저장해놓는다
            # print("구매일:",i ,'구매가격',buy)

        # 판매한 날을 체크, 판매가 지정, 수익률 계산
        elif (df1.shift(1).loc[i,"trade"]=="buy") and (df1.loc[i,"trade"]==""):
            sell= df1.loc[i,col]
            rtn= (sell-buy)/buy +1
            df1.loc[i,'return']=rtn
    acc_rtn=1.0

    for i in df1.index:

        acc_rtn *= df1.loc[i,'return']
        df1.loc[i,'acc_rtn']= acc_rtn
        
    print('누적 수익율:',acc_rtn)

    return df1