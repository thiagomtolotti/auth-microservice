import datetime

from app.utils.types import AuthNotificationHandler


class NotificationLogger(AuthNotificationHandler):
    def on_forgot_password(self, email: str, token: str, expires_at: int):
        print(
            f"Forgot password token for user {email}: {token} (expires at {datetime.datetime.fromtimestamp(expires_at)})"
        )
