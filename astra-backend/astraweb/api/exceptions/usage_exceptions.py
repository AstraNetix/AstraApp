class DataException(Exception):
    """
    Error raised when working with data i/o.
    """

    ADDING_COARSE  = {'coarse_data': ['You cannot directly add coarse level data.']}

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def adding_coarse(cls):
        return cls(cls.ADDING_COARSE)