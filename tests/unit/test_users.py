import security_flaws.user as user
from hamcrest import assert_that, equal_to


def test_encryption():
    """
    my terminal tells me: 
        MD5 ("charles t dog") = 0ad0df198d9e465e937cd67f4599ba7e 
    """
    assert_that(
        user.encrypt_secret('charles t dog'),
        equal_to('0ad0df198d9e465e937cd67f4599ba7e')
    )


def test_secret_validation():
    # too short
    assert_that(user.validate_secret(''), equal_to(False))
    # too long
    assert_that(user.validate_secret('1234567890abcdefx'), equal_to(False))
    # upper case
    assert_that(user.validate_secret('A'), equal_to(False))
    # special character
    assert_that(user.validate_secret('/'), equal_to(False))
    # good
    assert_that(user.validate_secret('a long secret'), equal_to(True))
