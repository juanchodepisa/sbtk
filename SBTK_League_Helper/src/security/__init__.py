valid_charset = '-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def check_valid_password(pwd):
    try:
        assert len(pwd) >= 10
        for char in pwd:
            assert char in valid_charset
    except AssertionError:
        return False
    else:
        return True