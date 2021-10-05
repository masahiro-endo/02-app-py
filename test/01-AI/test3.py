
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))

from sklearn.datasets import load_iris
iris = load_iris()

print (iris.data.shape)
print (iris.target_names)










os.system("pause")