import tokenlib
import secrets

manager = tokenlib.TokenManager(secret=secret_key, timeout=60)


def create_token(id):
    data = {'id': id}
    return manager.make_token(data)
