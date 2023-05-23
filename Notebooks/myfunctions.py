import numpy as np, pandas as pd, seaborn as sns, matplotlib as plt
from sklearn.model_selection import train_test_split
import datetime
from sklearn.model_selection import train_test_split
from tinydb import TinyDB, Query

def date_cols(df:pd.DataFrame,x:str):
    df['Month']=df[x].strftime('%m').astype('int')
    df['DayofMonth']=df[x].strftime('%d').astype('int')
    df['DayOfWeek']=df[x].strftime('%u').astype('int')

def create_db(path:str):
    df=pd.read_parquet('../Data/Raw/Data.parquet')
    db=TinyDB('db.json')
    for i in len(df):
        db.insert({c:df[c][i] for c in df.columns})
        
def outcome(df_):
    if df_['Cancelled']:
        return 'Cancelled'
    if df_['ArrDelayMinutes']>0:
        return 'Delayed'
    if df_['Diverted']:
        return 'Diverted'
    return 'OK'
