import abc
import math
import typing
from uuid import uuid4

import inject
from sqlalchemy import func, Column, or_, and_, distinct, update

from sqlalchemy.orm import Session, Query

from service_common.model import CoreModel
from service_common.adapter.redis_adapter import BaseBackend
from service_common.context_vars import get_current_user_uuid


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, model: CoreModel):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, uuid) -> typing.Union[CoreModel, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, data: dict, where: dict):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model: CoreModel = None
    search_fields: typing.List[Column] = None

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def add(self, model: typing.Union[CoreModel, dict]):
        if isinstance(model, dict):
            model = self.model(**model)
            model.created_by = get_current_user_uuid()
            model.modified_by = model.created_by
        if not model.public_id:
            model.public_id = str(uuid4())
        self.session.add(model)
        return model

    def get(self, id_: int, is_deleted: bool = False) -> typing.Union[CoreModel, None]:
        """
        Returns the record matching with given id_
        :param id_: int:
        :param is_deleted: bool:
        :return:
        """
        return self.session.query(self.model).filter_by(id=id_, is_deleted=is_deleted).first()

    def find_by_public_id(self, public_id: str, is_deleted: bool = False) -> typing.Union[CoreModel, None]:
        """
        Return the record for given Public ID
        :param public_id: str:
        :param is_deleted: bool:
        :return:
        """
        return self.session.query(self.model).filter_by(public_id=public_id).first()

    def update(self, values: dict, where: tuple):
        """
        Update the dictionary values with given where clause in the form of tuples
        :param values:
        :param where:
        :return:
        """
        if not values:
            values = {}
        values['modified_by'] = get_current_user_uuid()
        self.session.query(self.model).filter(*where).update(values)

    def update_by(self, values: dict, where: dict):
        """
        Update the dictionary values with given where clause in the form of dictionary
        :param values:
        :param where:
        :return:
        """
        if not values:
            values = {}
        values['modified_by'] = get_current_user_uuid()
        self.session.query(self.model).filter_by(**where).update(values)

    def update_multiple(self, values: dict, where: tuple):
        """
        Update multiple records
        :param values:
        :param where:
        :return:
        """
        stmt = update(self.model).where(*where).values(**values)
        self.session.execute(stmt)

    def get_single(self, **kwargs) -> typing.Union[CoreModel, None]:
        """
        Return the Single record matching with given criteria
        :param kwargs:
        :return:
        """
        return self.session.query(self.model).filter_by(**kwargs).first()

    def filter(self, order_by: str = None, order: str = None, **kwargs):
        """
        Filter records with given keyword arguments
        :param order_by:
        :param order:
        :param kwargs:
        :return:
        """
        if kwargs:
            kwargs['is_deleted'] = kwargs.get('is_deleted', False)
        else:
            kwargs = {'is_deleted': False}
        if kwargs.get('is_deleted', False) is None:
            # If `is_deleted` set to `None` then ignore the `is_deleted` filter
            del kwargs['is_deleted']
        query = self.session.query(self.model)
        if kwargs:
            query = query.filter_by(**kwargs)

        if order_by:
            # Apply orderby clause
            order = order or 'desc'
            return query.order_by(getattr(getattr(self.model, order_by), order.lower())()).all()
        else:
            return query.all()

    def refresh(self, instance_):
        """
        Refresh the Instance
        :param instance_:
        :return:
        """
        self.session.refresh(instance_)

    def delete(self, record: typing.Union[CoreModel, str, int]):
        """
        Mark the record as deleted
        :param record:
        :return:
        """
        if isinstance(record, CoreModel):
            self.session.query(self.model).filter(self.model.id == record.id).update({'is_deleted': True})
        elif type(record) == int:
            self.session.query(self.model).filter(self.model.id == record).update({'is_deleted': True})
        elif type(record) == str:
            self.session.query(self.model).filter(self.model.public_id == record).update({'is_deleted': True})

    def hard_delete(self, **kwargs):
        if not kwargs:
            raise Exception(f"Cannot delete all record from {self.model.__tablename__}")
        self.session.query(self.model).filter_by(**kwargs).delete()

    def get_paginated_result(self, search: str = None, order_by: str = 'created_at', order: str = 'DESC',
                             page: int = 1, page_size: int = 10, **kwargs):
        """
        Paginate through the results
        :param search:
        :param order_by:
        :param order:
        :param page:
        :param page_size:
        :return:
        """
        query, total_count = self.get_list_filter_query(search=search, order_by=order_by, order=order, **kwargs)

        offset_value = page * page_size - page_size
        result = query.offset(offset_value).limit(page_size).all()
        total_pages = math.ceil(total_count/page_size)
        return {
            "page": page,
            "page_size": page_size,
            "data": result,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next_page": bool(page < total_pages),
            "has_prev_page": bool(page > 1)
        }

    def get_list_filter_query(self, search: str = None,
                              order_by: str = 'created_at', order: str = 'desc',
                              **kwargs):
        """
        Filter records with given keyword arguments
        :param search: str:
        :param order_by: str:
        :param order: str:
        :param kwargs:
        :return:
        """
        if kwargs:
            kwargs['is_deleted'] = kwargs.get('is_deleted', False)
        else:
            kwargs = {'is_deleted': False}
        if kwargs.get('is_deleted', False) is None:
            # If `is_deleted` set to `None` then ignore the `is_deleted` filter
            del kwargs['is_deleted']
        query = self.session.query(self.model)
        # Use separate Count query for performance
        count_query = self.session.query(func.count(distinct(self.model.id)))
        if kwargs:
            query = query.filter_by(**kwargs)
            count_query = count_query.filter_by(**kwargs)

        if search:
            # Apply search filter
            if len(self.search_fields) > 1:
                # Search given value in all columns
                query = query.filter(or_(*[field_.like(f"%{search}%") for field_ in self.search_fields]))
                count_query = count_query.filter(or_(*[field_.like(f"%{search}%") for field_ in self.search_fields]))
            elif len(self.search_fields) == 1:
                query = query.filter(self.search_fields[0].like(f"%{search}%"))
                count_query = count_query.filter(self.search_fields[0].like(f"%{search}%"))

        if order_by:
            # Build the order by clause
            return query.order_by(getattr(getattr(self.model, order_by), order.lower())()), count_query.scalar()
        else:
            return query, count_query.scalar()

    def count_records(self, **kwargs) -> int:
        """
        Returns the count of records with given filter of current object
        :param kwargs:
        :return:
        """
        query = self.session.query(func.count(distinct(self.model.id)))
        if kwargs:
            query = query.filter_by(**kwargs)
        return query.scalar()

    def count_total_records(self, model, **kwargs) -> int:
        """
        Returns the count of records with given filter of current object
        :param model:
        :param kwargs:
        :return:
        """
        query = self.session.query(func.count(distinct(model.id)))
        if kwargs:
            query = query.filter_by(**kwargs)
        return query.scalar()


