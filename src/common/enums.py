import enum


class RoleEnum(enum.Enum):
    member = 1
    admin = 2
    root = 3


class StatusEnum(enum.Enum):
    pending = 1
    active = 2
    inactive = 3
    blocked = 4
    deleted = 5
