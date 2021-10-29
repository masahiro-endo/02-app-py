
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))



# 気温	
# dd

# 天気
# 0 :晴れ
# 1 :雨
# 2 :曇り

# 一番売れる商品
# 0 :かき氷
# 1 :アイス
# 2 :ドーナツ
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score


#csvファイルの読み込み
npArray = np.loadtxt("in.csv", delimiter = ",", dtype = "float")
print("csvファイルが格納された配列を出力")
print(npArray)
# 説明変数の格納
x = npArray[:, 0:2]
print("説明変数を出力\n", x)
#目的変数の格納
y = npArray[:, 2:3].ravel()
print("目的変数を出力\n", y)
#学習用データと評価用データに分割
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
print("学習用の目的変数を出力\n", y_train)
print("学習用の説明変数を出力\n", x_train)
print("評価用の目的変数を出力\n", y_test)
print("評価用の説明変数を出力\n", x_test)
#モデルに決定木を選択
clf = tree.DecisionTreeClassifier()
#学習
clf.fit(x_train, y_train)
#評価用データを使って予測
predict = clf.predict(x_test)
print("評価結果を出力\n", predict)
print("正解率を出力\n", accuracy_score(y_test, predict))







os.system("pause")