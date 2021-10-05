
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))





from sklearn import datasets



digits = datasets.load_digits()

import matplotlib.pyplot as plt
plt.matshow(digits.images[0], cmap="Greys")
plt.show()









os.system("pause")