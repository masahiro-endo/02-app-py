
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))


import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix



data = np.loadtxt('data.csv', delimiter=',')
y = data[:,0].astype(int)
x = data[:,1:3]

clf = svm.SVC(gamma="scale")
# 学習させる
clf.fit(x, y)

data_test = np.loadtxt('data_test.csv', delimiter=',') 
test_y = data_test[:,0].astype(int)
test_x = data_test[:,1:3]

print('正解',test_y)
# 学習したデータと比較して推測する
print('推測した結果',clf.predict(test_x))
print('推測した結果の正解率',clf.score(test_x, test_y))





os.system("pause")