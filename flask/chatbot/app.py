
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))

from flask import Flask, render_template, jsonify, request, json
app = Flask(__name__)

# 初期表示
@app.route('/')
def page_load():
    return render_template('chat.html')


# 質問を受け取って回答を返す
@app.route('/question', methods=['POST'])
def answer():
    question = request.form['question']
    return_json = {
            "information":"最も関連度の高い回答はこちらです。",
            "hit_question": question,
            "hit_answer": "Answer"
    }
    return jsonify(values=json.dumps(return_json))


from janome.analyzer import Analyzer# 形態素解析ライブラリ 「pip install janome」
from janome.charfilter import *
from janome.tokenfilter import *

# 形態素解析の設定
token_filters = [CompoundNounFilter(),# 連続する名詞の複合名詞化
                 POSKeepFilter(['名詞','形容詞']), # 抽出する品詞の指定
                 UpperCaseFilter()] # アルファベットを大文字に変換
a = Analyzer(token_filters=token_filters)

# 分かち書き
def separate_word(question):
    word_list = []
    for token in a.analyze(question):
        print(str(token))
        word_list.append(str(token).split()[0])
    return word_list




import openpyxl

# 問い合わせ台帳の読み込み
excel_path = "./data/QA.xlsx"
wb = openpyxl.load_workbook(excel_path)
sheet = wb.worksheets[0]
q_col = "B"# 質問の列（ABC...）
a_col = "C"# 回答の列（ABC...）

# エクセルを単語リストで検索し、行番号とヒット数を返す
def search_question(word_list):
    row_points = []
    for i in range(200):#検索対象の行数（いったん200）
        point = 0
        q_cell = sheet[q_col + str(i+1)]
        a_cell = sheet[a_col + str(i+1)]
        if q_cell.value is not None and a_cell.value is not None:
            for keyword in word_list:
                if keyword.casefold() in q_cell.value.casefold():# 大文字小文字区別しない
                    point += 1
            if point > 0: row_points.append([i+1,point])
    return row_points



# 管理画面(GET)
@app.route('/admin',methods=['GET'])
def adminpage_load():
    qa_table = []
    for i in range(200):#Excel何行目まで見るか
        q_cell = sheet[q_col + str(i+1)]
        a_cell = sheet[a_col + str(i+1)]
        if q_cell.value is not None and a_cell.value is not None:
            qa_table.append([i+1,q_cell.value,a_cell.value])
    return render_template('admin.html',qa_table=qa_table)

# 管理画面(POST:Excelのアップロード)
@app.route('/admin',methods=['POST'])
def upload():
    print("upload()処理開始")
    # ファイル存在チェック
    if 'file' not in request.files:
        print("ファイルが存在しない。")
        return redirect(request.url)
    # データの取り出し
    file = request.files['file']
    filename = file.filename
    print("ファイル名：" + filename)
    # ファイル名チェック
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xlsx','xls']:
        #filename = secure_filename(file.filename)# 危険な文字を削除（サニタイズ処理）★2バイト文字消えちゃうので一旦外す
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))# ファイルの保存
        print("upload()ファイル保存完了")
        # アップロード後のページに転送
        return redirect(request.url)
    else:
        print("ファイル名が存在しない。またはエクセル形式でない。")
        return redirect(request.url)
    #TODO アップしたエクセルを分かち書きにする
    #TODO wikiモデルに追加学習させる
    #TODO saveする


# キャッシュしない
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r







if __name__ == "__main__":
    app.run(debug=True)

