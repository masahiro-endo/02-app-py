
import os
from typing import Any, List
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))
from app import app
import pandas as pd
from flask import Flask, request, render_template




# Excelの読み込みと顧客一覧抽出
def read_excel(filename: str,sheetname: str, columnname: str) -> Any:
    df = pd.read_excel(filename, sheet_name=None)

    return df[sheetname].loc[:,columnname].unique()

data_1 = read_excel('sample.xlsx','Listitem1','ITEMNAME')
data_2 = read_excel('sample.xlsx','Listitem2','ITEMNAME')
data_3 = read_excel('sample.xlsx','Listitem3','ITEMNAME')



@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', 
               title='メインメニュー', 
               listitem_1=data_1, 
               listitem_2=data_2, 
               listitem_3=data_3 
               )

@app.route('/output/', methods = ['POST', 'GET'])
def output():
    if request.method == 'POST':
        result  = request.form
        prm_1: str = str(result['listitem_1'])
        prm_2: str = str(result['listitem_2'])
        prm_3: str = str(result['listitem_3'])
    
        texts: List[str] = []
        lists: List[List[str]] = []

        texts = []
        texts.append(prm_1)
        lists.append(texts)

        texts = []
        texts.append(prm_2)
        lists.append(texts)

        texts = []
        texts.append(prm_3)
        lists.append(texts)

        return render_template('output.html',
                lists=lists
                )
    else:
        return render_template('output.html')





if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)

