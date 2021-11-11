
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))
from app import app
import pandas as pd
from flask import Flask, render_template




# Excelの読み込みと顧客一覧抽出
def read_excel(filename="sample.xlsx"):
    df = pd.read_excel(filename, sheet_name=None)

    return df["Sheet2"].loc[:,"user_name"].unique()

data_list = read_excel()



@app.route('/')
def index():
    return render_template("index.html", data_list=data_list)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)

