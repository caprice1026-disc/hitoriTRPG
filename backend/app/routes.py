from flask import send_from_directory
from flask_login import login_required, current_user
import os
from app import app

@app.route('/')
def index():
    # フロントエンドのビルドファイルを返す。npm run buildを行う前後でパスが変わるため、os.path.joinを使ってパスを結合
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'frontend', 'build'), 'index.html')

@app.route('/game')
@login_required
def game():
    # フロントエンドのビルドファイルを返す。上記のindex()と同様の点に留意すること。
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'frontend', 'build'), 'index.html')

#ルーティングはReactRouterでフロントエンド側のルーティングを行う。
#そのため、フロントエンド側のビルドファイルを返すように変更
#参考: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/#uploading-files

