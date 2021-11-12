
from typing import Any
from flask import Flask


config = {
    "default": "config.config.AppConfig"
}


def create_app():

    app: Any = Flask(__name__, instance_relative_config=True)

    # 設定はオブジェクトとして読み込む
    app.config.from_object(config['default'])
    # センシティブな設定はインスタンスフォルダ内の設定で上書きする
    app.config.from_pyfile('config.cfg', silent=True)
    
    return app

app = create_app()

