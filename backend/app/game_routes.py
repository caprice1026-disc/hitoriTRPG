from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
# dbの循環参照を行わないか後で確認
from app import db
from services.openai_service import openai_call
from services.openai_service import stream_openai_response
# 必要なモデルや関数をインポート

game_bp = Blueprint('game', __name__, url_prefix='/api/game')

@game_bp.route('/action', methods=['POST'])
@jwt_required()
def stream_game_action(json):
    # SSEヘッダを設定
    response = Response(stream_openai_response(json), mimetype="text/event-stream")
    response.headers.set('Cache-Control', 'no-cache')
    return response

# 他のゲーム関連のエンドポイントもこのファイルに追加