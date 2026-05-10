from fastapi import Depends

from app.repositories.users import InMemoryUsersRepository


def get_users_repo():
    return InMemoryUsersRepository()


def get_users_service(repo: InMemoryUsersRepository = Depends(get_users_repo)):
    from app.services.users import UsersService

    return UsersService(repo)