class RedisRepository(AbstractRepository):

    @inject.autoparams('backend')
    def __init__(self, backend: BaseBackend):
        self.backend: BaseBackend = backend

    def _add(self, key: str, data: typing.Union[dict, list, str], **kwargs):
        if type(data) == dict:
            self.backend.set_dict(key, data, **kwargs)
        elif type(data) == list:
            self.backend.set_list(key, data, **kwargs)
        elif type(data) == str:
            self.backend.set_str(key, data, **kwargs)
        else:
            raise NotImplemented(f"Unable to save the {type(data)!r}")

    def add(self, model: CoreModel):
        self._add(model.public_id, {c: getattr(self, c) for c in model.__table__.columns})

    def get(self, uuid: str) -> typing.Union[dict, str, list, None]:
        return self.backend.get_dict(uuid)

    def update(self, data: dict, where: dict):
        raise NotImplemented("Cannot implement update record for RedisRepository")


class UserBaseSqlAlchemyRepository(SqlAlchemyRepository):

    def find_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()

    def find_by_mobile(self, mobile):
        return self.session.query(self.model).filter_by(mobile=mobile).first()

    def check_user_exists(self, email: str = None, mobile: str = None) -> bool:
        query = self.session.query(func.count(self.model.id))
        if mobile and email:
            query = query.filter(or_(self.model.mobile == mobile, self.model.email == email))
        else:
            if mobile:
                query = query.filter_by(mobile=mobile)
            if email:
                query = query.filter_by(email=email)
        rec = query.scalar()
        return bool(rec)
