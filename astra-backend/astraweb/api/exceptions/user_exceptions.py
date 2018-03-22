class CreationError(Exception):
    """
    Error raised when unable to create user 
    """

    UNMATCHING_PASSWORDS = 'Passwords do not match.'
    USER_EXISTS = 'This email is already in use.'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def unmatching_passwords(cls):
        return cls(cls.UNMATCHING_PASSWORDS)

    @classmethod
    def user_exists(cls):
        return cls(cls.USER_EXISTS)

class AuthenticationError(LookupError):
    """
    Error raised when a user fails to authenticate a User.
    """

    USER_DOES_NOT_EXIST = 'There is no account associated with this email.'
    INVALID_CREDENTIALS = 'The credentials you provided are invalid.'
    MISSING_FIELDS = 'One or more of the fields is blank.'
    INACTIVE_ACCOUNT = 'Your account is inactive.'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def user_does_not_exist(cls):
        return cls(cls.USER_DOES_NOT_EXIST)

    @classmethod
    def invalid_credentials(cls):
        return cls(cls.INVALID_CREDENTIALS)

    @classmethod
    def missing_fields(cls):
        return cls(cls.MISSING_FIELDS)

    @classmethod
    def inactive_account(cls):
        return cls(cls.INACTIVE_ACCOUNT)


class PasswordChangeError(Exception):
    """
    Error raised when a user fails to change their password.
    """

    MISSING_FIELDS = 'One or more fields is blank.'
    PASSWORD_TOO_SHORT = 'New password must be at least 6 characters long.'
    INVALID_CHARACTERS = 'New password can only consist of alphanumeric characters and symbols.'
    INCORRECT_PASSWORD = 'Incorrect password.'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def missing_fields(cls):
        return cls(cls.MISSING_FIELDS)

    @classmethod
    def password_too_short(cls):
        return cls(cls.PASSWORD_TOO_SHORT)

    @classmethod
    def invalid_characters(cls):
        return cls(cls.INVALID_CHARACTERS)

    @classmethod
    def incorrect_password(cls):
        return cls(cls.INCORRECT_PASSWORD)

class TokenICOKYCError(Exception):
    """
    Error raised with user is not valid for token sale
    """

    INCOMPLETE_ICO = 'User is not registered for token sale.'
    INACTIVE = 'User is not active'
    NOT_VERIFIED = 'User is not email validated yet'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def incomplete_ICO(cls):
        return cls(cls.INCOMPLETE_ICO)

    @classmethod
    def inactive(cls):
        return cls(cls.INACTIVE)

    @classmethod
    def not_verified(cls):
        return cls(cls.NOT_VERIFIED)

