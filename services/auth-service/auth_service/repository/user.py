import typing
from sqlalchemy import func, or_
from service_common.repository import SqlAlchemyRepository
from auth_service.model.user import UserModel
from auth_service import model
from service_common.enums import UserTypeEnum


class UserSqlAlchemyRepository(SqlAlchemyRepository):
    model: UserModel = UserModel
    search_fields = [UserModel.first_name, UserModel.middle_name, UserModel.last_name]

    def find_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()

    def find_by_mobile(self, mobile):
        return self.session.query(self.model).filter_by(mobile=mobile).first()

    def get_users_count_by_type(self, created_by: str = None):
        """

        :param created_by:
        :return:
        """
        query = self.session.query(self.model.user_type, func.count(self.model.id))
        if created_by:
            query = query.filter(
                self.model.created_by == created_by
            )
        return query.group_by(self.model.user_type).all()

    def check_user_exists(self, email: str = None, mobile: str = None, public_id: str = None) -> bool:
        query = self.session.query(func.count(self.model.id))
        if mobile and email:
            query = query.filter(or_(self.model.mobile == mobile, self.model.email == email))
        else:
            if mobile:
                query = query.filter_by(mobile=mobile)
            if email:
                query = query.filter_by(email=email)
        if public_id:
            query = query.filter(self.model.public_id != public_id)
        rec = query.scalar()
        return bool(rec)

    @staticmethod
    def get_user_map(user: UserModel):
        map_ = []
        if user.user_type == UserTypeEnum.farmer:
            map_.append({"user_type": UserTypeEnum.farmer, "public_id": user.public_id})

        return map_
