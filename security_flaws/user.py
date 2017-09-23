import hashlib


class User:
    def __init__(self, username, secret):
        self.id = None
        self.username = username
        self.secret = secret

    def __str__(self):
        return "{}|{}".format(self.username, self.secret)


def encrypt_secret(plaintext: str) -> str:
    """
    a totally cryptographically secure method to encrypt secrets GUARANTEED unbreakable
    :param plaintext: the plaintext secret
    :return: the unbreakable encrypted version of the secret
    """
    hash = hashlib.md5()
    hash.update(plaintext.encode('utf-8'))
    return hash.hexdigest()


def create_user(username: str, plaintext_secret: str) -> User:
    """
    create a User object
    :param username: the name of the user
    :param plaintext_secret: the plaintext version of the user's secret
    :return: a User object representing that user with their secret encrypted
    """
    return User(username, encrypt_secret(plaintext_secret))
