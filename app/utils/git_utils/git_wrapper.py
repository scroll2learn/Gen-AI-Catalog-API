
from app.utils.git_utils.github_provider import GitHubProvider
from app.utils.git_utils.gitlab_provider import GitLabEnterpriseProvider, GitLabProvider


class GitWrapper:
    def __init__(self, token, repo_owner, repo_name, provider_type):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.provider = self._initialize_provider(provider_type)

    def _initialize_provider(self, provider_type):
        if provider_type == 4100:
            return GitHubProvider(self.token, self.repo_owner, self.repo_name)
        elif provider_type == 4101:
            return GitLabEnterpriseProvider(self.token, self.repo_owner, self.repo_name)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")

    async def validate_token(self):
        """Validate the provided token."""
        return await self.provider.validate_token()

    async def create_initial_commit(self, file_path, commit_message, content, branch_name):
        """Create an initial commit."""
        return await self.provider.create_initial_commit(file_path, commit_message, content, branch_name)

    async def create_branch(self, new_branch):
        """Create a new branch."""
        return await self.provider.create_branch(new_branch)

    async def check_in_code(self, branch_name, file_path, commit_message, content):
        """Check in code to a specific branch."""
        return await self.provider.check_in_code(branch_name, file_path, commit_message, content)

    async def delete_branch(self, branch_name):
        """Delete a branch."""
        return await self.provider.delete_branch(branch_name)

    async def get_branch_sha(self, branch_name):
        """Get the SHA of a branch."""
        return await self.provider.get_branch_sha(branch_name)
    
    async def check_repo_exists(self):
        return await self.provider.check_repo_exists()
    
    async def validate_username(self, provided_username):
        return await self.provider.validate_username(provided_username)
    
    async def update_file(self, file_path, commit, content_json, branch):
        """Update a file in the repository."""
        return await self.provider.update_file(file_path, commit, content_json, branch)
    
    async def commit_multiple_files(self, files_to_commit, commit, branch):
        return await self.provider.commit_multiple_files(files_to_commit, commit, branch)
    
    async def get_file_content_by_version_tag(self, file_path, ref):
        return await self.provider.get_file_content_by_version_tag(file_path, ref)
    
    async def get_tags(self):
        return await self.provider.get_tags()

