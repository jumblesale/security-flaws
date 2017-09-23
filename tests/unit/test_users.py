import security_flaws.user as user


def test_encryption():
    """
    my terminal tells me: 
        MD5 ("charles t dog") = 0ad0df198d9e465e937cd67f4599ba7e 
    """
    assert user.encrypt_secret('charles t dog') == '0ad0df198d9e465e937cd67f4599ba7e'
