from fastapi import status
from app.exceptions import BaseHTTPException


class GitUrlNotValid(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Github URL is not valid.'
    error_code = 'GITHUB_URL_NOT_VALID'

class GitUsernameNotValid(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'The url username is not the same as the username.'
    error_code = 'GITHUB_USERNAME_NOT_VALID'

class GitWrapperException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = '{error}'
    error_code = 'GITHUB_WRAPPER_ERROR'

class GitTokenNotValid(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'The Github token is not valid.'
    error_code = 'GITHUB_TOKEN_NOT_VALID'

class GitCreateBranchException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = '{error}'
    error_code = 'GIT_CREATE_BRANCH_ERROR'

class RepoDoesNotExistException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Repository does not exist.'
    error_code = 'REPO_DOES_NOT_EXIST'

class GitRepoMismatchException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'The url repo name is not the same as the repo name.'
    error_code = 'GIT_REPO_MISMATCH'

class GitUsernameNotAuthorized(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Username does not match repository owner or is not authorized.'
    error_code = 'GITHUB_USERNAME_NOT_AUTHORIZED'