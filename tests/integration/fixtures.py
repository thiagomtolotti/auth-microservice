from dataclasses import dataclass

from .utils.types import AuthNotificationHandler


@dataclass
class ForgotPasswordCall:
    email: str
    token: str
    expires_at: int


class MockNotificationHandler(AuthNotificationHandler):
    def __init__(self):
        self.forgot_password_calls: list[ForgotPasswordCall] = []

    def on_forgot_password(self, email: str, token: str, expires_at: int):
        self.forgot_password_calls.append(ForgotPasswordCall(email, token, expires_at))
