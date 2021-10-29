

import matplotlib.pyplot as plt

'''

aa: int = 0
print(f"{aa}")


year = [1980, 1985, 1990, 2000, 2010, 2018]
weight = [3, 15, 25, 55, 62, 58]
plt.plot(year, weight)
plt.show()


x = []
y = []
for i in range(0,10):
    x.append(i)
    y.append(i**2)
print(x)
print(y)
plt.plot(x,y)
plt.show()



from matplotlib.pyplot import figure
import requests, bs4
font = {"family": "TakaoGothic"}
matplotlib.rc('font', **font)

TEMPERATURE = []
for x in range(1, 9):
    loop_url = "res" + str(x)
    loop_url = requests.get('http://www.wbgt.env.go.jp/graph_ref_td.php?region=07&prefecture=61&point=61286&refId='+str(x))
    loop_soup = "soup" + str(x)
    loop_soup = bs4.BeautifulSoup(loop_url.text, "html.parser")
    loop_elems = "elems" + str(x)
    loop_elems = loop_soup.select('span.num')
    loop_number = "number" + str(x)
    loop_number = loop_elems[0].getText()
    temp = loop_number[0:4]
    TEMPERATURE.append(temp)
print(TEMPERATURE)

figure(num=None, figsize=(10, 6))
point = ['基準','駐車場','交差点','バス停','住宅地','子供','ビニールハウス','体育館']
temp = [TEMPERATURE]
plt.title("熱中症注意！！京都市内各箇所の気温目安")
plt.xlabel("場所")
plt.ylabel("気温（℃）")
plt.scatter(point,temp, s=300)
plt.grid()
plt.show()


'''

import math
import numpy as np
from matplotlib import pyplot


pi: float = math.pi

x: np.ndarray = np.linspace(0, 2*pi, 100)
sin_y = np.sin(x)
cos_y = np.cos(x)

pyplot.plot(x, sin_y, label='sin')
pyplot.plot(x, cos_y, label='cos')

#グラフタイトル
pyplot.title('Sin And Cos Graph')

#グラフの軸
pyplot.xlabel('X-Axis')
pyplot.ylabel('Y-Axis')

#グラフの凡例
pyplot.legend()

pyplot.show()


