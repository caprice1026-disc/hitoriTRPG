from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os

from services import (
    create_player, 
    update_player_status, 
    add_player_condition, 
    update_player_inventory, 
    delete_player
)
from models import db, GameSession, Player, GameStateEnum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/player', methods=['POST'])
def api_create_player():
    """新しいプレイヤーを作成するAPIエンドポイント"""
    data = request.json
    name = data.get('name')
    job = data.get('job')
    if not name or not job:
        return jsonify({"message": "Name and Job are required"}), 400

    try:
        player = create_player(name, job)
        return jsonify({"message": "Player created", "player_id": player.id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/player/<int:player_id>/status', methods=['PUT'])
def api_update_player_status(player_id):
    """既存のプレイヤーのステータスを更新するAPIエンドポイント"""
    status_changes = request.json
    try:
        update_player_status(player_id, status_changes)
        return jsonify({"message": "Player status updated"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/player/<int:player_id>/condition', methods=['POST'])
def api_add_player_condition(player_id):
    """プレイヤーに新しいコンディションを追加するAPIエンドポイント"""
    data = request.json
    condition_type = data.get('condition_type')
    value = data.get('value')
    if not condition_type or not value:
        return jsonify({"message": "Condition type and value are required"}), 400

    try:
        add_player_condition(player_id, condition_type, value)
        return jsonify({"message": "Condition added"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/player/<int:player_id>/inventory', methods=['PUT'])
def api_update_player_inventory(player_id):
    """プレイヤーのインベントリを更新するAPIエンドポイント"""
    data = request.json
    item_name = data.get('item_name')
    quantity = data.get('quantity')
    if not item_name or quantity is None:
        return jsonify({"message": "Item name and quantity are required"}), 400

    try:
        update_player_inventory(player_id, item_name, quantity)
        return jsonify({"message": "Inventory updated"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/player/<int:player_id>', methods=['DELETE'])
def api_delete_player(player_id):
    """プレイヤーを削除するAPIエンドポイント"""
    try:
        delete_player(player_id)
        return jsonify({"message": "Player deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/session', methods=['POST'])
def api_create_session():
    """新しいゲームセッションを作成するAPIエンドポイント"""
    data = request.json
    player_id = data.get('player_id')
    if not player_id:
        return jsonify({"message": "Player ID is required"}), 400

    new_session = GameSession(player_id=player_id, state=GameStateEnum.PROGRESSING, progress_log="")
    db.session.add(new_session)
    try:
        db.session.commit()
        return jsonify({"message": "Game session created", "session_id": new_session.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/api/session/<int:session_id>/log', methods=['PUT'])
def api_update_session_log(session_id):
    """ゲームセッションのログを更新するAPIエンドポイント"""
    data = request.json
    progress_log = data.get('progress_log')
    if progress_log is None:
        return jsonify({"message": "Progress log is required"}), 400

    session = GameSession.query.get(session_id)
    if session:
        session.progress_log = progress_log
        try:
            db.session.commit()
            return jsonify({"message": "Progress log updated"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "Session not found"}), 404
    
# SSEの関数の例
'''
@game_bp.route('/action', methods=['POST'])
# @jwt_required()
def stream_game_action(json):
    # SSEヘッダを設定
    response = Response(stream_openai_response(json), mimetype="text/event-stream")
    response.headers.set('Cache-Control', 'no-cache')
    return response
'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# ルーティングはReactRouterでフロントエンド側のルーティングを行う。
# そのため、フロントエンド側のビルドファイルを返すように変更
# 参考: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/#uploading-files