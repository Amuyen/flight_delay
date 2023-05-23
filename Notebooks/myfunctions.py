import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from tinydb import TinyDB, Query

def cols_types(df:pd.DataFrame):
    df['Month']=[datetime.strftime(df['FlightDate'][i],'%m') for i in df.index]
    df['DayOfWeek']=[datetime.strftime(df['FlightDate'][i],'%u') for i in df.index]
    df['DayOfMonth']=[datetime.strftime(df['FlightDate'][i],'%d') for i in df.index]
    df['CRSDepTime']=df['CRSDepTime'].apply(lambda x: convert_to_min(x))
    df['CRSArrTime']=df['CRSArrTime'].apply(lambda x: convert_to_min(x))
    df['Flight_Number_Marketing_Airline']=df['Flight_Number_Marketing_Airline'].astype('object')
    df['Flight_Number_Operating_Airline']=df['Flight_Number_Operating_Airline'].astype('object')
    return df

def convert_to_min(x):
    if x<10:
        string= '00:0'+str(x)
    elif x<60:
        string= '00:'+str(x)
    elif x<960:
        string= '0'+str(x)[0]+':'+str(x)[1:]
    else:
        string=str(x)[0:2]+':'+str(x)[2:]
    dt=datetime.strptime(string,'%H:%M')+timedelta(days=25569)
    return dt.timestamp()


def create_db(df):
    db=TinyDB('db.json')
    for i in len(df):
        db.insert({c:df[c][i] for c in df.columns})

def outcome(df):
    if df['Cancelled']:
        return 'Cancelled'
    if df['ArrDelayMinutes']>0:
        return 'Delayed'
    if df['Diverted']:
        return 'Diverted'
    return 'OK'

def filtered(df):
    thresh=max(df['FlightDate'])
    df=df[thresh<(df['FlightDate']+pd.Timedelta(days=730))]
    return df[~df['Diverted']]

def add_marketing(df):
    companies=df.groupby(['IATA_Code_Operating_Airline','Airline']).agg('count').reset_index()
    return {companies['IATA_Code_Operating_Airline'][i]:companies['Airline'][i] for i in range(len(companies))}

def clean(df):
    if df['FlightDate'].dtype=='object':
        df['FlightDate']=pd.to_datetime(df['FlightDate'])
    df=filtered(df)
    df['result']=df.apply(lambda x: outcome(x), axis=1)
    df=cols_types(df)
    df=df[['Month','DayofMonth','DayOfWeek','Origin', 'Dest','IATA_Code_Marketing_Airline','IATA_Code_Operating_Airline','Flight_Number_Marketing_Airline','Flight_Number_Operating_Airline','ArrDelayMinutes','Distance','CRSDepTime','CRSArrTime','result']] 
    return df
