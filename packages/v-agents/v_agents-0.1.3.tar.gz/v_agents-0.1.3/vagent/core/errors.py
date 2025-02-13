class ProgramError(Exception):
    """Base exception class for program-related errors"""

    pass


class FunctionCallError(ProgramError):
    """Raised when there are issues with function calls"""

    pass


class BadProgramError(ProgramError):
    pass


class InvalidResponseError(ProgramError):
    """Raised when LLM response is invalid"""

    pass


class LLMException(Exception):
    """Base exception class for LLM-related errors"""

    pass


class APIConnectionError(LLMException):
    """Raised when there are issues connecting to the API"""

    pass


class InvalidConfigurationError(LLMException):
    """Raised when required configuration is missing or invalid"""

    pass
