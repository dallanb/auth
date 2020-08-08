import re
from uuid import UUID
from sqlalchemy.orm.base import object_mapper
from sqlalchemy.orm.exc import UnmappedInstanceError
from iso4217 import Currency


def is_mapped(v):
    if v is None:
        return v
    try:
        object_mapper(v)
    except UnmappedInstanceError:
        return None
    return v


def is_id(v):
    if v is None:
        return v
    return is_int(v, 1)


def is_string(v, min_length=0, max_length=2000):
    if v is None:
        return v
    if not isinstance(v, str):
        return None
    if len(v) < min_length or len(v) > max_length:
        return None
    return v


def is_text(v, min_length=0, max_length=4000):
    if v is None:
        return v
    if not isinstance(v, str):
        return None
    if len(v) < min_length or len(v) > max_length:
        return None
    return v


def is_int(v, min_count=0, max_count=9999999999):
    if v is None:
        return v
    if isinstance(v, str) and v.isdigit():
        v = int(v)
    if not isinstance(v, int):
        return None
    if min_count is not None and v < min_count:
        return None
    if max_count is not None and v > max_count:
        return None
    return v


def is_email(v):
    if v is None:
        return v
    if not re.search('[^@]+@[^@]+\.[^@]+', v):
        return None
    return v


def is_enum(v, enum_class):
    if v is None:
        return v
    if v in enum_class.__members__ is False:
        return None
    return enum_class[v]


def is_uuid(v):
    if v is None:
        return v
    try:
        if isinstance(v, UUID):
            v = str(v)
        uuid_v = UUID(v)
    except ValueError:
        return None
    if not str(uuid_v) == v:
        return None
    return uuid_v


def is_list(v):
    if v is None:
        return v
    if not isinstance(v, list):
        return None
    return v


def is_dict(v):
    if v is None:
        return v
    if not isinstance(v, dict):
        return None
    return v


def is_hash(v):
    if v is None:
        return v
    if not is_int(v, min_count=None, max_count=None):
        return None
    return v


def is_currency(v):
    if v is None:
        return v
    try:
        Currency(v)
    except ValueError:
        return None
    return v


def is_float(v):
    if v is None:
        return v
    if not isinstance(v, float):
        return None
    return v


def is_num(v):
    if v is None:
        return v
    if not is_float(v) and not is_int(v):
        return None
    return v
