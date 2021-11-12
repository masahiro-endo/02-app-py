
import os
from typing import Any, List
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))
from app import app
import pandas as pd
from flask import Flask, request, render_template




@app.route('/', methods=['POST', 'GET'])
def index():
    df = pd.read_excel('sample.xlsx', sheet_name=['Listitem1', 'Listitem2', 'Listitem3'])
    data_1 = df['Listitem1'].to_numpy().tolist()
    data_2 = df['Listitem2'].to_numpy().tolist()
    data_3 = df['Listitem3'].to_numpy().tolist()

    return render_template('index.html', 
               title='メインメニュー', 
               listitem_1=data_1, 
               listitem_2=data_2, 
               listitem_3=data_3 
               )

@app.route('/output/', methods = ['POST', 'GET'])
def output():
    if request.method == 'POST':
        if (request.form.get('search') != None):
            pass
        if (request.form.get('chkbtn1') != None):
            pass
        opt1 = request.form.get('optbtn1')
        
        result  = request.form
        prm_1: Any = str(result['listitem_1'])
        prm_2: Any = str(result['listitem_2'])
        prm_3: Any = str(result['listitem_3'])

        # 90X をインデックス指定すると何故かエラーになる
        df = pd.read_excel('sample.xlsx', sheet_name=['BODY'], index_col='APP')
        res_1: Any = df['BODY'].loc[f"{prm_1}", 'RPY_GRP']
        res_2: Any = df['BODY'].loc[f"{prm_1}", 'INQ']
        res_3: Any = df['BODY'].loc[f"{prm_1}", 'ANS']

        column: List[str] = []
        results: List[List[str]] = []
        column = []
        column.append(res_1)
        results.append(column)
        column = []
        column.append(res_2)
        results.append(column)
        column = []
        column.append(res_3)
        results.append(column)



        column: List[str] = []
        lists: List[List[str]] = []

        column = []
        column.append(prm_1)
        lists.append(column)
        column = []
        column.append(prm_2)
        lists.append(column)
        column = []
        column.append(prm_3)
        lists.append(column)

        return render_template('output.html',
                lists=lists,
                results=results
                )
    else:
        return render_template('output.html')





if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)

