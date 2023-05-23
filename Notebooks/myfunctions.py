def load_files(path,iterable,extension):
    df_dict={}
    funct=eval('pd.read_'+extension)
    for i in range(len(iterable)):
        df_dict[i]=funct(path+iterable[i]+'.'+extension)
    return df_dict

def date_cols(df:pd.DataFrame,x:str):
    df['Month']=df., 'DayofMonth', 'DayOfWeek'
