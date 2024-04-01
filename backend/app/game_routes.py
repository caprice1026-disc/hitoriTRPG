from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# dbの循環参照を行わないか後で確認
from app import db
from services.openai_service import openai_call
# 必要なモデルや関数をインポート

game_bp = Blueprint('game', __name__, url_prefix='/api/game')

@game_bp.route('/action', methods=['POST'])
@jwt_required()
def game_action(json):
    # ここにゲームアクションの処理を実装
    openai_call(json)
    
    return jsonify({'status': 'success', 'message': 'Action processed.'})

# 他のゲーム関連のエンドポイントもこのファイルに追加