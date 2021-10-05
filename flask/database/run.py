from app import app
from core.database import db
from models.models import User


@app.route('/')
def index():
    users = User.query.all()
    for row in users:
        print(row)

    return "OK"

if __name__ == '__main__':
    app.run(debug=True, port=8888, threaded=True) 

    