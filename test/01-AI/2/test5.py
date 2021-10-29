
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))





import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
sns.set(font="IPAexGothic")
import sklearn
from sklearn.linear_model import LinearRegression


df1=pd.read_excel('diabetes.xlsx')
	
df1.head()
df1.info()

df1['1年後の疾患進行度'].hist(bins=50,figsize=(7,5))
plt.xlabel('1年後の疾患進行度')
plt.ylabel('人数')


plt.figure(figsize=(7, 5))
plt.scatter(df1['1年後の疾患進行度'],df1['BMI'])
plt.xlabel('1年後の疾患進行度')
plt.ylabel('BMI')


lreg = LinearRegression()
sns.lmplot('1年後の疾患進行度','BMI',data = df2,height=5.5, aspect=1.2)


X=df2.drop('1年後の疾患進行度',1)
Y=df2['1年後の疾患進行度']


lreg.fit(X,Y)


test1 = np.array([[24,1,25,84,198,131,40,5,5,89]])
lreg.predict(test1)
test1 = np.array([[50,2,30,100,180,120,50,4,5,77]])
lreg.predict(test1)
test1 = np.array([[35,1,25,80,130,50,60,4,4,60]])
lreg.predict(test1)


df2 = df1.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))


df2.head()


df3=pd.DataFrame({'項目':X.columns,'係数':np.abs(lreg.coef_)}).sort_values(by='係数',ascending=False) 
df3








os.system("pause")