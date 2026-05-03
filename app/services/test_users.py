from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService
from app.utils.types import CreateUserHandlerDTO


def test_create_success():
    service = UsersService(repository=InMemoryUsersRepository())

    service.create(CreateUserHandlerDTO(email="test@example.com", password="@aa123456"))

    assert service.repository.find_by_email("test@example.com") is not None
