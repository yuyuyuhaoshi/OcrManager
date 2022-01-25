# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from random import sample

from flask_restless.helpers import strings_to_dates, to_dict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, String, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.schema import Column
from sqlalchemy.types import TEXT, VARCHAR, Boolean, DateTime, Float, Integer

from manager.exceptions import BusinessError, DuplicateNamed, ObjectNotFound

db = SQLAlchemy()

Model = db.Model
session = db.session


def gen_primary_key():
    return str(uuid.uuid4())


def err_func(error):
    raise error


def query_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count


class ModelMixin(object):
    __table_args__ = {"extend_existing": True}

    system_columns = [
        "id",
        "is_deleted",
        "tdate",
        "udate",
    ]
    user_invisible = ["is_deleted"]
    include_relations = []
    custom_relation = ()

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_deleted = Column(Boolean, index=True, default=False)
    tdate = Column(DateTime, default=datetime.now, index=True)
    udate = Column(
        DateTime,
        onupdate=datetime.now,
        default=datetime.now,
        index=True,
    )

    @classmethod
    def get_by_id(
        cls,
        record_id,
        ignore_deleted=True,
        exception=None,
        error_back=lambda: err_func(ObjectNotFound(error="页面丢失啦~是不是写错了呢")),
    ):
        q = cls.query_ignore_deleted() if ignore_deleted else cls.query
        inst = q.filter_by(id=record_id).first()
        if inst is None:
            if exception:
                raise exception
            error_back()
        return inst

    @classmethod
    def query_ignore_deleted(cls):
        return cls.query.filter_by(is_deleted=False)

    def to_dict(
        self, exclude=None, include=None, exclude_relations=None, include_relations=None
    ):

        res: dict = to_dict(
            self,
            deep=0,
            exclude=exclude,
            include=include,
            include_relations=None,
            exclude_relations=None,
        )

        for k in self.user_invisible:
            if k in res:
                res.pop(k)
        return res

    @classmethod
    def drop_exclude_data(cls, data):
        result = {}
        columns = {c.name for c in cls.__table__.columns}
        for key, val in data.items():
            if (
                key in cls.system_columns
                or key in cls.user_invisible
                or key not in columns
            ):
                continue
            result[key] = val
        return result

    def update(self, commit=True, overwrite_json=True, **data):
        """Update specific fields of a record."""
        data = self.drop_exclude_data(data)
        data = strings_to_dates(self.__class__, data)
        for attr, value in data.items():
            column_type = getattr(self.__class__, attr).type
            ori_val = getattr(self, attr)
            if (
                isinstance(column_type, JSON)
                and (not overwrite_json)
                and isinstance(ori_val, dict)
            ):
                value = {**ori_val, **value}
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(
        self, commit=True, duplicated_back=lambda: err_func(BusinessError("数据存在重复"))
    ):
        """Save the record."""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                if duplicated_back and (
                    "duplicate" in err.args[0].lower()
                    or "unique" in err.args[0].lower()
                ):
                    duplicated_back()
                raise
        return self

    def delete(self, commit=True):
        """Soft delete the record from the database."""
        self.is_deleted = True

        return commit and self.save() or self

    @classmethod
    def create(cls, **data):
        """Returns an instance of the model with the specified attributes."""
        data = cls.drop_exclude_data(data)
        data = strings_to_dates(cls, data)
        instance = cls(**data)
        return instance


class Image(ModelMixin, Model):
    __tablename__ = "image"

    user_invisible = ["is_deleted"]

    name = Column(VARCHAR(256), nullable=False)
    url = Column(TEXT, nullable=False, default="")
    content = Column(JSON, nullable=False, default="[]")
