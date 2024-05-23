from models import db, Player, PlayerStatus, PlayerCondition, PlayerInventory, World
from sqlalchemy.exc import SQLAlchemyError

def create_player(name, job):
    """新しいプレイヤーを作成してデータベースに追加する"""
    new_player = Player(name=name, job=job)
    new_status = PlayerStatus(player=new_player)  # 初期ステータスを付与
    db.session.add(new_player)
    db.session.add(new_status)
    try:
        db.session.commit()
        return new_player
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Creating player failed: {e}")

def update_player_status(player_id, status_changes):
    """指定されたプレイヤーのステータスを更新する"""
    player = Player.query.get(player_id)
    if player and player.status:
        try:
            player.update_status(status_changes)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Updating status failed: {e}")

def add_player_condition(player_id, condition_type, value):
    """プレイヤーに新しいコンディションを追加する"""
    try:
        player = Player.query.get(player_id)
        if player:
            player.add_condition(condition_type, value)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Adding condition failed: {e}")

def update_player_inventory(player_id, item_name, quantity):
    """プレイヤーのインベントリを更新する"""
    try:
        player = Player.query.get(player_id)
        if player:
            player.update_inventory(item_name, quantity)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Updating inventory failed: {e}")

def delete_player(player_id):
    """プレイヤーのデータをデータベースから削除する"""
    try:
        player = Player.query.get(player_id)
        if player:
            db.session.delete(player)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Deleting player failed: {e}")
    
def create_world(name, description):
    try:
        new_world = World(name=name, description=description)
        db.session.add(new_world)
        db.session.commit()
        return new_world
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Failed to create world: {str(e)}")

    
    """プレイヤーのデータをデータベースから削除する"""
    """ワールドの各種サービス"""

