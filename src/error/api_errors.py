class ResourceAlreadyExistsError(Exception):
    """Exception raised when a resource already exists."""

    def __init__(self, message="Resource already exists."):
        self.message = message
        super().__init__(self.message)


class ResourceNotFound(Exception):
    """Exception raised when a resource already exists."""

    def __init__(self, message="Resource not found."):
        self.message = message
        super().__init__(self.message)
