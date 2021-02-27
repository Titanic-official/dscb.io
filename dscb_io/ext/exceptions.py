class OAuthError(Exception):
    pass


class Unauthorized(OAuthError):
    pass


class Ratelimited(OAuthError):
    pass
