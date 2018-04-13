class CreationError(Exception):
    """
    Error raised when unable to create user 
    """

    UNMATCHING_PASSWORDS    =   {'confirm_password':    ['Passwords do not match.']                 }
    USER_EXISTS             =   {'email':               ['This email is already in use.']           }
    OLD_PASSWORD_REQUIRED   =   {'old_password':        ['Former password confirmation required.']  }

    def __init__(self, errors):
        super().__init__(next(iter(errors)))
        self.errors = errors

    @classmethod
    def unmatching_passwords(cls):
        return cls(cls.UNMATCHING_PASSWORDS)

    @classmethod
    def user_exists(cls):
        return cls(cls.USER_EXISTS)

    @classmethod
    def old_password_required(cls):
        return cls(cls.OLD_PASSWORD_REQUIRED)


class AuthenticationError(LookupError):
    """
    Error raised when a user fails to authenticate a User.
    """

    USER_DOES_NOT_EXIST = {'email':     ['There is no account associated with this email.'] }
    INVALID_CREDENTIALS = {'general':   ['The credentials you provided are invalid.']       }
    MISSING_FIELDS      = {'general':   ['One or more of the fields is blank.']             }
    INACTIVE_ACCOUNT    = {'general':   ['Your account is inactive.']                       }

    def __init__(self, errors):
        super().__init__(next(iter(errors)))
        self.errors = errors

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

    MISSING_FIELDS      = {'general':       ['One or more fields is blank.']                                            }
    PASSWORD_TOO_SHORT  = {'new_password':  ['New password must be at least 6 characters long.']                        }
    INVALID_CHARACTERS  = {'new_password':  ['New password can only consist of alphanumeric characters and symbols.']   }
    INCORRECT_PASSWORD  = {'password':      ['Incorrect password.']                                                     }

    def __init__(self, errors):
        super().__init__(next(iter(errors)))
        self.errors = errors

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

    INCOMPLETE_ICO  = {'general':   ['User is not registered for token sale.']  }
    INACTIVE        = {'general':   ['User is not active']                      }
    NOT_VERIFIED    = {'email':     ['User is not email validated yet']         }

    def __init__(self, errors):
        super().__init__(next(iter(errors)))
        self.errors = errors

    @classmethod
    def incomplete_ICO(cls):
        return cls(cls.INCOMPLETE_ICO)

    @classmethod
    def inactive(cls):
        return cls(cls.INACTIVE)

    @classmethod
    def not_verified(cls):
        return cls(cls.NOT_VERIFIED)

class ReferralError(Exception):
    """
    Error raised when attributing user to a referral.
    """
    
    REFERRAL_CODE_ERROR = {'referral_code': ['Referral code does not belong to a user']         }
    REFERRAL_MAX_ERROR  = {'referral_code': ['This user has used up all of their referrals']    }
    REFERRAL_SET        = {'referral_code': ['You have already set your referral']              }
    SELF_REFERRAL       = {'referral_code': ['You cannot refer yourself']                       }
    CIRCULAR_REFERRAL   = {'referral_code': ['You cannot refer someone who referred you']       }

    def __init__(self, errors):
        super().__init__(next(iter(errors)))
        self.errors = errors

    @classmethod
    def referral_code_error(cls):
        return cls(cls.REFERRAL_CODE_ERROR)

    @classmethod
    def referral_max_error(cls):
        return cls(cls.REFERRAL_MAX_ERROR)

    @classmethod
    def referral_set(cls):
        return cls(cls.REFERRAL_SET)
    
    @classmethod
    def self_referral(cls):
        return cls(cls.SELF_REFERRAL)
    
    @classmethod
    def circular_referral(cls):
        return cls(cls.CIRCULAR_REFERRAL)