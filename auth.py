class Auth:
    def __init__(self):
        self.users = {}  # In-memory store for simplicity

    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        return True

    def authenticate(self, username, password):
        return self.users.get(username) == password
