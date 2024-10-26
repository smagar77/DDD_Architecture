import typing
from logging import getLogger
from pydantic import BaseModel, Field

from service_common import enums
from service_common.utils import get_password_hash, verify_password

T = typing.TypeVar('T')
logger = getLogger(__name__)


class BaseDomain(BaseModel):
    _protected_fields: typing.List[str] = Field(default_factory=list, exclude=True)
    _special_fields: typing.List[str] = Field(default_factory=list, exclude=True)

    public_id: typing.Optional[str] = None

    @staticmethod
    def _check_field(obj_: typing.Any, field_: str):
        """
        Utility function to check if given field exists in the other object/dict

        :param obj_:
        :param field_:
        :return:
        """
        try:
            if isinstance(obj_, BaseModel):
                return field_ in obj_.__fields__
            return field_ in obj_
        except TypeError:
            return hasattr(obj_, field_)

    @staticmethod
    def _get_value_(obj: typing.Any, field_: str, default: typing.Any = None):
        """
        Utility function to retrieve the value of any object/dict

        :param obj:
        :param field_:
        :param default:
        :return:
        """
        try:
            return obj[field_]
        except TypeError:
            return getattr(obj, field_, default)

    def _copy_value(self, name: str, o_val: typing.Any, override_strategy: str = None):
        """
        This function is meant to override if you need different approach to copy the value or need some more processing

        :param name: str: Name of the field
        :param o_val: typing.Any: Value of the field in other object
        :param override_strategy: SELF_NULL | OTHER_NOT_NULL
                    SELF_NULL: If self.{field} == None then only copy value from other_obj.{field}
                    OTHER_NOT_NULL: If other_obj.{field} != None then only copy other_obj.{field}
        :return:
        """
        value = getattr(self, name)
        if override_strategy == 'SELF_NULL' and not value:
            # Copy value from target only if current value is None
            setattr(self, name, o_val)
        elif override_strategy == 'OTHER_NOT_NULL' and o_val:
            # Copy the value from target only when target value is not None
            setattr(self, name, o_val)
        elif not override_strategy:
            # Always copy the value from Target
            setattr(self, name, o_val)

    def copy_(self, other_obj: typing.Any, override_strategy: str = None):
        """
        Copy the values from the other object to the self by given strategy

        Do not override unless and until it is absolutely necessary.
        To change the copy behaviour please override `_copy_value` method

        :param other_obj:
        :param override_strategy: SELF_NULL | OTHER_NOT_NULL
                    SELF_NULL: If self.{field} == None then only copy value from other_obj.{field}
                    OTHER_NOT_NULL: If other_obj.{field} != None then only copy other_obj.{field}
        :return:
        """
        for name, field_ in self.__fields__.items():
            # Take care of the defined aliases while performing the copy
            alias = field_.alias
            if self._check_field(other_obj, alias):
                o_val = self._get_value_(other_obj, alias, None)
                self._copy_value(name, o_val, override_strategy=override_strategy)

    def __add__(self, other: typing.Union[dict, T]) -> T:
        """
        Combines the details
        If First object do not have the value then only we will consider the value of other object
        We assume that the current object is populated from Database data, and we are overriding with request data

        :param other:
        :return:
        """
        if type(other) == dict:
            other = self.__class__(**other)
        if not issubclass(type(other), BaseDomain):
            # Only same types can be added
            raise NotImplementedError(f"Can not add {self.__class__.__name__} type in {type(other)}")

        for field_, value in self:
            o_val = getattr(other, field_, None)
            # Set the new values, override with other values always
            self._add(field_, o_val)
        return self

    def _add(self, field_: str, o_val: typing.Any):
        """
        Define how to replace the source value with other value
        This function is meant to override, if we don't want the default way
        :param field_: Field name
        :param o_val: Value of field in other object
        :return:
        """
        value = getattr(self, field_)
        try:
            if field_ in self._protected_fields and value:
                # Do not override protected fields
                return
        except TypeError as e:
            # Ignoring the exception if self._protected_fields is not declared
            logger.warning(f"{type(self)} is not having '_protected_fields' attribute Exception: {e}", exc_info=True)

        try:
            is_special_field = field_ in self._special_fields
        except TypeError as e:
            is_special_field = False
            # Ignoring the exception if self._protected_fields is not declared
            logger.warning(f"{type(self)} is not having '_special_fields' attribute Exception: {e}", exc_info=True)

        if o_val:
            if isinstance(o_val, BaseDomain) and isinstance(value, BaseDomain):
                value = value + o_val
                # Merge the source value with the other value and update the source value
                setattr(self, field_, value)
            elif is_special_field:
                if isinstance(value, list):
                    # Merge the two lists
                    value = list(set(value).union(set(o_val)))
                # Merge the source value with the other value and update the source value
                setattr(self, field_, value)
            else:
                # By default, always replace the source value with other value
                setattr(self, field_, o_val)


class User(BaseDomain):
    email: str = Field(default=None)
    mobile: str = Field(default=None)
    public_id: typing.Optional[str] = Field(default=None)
    user_type: enums.UserTypeEnum = Field(default=enums.UserTypeEnum.field_agent)
    first_name: str = Field(default=None)
    middle_name: typing.Optional[str] = Field(default=None)
    last_name: typing.Optional[str] = Field(default=None)

    class Config:
        orm_mode = True


class UserDb(User):
    password_hash: str = None

    def set_pass_hash(self, password):
        self.password_hash = get_password_hash(password)

    def verify_password(self, password):
        return verify_password(password, self.password_hash)

    class Config:
        orm_mode = True


class PaginatedParameters(BaseModel):
    page: int = 1
    page_size: int = 100
    order_by: str = 'created_at'
    order: enums.OrderEnum = enums.OrderEnum.desc


class SearchPaginatedParameters(PaginatedParameters):
    search: str = None
    page: int = 1
    page_size: int = 100
    order_by: str = 'created_at'
    order: enums.OrderEnum = enums.OrderEnum.desc

    def load_order_by_parameters(self, order: enums.OrderByEnum = enums.OrderByEnum.recently_added):
        if order == enums.OrderByEnum.recently_added_rev:
            self.order = enums.OrderEnum(enums.OrderEnum.asc)
        elif order == enums.OrderByEnum.recently_added:
            self.order_by = 'modified_at'
        elif order == enums.OrderByEnum.recently_updated_rev:
            self.order_by = 'modified_at'
            self.order = enums.OrderEnum(enums.OrderEnum.asc)


class UserSearchPaginatedParameters(SearchPaginatedParameters):
    user_type: typing.Optional[enums.UserTypeEnum] = None
