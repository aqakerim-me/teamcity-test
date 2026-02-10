from enum import Enum


class AlertMessages(str, Enum):
    USERNAME_CANNOT_BE_BLANK = "Username cannot be blank"