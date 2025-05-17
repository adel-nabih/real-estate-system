from .user import User

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
