from model.dao.UserDAO import UserDAO
from model.User import User


class UserController:
    def __init__(self):
        self.user_dao = UserDAO()

    def lay_tc(self):
        try:
            return self.user_dao.lay_tc()
        except Exception as e:
            print(e)

    def lay_bang_id(self, id):
        try:
            return self.user_dao.lay_bang_id(id)
        except Exception as e:
            print(e)

    def them(self, ten, dia_chi, sdt):
        try:
            user = User(ten, dia_chi, sdt)
            self.user_dao.tao(user)
        except Exception as e:
            print(e)

    def sua(self, user_id: int, ten, dia_chi, sdt):
        try:
            user = self.user_dao.lay_bang_id(user_id)
            if user:
                user.ten = ten or user.ten
                user.dia_chi = dia_chi or user.dia_chi
                user.sdt = sdt or user.sdt
                self.user_dao.sua(user)
        except Exception as e:
            print(e)

    def xoa(self, user_id: int):
        try:
            self.user_dao.xoa(user_id)
        except Exception as e:
            print(e)
