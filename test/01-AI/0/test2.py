
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn import datasets



iris = datasets.load_iris()
X = iris.data
y = iris.target

estimator = KMeans(n_clusters=3)
estimator.fit(X)

fig = plt.figure(figsize=(18, 8))
ax = fig.add_subplot(121, projection='3d', elev=45, azim=135)
ax.scatter(X[:, 3], X[:, 0], X[:, 2],
           c=estimator.labels_.astype(np.float), edgecolor='k')

ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('KMeans 3 clusters')
ax.dist = 12

ax = fig.add_subplot(122, projection='3d', elev=45, azim=135)

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))

y = np.choose(y, [2, 1, 0]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')

ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Ground Truth')
ax.dist = 12

fig.show()



