from enum import Enum


class AlertMessages(str, Enum):
    PROJECT_EMPTY = "Project name cannot be empty"
    PROJECT_ID_TOO_LONG = "Project ID is invalid: it is characters long while the maximum length is 225. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)."
    PROJECT_ID_STARTS_WITH_DIGIT = "Project ID is invalid: starts with non-letter character '1'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)."
    PROJECT_ID_CONTAINS_SPACE = "Project ID is invalid: contains unsupported character ' '. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)"
    PROJECT_ID_CONTAINS_DASH = "Project ID is invalid: contains unsupported character '-'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)."
    PROJECT_ID_CONTAINS_DOT = "Project ID is invalid: contains unsupported character '.'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)."
    PROJECT_ID_CONTAINS_AT = "Project ID is invalid: contains unsupported character '@'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)."
    PROJECT_WITH_NAME_ALREADY_EXISTS = "A project with this name already exists"
    PROJECT_WITH_ID_ALREADY_EXISTS = "Project is already used by another project"
    USERNAME_TOO_LONG = "size limit: 191 table: USERS column: USERNAME"
    USERNAME_IS_EMPTY = "Username must not be empty when creating user."