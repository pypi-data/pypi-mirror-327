class CLIFlaskavelException(Exception):
    """
    Custom exception raised when there is an issue with dumping the Flaskavel data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIFlaskavelException with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"CLIFlaskavelException: {self.response}"

class CLIFlaskavelValueError(Exception):
    """
    Custom exception raised when there is an issue with dumping the Flaskavel data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIFlaskavelValueError with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"CLIFlaskavelValueError: {self.response}"

class CLIFlaskavelScheduleException(Exception):
    """
    Custom exception raised when there is an issue with dumping the Flaskavel data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIFlaskavelValueError with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"CLIFlaskavelValueError: {self.response}"