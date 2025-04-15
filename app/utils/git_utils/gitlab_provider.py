import base64

from app.core.config import Config

import requests
import logging

logger = logging.getLogger(__name__)

class GitLabProvider:
    def __init__(self, token, repo_owner, repo_name, gitlab_base_url=Config.GITLAB_PROVIDER_BASE_URL):
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

class GitLabEnterpriseProvider(GitLabProvider):
    def __init__(self, token, repo_owner, repo_name, enterprise_base_url):
        super().__init__(token, repo_owner, repo_name, gitlab_base_url=enterprise_base_url)

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