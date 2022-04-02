# coding: utf-8
from flask import Flask, render_template, request
from wtforms import Form, FloatField, StringField, validators, ValidationError, IntegerField, SubmitField
import joblib
import numpy as np
import pandas as pd
import json


# データの受け取り先は改訂予定
df = pd.read_excel(r"C:\Users\taipo\project_haitlab_2\Stock_price_prediction_app\managing_app\templates\data_j.xlsx", engine = 'openpyxl')
df

#33業種以外の物を抽出
special = df[df["33業種コード"] == "-"]

#33業種以外の銘柄名をリスト化
igai33 = ["ETF・ETN","REIT・ベンチャーファンド・カントリーファンド・インフラファンド","出資証券"]

#業種ごとに銘柄を辞書でまとめる1
data = {}
for content in igai33:
    kind = special[special["33業種区分"] == content]
    data[content] = kind[["銘柄名"]].to_numpy().reshape(1,-1).tolist()


#33業種を抽出する準備作業
df2 = df.replace({"-": np.nan})

#33業種を抽出
df3 = df2.dropna(subset = ["33業種区分"])

# 33業種をリスト化

gyousyu33 = ["水産・農林業","食料品","鉱業","石油・石炭製品","建設業","金属製品","ガラス・土石製品","繊維製品","パルプ・紙","化学","医薬品","ゴム製品","輸送用機器","鉄鋼","非鉄金属","機械","電気機器","精密機器","その他製品","情報・通信業","サービス業","電気・ガス業","陸運業","海運業","空運業","倉庫・運輸関連業","卸売業","小売業","銀行業","証券、商品先物取引業","保険業","その他金融業","不動産業"]

#業種ごとに銘柄を辞書でまとめる2

for content in gyousyu33:
    kind = df3[df3["33業種区分"] == content]
    data[content] = kind[["銘柄名"]].to_numpy().reshape(1,-1).tolist()

gyousyu33.extend(igai33)

def predict (parameters):
    model = joblib.load()
    return model

app = Flask(__name__)

class StockForm(Form):
    Kind = StringField("The Kind of Stock",
                       [validators.InputRequired("記入必須")])
    
    Year1 = IntegerField("年",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 2022)])
    
    Month1 = IntegerField("月",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 1, max = 12)])
    
    Day1 = IntegerField("日から",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 1, max = 31)])
    
    Year2 = IntegerField("年",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 2022)])
    
    Month2 = IntegerField("月",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 1, max = 12)])
    
    Day2 = IntegerField("日まで",
                         [validators.InputRequired("記入必須"),
                          validators.NumberRange(min = 1, max = 31)])
    
    submit = SubmitField("送信")





@app.route("/", methods=["GET", "POST"])
def predicts():
    form = StockForm(request.form)
    list_name = gyousyu33
    stock_data = data
    if request.method == "POST":
        if form.validate() == False:
            return render_template('index.html', form = form, list_name = list_name, stock_data = stock_data)
        else:
            
            return render_template('result.html')
    elif request.method == "GET":
        
        
        return render_template('index.html',form = form, list_name = list_name, stock_data = stock_data)
    
    
if __name__ == "__main__":
    app.run(debug = True)