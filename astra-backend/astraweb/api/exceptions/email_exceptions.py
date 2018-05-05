class ParsingError(Exception):
    """
    Error raised when trying to parse email content for field replacement
    """

    FIELD_DOES_NOT_EXIST    =   'The field {0} does not exist on model {1}.'

    def __init__(self, error):
        super().__init__(error)

    @classmethod
    def field_does_not_exist(cls, model, field):
        return cls(cls.FIELD_DOES_NOT_EXIST.format(field, model))
    


