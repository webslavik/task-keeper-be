from .constants import pwd_context


def get_hashed_password(password):
    return pwd_context.hash(password)
