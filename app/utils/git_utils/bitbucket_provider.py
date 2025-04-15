import base64
import requests
from app.core.config import Config
import logging

logger = logging.getLogger(__name__)

class BitbucketProvider:
    def __init__(self, token, repo_owner, repo_name, bitbucket_base_url=Config.BITBUCKET_PROVIDER_BASE_URL):
        pass

    async def validate_token(self):
        pass

    async def create_branch(self, base_branch, new_branch):
        pass

    async def check_in_code(self, branch_name, file_path, commit_message, content):
        pass

    async def delete_branch(self, branch_name):
        pass

    async def create_initial_commit(self, file_path, commit_message, content, branch_name='main'):
        pass