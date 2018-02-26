class StartProjectError(Exception):
    """
    Error raised when trying to start a project on a device.
    """

    PROJECT_ACTIVE = 'This project is already active.'
    PROJECT_NONEXISTENT = 'This project does not exist'
    PROJECT_FINISHED = 'This project is already completed'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def project_active(cls):
        return cls(cls.PROJECT_ACTIVE)

    @classmethod
    def project_nonexistent(cls):
        return cls(cls.PROJECT_NONEXISTENT)

    @classmethod
    def project_finished(cls):
        return cls(cls.PROJECT_FINISHED)

class QuitProjectError(Exception):
    """
    Error raised when trying to quit a project on a device.
    """

    PROJECT_NOT_ACTIVE = 'This project is not currently active.'
    PROJECT_NONEXISTENT = 'This project does not exist.'
    PROJECT_FINISHED = 'This project is already completed'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def project_not_active(cls):
        return cls(cls.INVALID_CREDENTIALS)

    @classmethod
    def project_nonexistent(cls):
        return cls(cls.PROJECT_NONEXISTENT)

    @classmethod
    def project_finished(cls):
        return cls(cls.PROJECT_FINISHED)

class DeviceClientError(Exception):
    """
    Error raised by client or by server when unable to communicate with client
    """

    DEVICE_UNREACHABLE = 'Device took too long to respond.'
    UNEXPECTED_DISCONNECT = 'Device has unexpectedly disconnected from server'

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def device_unreachable(cls):
        return cls(cls.DEVICE_UNREACHABLE)

    @classmethod
    def device_error(cls, error_message):
        return cls(error_message)

    @classmethod
    def unexpected_disconnect(cls):
        return cls(cls.UNEXPECTED_DISCONNECT)

