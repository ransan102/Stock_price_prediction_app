# coding: utf-8
from flask import Flask, render_template, request
from wtforms import Form, FloatField, StringField, validators, ValidationError, IntegerField, SubmitField
import joblib
import numpy as np
import pandas as pd

from ml import predict


# データの受け取り先は改訂予定
df = pd.read_excel("./managing_app/templates/data_j.xlsx", engine = 'openpyxl')
df = df[["コード","銘柄名","市場・商品区分", "33業種コード", "33業種区分"]]

#33業種以外の物を抽出
special = df[df["33業種コード"] == "-"]

#33業種以外の銘柄名をリスト化
igai33 = list(set(special["市場・商品区分"].tolist()))

#業種ごとに銘柄を辞書でまとめる1
data = {}
for content in igai33:
    kind = special[special["市場・商品区分"] == content]
    data[content] = kind["銘柄名"].tolist()

#33業種を抽出
df_33 = df[(df["33業種コード"] != "-") & (df["33業種区分"] != "-")] 


# 33業種をリスト化
gyousyu33 = list(set(df_33["33業種区分"].tolist()))

#業種ごとに銘柄を辞書でまとめる2
for content in gyousyu33:
    kind = df_33[df_33["33業種区分"] == content]
    data[content] = kind["銘柄名"].tolist()

gyousyu33.extend(igai33)









app = Flask(__name__)

class StockForm(Form):
    
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

class KindForm(Form):
    submit = SubmitField("送信")



@app.route("/", methods=["GET", "POST"])
def predicts():
    form = StockForm(request.form)
    list_name = gyousyu33
    stock_data = data
    
    if request.method == "POST":
        if form.validate() == False:
            kind = request.form.get("kind")
            return render_template('index2.html', form = form,  stock_data = stock_data, kind = kind)
        else:
            name = request.form.get("name")
            predict.save_fig_predict(name)
            path1 = './managing_app/images/predict1.png'
            path2 = './managing_app/images/predict2.png'
            
            return render_template('result.html' ,Path1 = path1, Path2 = path2)
    elif request.method == "GET":
        submit = KindForm(request.form)
        
        return render_template('index.html', list_name = list_name, submit = submit)
    
    
if __name__ == "__main__":
    app.run(debug = True)