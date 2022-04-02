import pandas as pd
from prophet import Prophet
import pandas_datareader as web

def predict(code, period, column):
    df = web.DataReader(code, data_source="yahoo", start="2000-01-01")
    df.reset_index(inplace=True)
    df_predict = df[["Date", column]].rename(columns={"Date":"ds", column: "y"})
    
    m = Prophet()
    m.fit(df_predict)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    
    
    return forecast
    