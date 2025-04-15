import re
from typing import Optional

from app.exceptions.git import GitCreateBranchException, GitUrlNotValid, GitWrapperException
from app.models.bh_project import BHProject
from app.utils.git_utils.git_wrapper import GitWrapper



def extract_secret_name(secret_path: str) -> str:
    # Extract the secret name from the secret path
    parts = secret_path.split('/')
    
    # The secret name is the part after 'secrets/'
    for i, part in enumerate(parts):
        if part == 'secrets':
            return parts[i + 1]
    
    # Return None if 'secrets/' is not found
    return None

def check_git_url_format(url: str):
    # Check the URL is in correct format
    pattern = r'^https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\/?$'
    if not re.match(pattern, url):
            raise GitUrlNotValid()
    
    return True

        

def extract_github_org_and_repo(url: str) -> str:
    """Extract the Github username and repo from the URL."""
    parts = url.rstrip('/').split('/')
    url_username, repo = parts[-2], parts[-1]
    return url_username, repo


async def initialize_git_provider(project: BHProject, github_token: Optional[str] = None) -> GitWrapper:
    """Initialize the GitWrapper for the project."""
    github_org, repo = extract_github_org_and_repo(project.bh_github_url)
    try:
        return GitWrapper(
            github_token, 
            github_org, 
            repo,  
            project.bh_github_provider
        )
    except Exception as e:
        raise GitWrapperException(context={"error": str(e)})

async def create_git_branch(git_provider: GitWrapper, branch_name: str) -> None:
    """Create a new branch using the Git provider."""
    response = await git_provider.create_branch(branch_name)
    if response.get('status') != 201:
        raise GitCreateBranchException(
            context={"error": str(response.get('message'))}
        )
