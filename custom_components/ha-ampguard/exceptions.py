"""Custom Exceptions."""


class AmpGuardError(Exception):
    """Base exception."""


class CannotConnect(AmpGuardError):
    """Error to indicate we cannot connect."""


class InvalidAuth(AmpGuardError):
    """Error to indicate there is invalid auth."""
