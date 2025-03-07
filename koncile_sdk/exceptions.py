class APIError(Exception):
    """Base exception for API errors"""

    pass


# ##################################
# Authentication & Validation Errors
# ##################################
class AuthenticationError(APIError):
    """Raised when authentication fails"""

    pass


class ValidationError(APIError):
    """Raised when credentials validation fails"""

    pass


# ##################################
# Limit Exceeded Errors
# ##################################
class FreeTierLimitReached(APIError):
    """Raised when the user exceeds the free amount of extractions"""

    pass


class UploadLimitReached(APIError):
    """Raised when the user exceeds the account limit on file uploads"""

    pass


# ##################################
# Restriction Errors
# ##################################
class RestrictedFileType(APIError):
    """Raised when an unsupported file type is being uploaded"""

    pass


class RestrictedFieldType(APIError):
    """Raised when an unsupported field type is being used"""

    pass


class RestrictedInstructionType(APIError):
    """Raised when an unsupported instruction type is being used"""

    pass


# ##################################
# Not Found Errors
# ##################################
class ObjectNotFound(APIError):
    """Raised when some object is not found during enpoint execution"""

    pass


class FolderNotFound(ObjectNotFound):
    """Raised when folder is not found during enpoint execution"""

    pass


class TemplateNotFound(ObjectNotFound):
    """Raised when template is not found during enpoint execution"""

    pass


class FieldNotFound(ObjectNotFound):
    """Raised when field is not found during enpoint execution"""

    pass


class InstructionNotFound(ObjectNotFound):
    """Raised when instruction is not found during enpoint execution"""

    pass


class TaskNotFound(ObjectNotFound):
    """Raised when task is not found during enpoint execution"""

    pass
