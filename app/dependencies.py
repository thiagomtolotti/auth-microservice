from fastapi import Depends

from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService

users_repo = InMemoryUsersRepository()
users_service = UsersService(users_repo)


def get_users_repo():
    return users_repo


def get_users_service(repo: InMemoryUsersRepository = Depends(get_users_repo)):
    return UsersService(repo)
