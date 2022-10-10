class ParseError(Exception):
    """Raise when a specific key was not fetched with passed format."""
    def __init__(self, message, reason, *args):
        self.message = message
        self.reason = reason
        super().__init__(message, reason, *args)