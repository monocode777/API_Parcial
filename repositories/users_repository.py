from models.users_model import User

class UserRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id):
        return self.db.query(User).filter_by(id=user_id).first()

    def create_user(self, username, password, role="user"):
        new_user = User(username=username, password=password, role=role)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id, username=None, password=None):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return True
