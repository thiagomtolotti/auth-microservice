from app.repositories.users import UsersRepository


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def create(self):
        print("Creating User")
        self.repository.create()
