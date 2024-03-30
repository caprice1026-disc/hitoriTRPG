from flask import send_from_directory, request, jsonify
from flask_login import login_required, current_user
import os
from app import app
from app.models import GameStateEnum
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth import auth
from app.game_routes import game_bp
from flask import send_from_directory
import os
from app import app

# Blueprintの登録

app.register_blueprint(game_bp)
app.register_blueprint(auth) 

# すべてのフロントエンドのルートを捕捉する汎用的なルートハンドラ
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, 'build', path)):
        # リクエストされたパスが実際に存在する静的ファイルであれば、そのファイルを返す
        return send_from_directory(os.path.join(app.static_folder, 'build'), path)
    else:
        # それ以外の場合は、React Routerが処理するためにindex.htmlを返す
        return send_from_directory(os.path.join(app.static_folder, 'build'), 'index.html')

# ルーティングはReactRouterでフロントエンド側のルーティングを行う。
# そのため、フロントエンド側のビルドファイルを返すように変更
# 参考: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/#uploading-files