from prophet import Prophet
import pandas_datareader as web
import datetime

def save_fig_predict(code, start, end, column="Adj Close"):
    df = web.DataReader(code, data_source="yahoo", start="2000-01-01")
    df.reset_index(inplace=True)
    df_predict = df[["Date", column]].rename(columns={"Date":"ds", column: "y"})
    
    m = Prophet()
    m.fit(df_predict)
    
    dt_now = df_predict["ds"].tolist()[-1]
    td = end - dt_now
    period = td.days
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    
    fig1 = m.plot(forecast)
    fig2 = m.plot_components(forecast)
    
    fig1.savefig("./managing_app/images/predict1.png")
    fig2.savefig("./managing_app/images/predict2.png")
    
    benefit = forecast[forecast["ds"]==end]["yhat"].values[0] - forecast[forecast["ds"]==start]["yhat"].values[0]
    
    return benefit

if __name__ == "__main__":
    start = datetime.datetime(2022,4,2)
    end = datetime.datetime(2023,4,2)
    print(save_fig_predict("9020.T", start, end))