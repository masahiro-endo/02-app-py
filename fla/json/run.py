from flask import Flask, jsonify

app = Flask(__name__)

#json ascii -> unescape
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def getjson():
  result = {
      "firstname": "佐藤",
      "lastname": "太郎",
  }
  return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True) 

    