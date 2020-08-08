import enum


class UserRoleEnum(enum.Enum):
    member = 1
    admin = 2
    root = 3


class UserStatusEnum(enum.Enum):
    pending = 1
    active = 2
    inactive = 3
    blocked = 4
    deleted = 5


class TokenStatusEnum(enum.Enum):
    active = 1
    inactive = 2
