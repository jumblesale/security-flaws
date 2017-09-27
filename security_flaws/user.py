import hashlib


class User:
    required_fields = ['username', 'secret']

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
    validate and create a User object
    :param username: the name of the user
    :param plaintext_secret: the plaintext version of the user's secret
    :return: a User object representing that user with their secret encrypted
    """
    return User(username, encrypt_secret(plaintext_secret))


def create_user_from_dict(d: dict) -> User:
    """
    validate and create a User object from a dictionary of values
    :param d: a dict containing all the needed fields
    :return: a User object if the dict is valid
    """
    errors = []
    for field in User.required_fields:
        if field not in d.keys():
            errors.append('{} was not provided'.format(field))
    if errors:
        raise ValueError(*errors)
    return create_user(d['username'], d['secret'])
