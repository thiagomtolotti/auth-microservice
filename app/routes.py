from enum import Enum


class Routes(Enum):
    PING = "/"
    LOGIN = "/login"
    LOGOUT = "/logout"
    REGISTER = "/register"
    DELETE_USER = "/delete"
    REFRESH_TOKEN = "/refresh-token"
    FORGOT_PASSWORD = "/forgot-password"
    RESET_PASSWORD = "/reset-password"
    CHANGE_PASSWORD = "/change-password"
    PROTECTED = "/protected"
