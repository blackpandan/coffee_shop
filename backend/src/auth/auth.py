import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dfauth.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeshop'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    header = request.headers.get("Authorization")

    if header is None:
        raise AuthError("no header present", 400)

    authorization = header.split(" ")

    if len(authorization) != 2:
        raise AuthError("malformed header", 400)
    if authorization[0].lower() != 'bearer':
        raise AuthError("Token Method Not Bearer ", 400)

    return authorization[1]
    # raise Exception('Not Implemented')


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in
    the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload: dict):
    if "permissions" not in payload:
        raise AuthError("permission not in payload", 400)
    if permission not in payload["permissions"]:
        raise AuthError("not permitted to perform action", 401)


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)

    except jwt.JWTError as e:
        raise AuthError({
            "code": "error decoding token",
            "description": "the token supplied is invalid"
        }, 401)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "token expired",
                "description": "token expired"
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "invalid claims",
                "description":
                    "incorret claims,"
                    "please check the audience and issuer"
            }, 401)

        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "unable to parse authentication token."
            }, 401)

        # _request_ctx_stack.top.current_user = payload

        raise AuthError({
            "code": "invalid_header",
            "description": "unable to find the appropriate key"
        }, 401)
    # raise Exception('Not Implemented')


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and
    check the requested permission
    return the decorator which passes the decoded payload to the
decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
