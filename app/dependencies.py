from fastapi import Depends

from .repositories.postgresql import PostgreSQLRepository
from .repositories.types import UsersRepository

from .services import NotificationLogger
from .services.users import UsersService
from .utils.types import AuthNotificationHandler


notification_logger = NotificationLogger()
users_repo = PostgreSQLRepository()
users_service = UsersService(users_repo, notification_logger)


def get_users_repo():
    return users_repo


def get_notification_handler() -> AuthNotificationHandler:
    return NotificationLogger()


def get_users_service(
    repo: UsersRepository = Depends(get_users_repo),
    notification_handler: NotificationLogger = Depends(get_notification_handler),
):
    return UsersService(repo, notification_handler)
