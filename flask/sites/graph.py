
#!/usr/bin/python
#-*- encoding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io as cStringIO
from flask import Flask, render_template, make_response


app = Flask(__name__)

@app.route("/")
def main():
   sns.set(font="serif")
   fig, ax = matplotlib.pyplot.subplots()
   flip = 1
   x = np.linspace(0, 14, 100)
   for i in range(1, 7):
      ax.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

   canvas = FigureCanvasAgg(fig)
   buf = cStringIO.StringIO()
   canvas.print_png(buf)
   data = buf.getvalue()

   response = make_response(data)
   response.headers['Content-Type'] = 'image/png'
   response.headers['Content-Length'] = len(data)
   return response



if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8888, debug=True)