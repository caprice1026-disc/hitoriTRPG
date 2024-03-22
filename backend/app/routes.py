from flask import send_from_directory, request, jsonify
from flask_login import login_required, current_user
import os
from app import app
from app.models import GameStateEnum
from app import db

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


# 下記からAPIのエンドポイントを追加していく予定。ファイルの分離も検討すること。

@app.route('/game/action', methods=['POST'])
@login_required
def game_action():
    # リクエストからプレイヤーの行動を取得
    action = request.json.get('action')
    # ゲームセッションを取得し、進行状況を更新
    # 注意: current_user.game_session.update_progress(action) の実装が必要
    if hasattr(current_user, 'game_session') and callable(getattr(current_user.game_session, 'update_progress', None)):
        current_user.game_session.update_progress(action)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Game progress updated.'})
    else:
        return jsonify({'status': 'error', 'message': 'Game session update method not implemented.'})

# ルーティングはReactRouterでフロントエンド側のルーティングを行う。
# そのため、フロントエンド側のビルドファイルを返すように変更
# 参考: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/#uploading-files