class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class User(LoggingMixin):
    def __init__(self, name):
        self.name = name

    def login(self):
        message = f"{self.name} увійшов у систему"
        print(message)
        self.log(message)


if __name__ == "__main__":
    user = User("Олександр")
    user.login()
