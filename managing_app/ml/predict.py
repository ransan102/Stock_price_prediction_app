import pandas as pd
from prophet import Prophet
import pandas_datareader as web
import matplotlib.pyplot as plt
import os

def save_fig_predict(code, column="Adj Close"):
    df = web.DataReader(code, data_source="yahoo", start="2000-01-01")
    df.reset_index(inplace=True)
    df_predict = df[["Date", column]].rename(columns={"Date":"ds", column: "y"})
    
    m = Prophet()
    m.fit(df_predict)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    
    fig1 = m.plot(forecast)
    fig2 = m.plot_components(forecast)
    
    fig1.savefig("./managing_app/images/predict1.png")
    fig2.savefig("./managing_app/images/predict2.png")
    return forecast