import pytest

from .fixtures import MockNotificationHandler


@pytest.fixture()
def client():
    from starlette.testclient import TestClient

    from app.main import app
    from app.dependencies import get_users_repo
    from app.repositories.users import InMemoryUsersRepository

    fresh_repo = InMemoryUsersRepository()
    app.dependency_overrides[get_users_repo] = lambda: fresh_repo

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture()
def notification_handler():
    from app.main import app
    from app.dependencies import get_notification_handler

    notification_handler = MockNotificationHandler()
    app.dependency_overrides[get_notification_handler] = lambda: notification_handler

    yield notification_handler
