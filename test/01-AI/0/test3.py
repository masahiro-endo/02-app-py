
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))

from sklearn import linear_model
from sklearn import svm
from sklearn.datasets import load_iris
iris = load_iris()



# 分類名
print (iris.data.shape)
print (iris.target_names)

# サンプルデータ
for data, target in zip(iris.data[:120], iris.target[:120]):
    print(data, target)


# 学習させる
clf: svm.SVC = svm.SVC(gamma="scale") # 学習器を作る
# その他の学習器（学習アルゴリズム）　
# lng = linear_model.LogisticRegression()
# model = linear_model.LinearRegression() #回帰モデル

clf.fit(iris.data, iris.target) #学習器に訓練データと教師データを渡す


# ランダムに見つけた値で分類できるかどうか確認する
# case versicolor
# test_data = [[ 5.5,  2.6,  1.4,  0.2]]
test_data = [[ 5.8, 2.7, 5.1, 1.9]]
print(clf.predict(test_data))






os.system("pause")