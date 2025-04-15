import base64
import requests
from app.core.config import Config
import logging

from app.exceptions.git import GitUsernameNotAuthorized

logger = logging.getLogger(__name__)

class GitHubProvider:
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f'{Config.GITHUB_PROVIDER_BASE_URL}/repos/{self.owner}/{self.repo}'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    async def validate_token(self):
        """Validate the GitHub Token."""
        user_url = f'{Config.GITHUB_PROVIDER_BASE_URL}/user'
        try:
            response = requests.get(user_url, headers=self.headers)
            if response.status_code == 200:
                logger.info("Token is valid.")
                return {"status": 200, "message": "Token is valid."}
            else:
                logger.error(f"Token validation failed. Status code: {response.status_code}")
                return {"status": 401, "message": f"Token validation failed. Url: {user_url}"}
        except Exception as e:
            logger.error(f"Failed to validate token: {str(e)}")
            return {"status": 500, "message": f"Error occurred while validating token. Url: {user_url}"}


    async def get_branch_sha(self, branch_name):
        """Get the SHA of the branch."""
        branch_url = f'{self.base_url}/git/ref/heads/{branch_name}'
        try:
            response = requests.get(branch_url, headers=self.headers)
            if response.status_code == 200:
                sha = response.json()['object']['sha']
                logger.info(f"Branch '{branch_name}' SHA retrieved successfully.")
                return {"status": 200, "sha": sha, "message": f"Branch '{branch_name}' SHA retrieved successfully."}
            else:
                logger.error(f"Failed to get branch SHA. Status code: {response.status_code}")
                return {"status": response.status_code, "message": f"Error occurred while retrieving branch SHA. Url: {branch_url}"}

        except Exception as e:
            logger.error(f"Failed to retrieve branch SHA: {str(e)}")
            return {"status": 500, "message": f"Error occurred while retrieving branch SHA. Url: {branch_url}"}

    async def create_branch(self, new_branch='main'):
        """Create a new branch from the base branch."""
        # Get the default branch     
        
        try:
            repo_info = requests.get(self.base_url, headers=self.headers).json()        
            default_branch = repo_info['default_branch']
        except Exception as e:
            logger.error(f"Repository does not exist.")
            return {"status": 404, "message": f"Repository does not exist. Url: {self.base_url}"}

        # Get the SHA of the base branch
        branch_sha_response = await self.get_branch_sha(default_branch)
        if branch_sha_response['status'] == 409:
            # Repository might be empty, so create initial commit
            logger.info(f"Repository is empty or base branch '{default_branch}' not found. Creating initial commit.")
            init_commit_result = await self.create_initial_commit(file_path='README.md',
                                                                commit_message='Initial commit',
                                                                content='# Initial Commit\n\nThis is the first commit in the repository.',
                                                                branch_name=new_branch)
            if init_commit_result['status'] == 201:
                logger.info(f"Initial commit created successfully in branch '{new_branch}'.")
                return {"status": 201, "message": f"Initial commit created successfully in branch '{new_branch}'."}
            else:
                logger.error("Failed to create initial commit.")
                return {"status": 500, "message": f"Failed to create initial commit. Url: {self.base_url}/contents/README.md"}

        elif branch_sha_response['status'] == 200:
            base_sha = branch_sha_response['sha']
        else:
            logger.error(branch_sha_response['message'])
            return {"status": branch_sha_response['status'], "message": branch_sha_response['message']}

        create_branch_url = f'{self.base_url}/git/refs'
        payload = {
            "ref": f"refs/heads/{new_branch}",
            "sha": base_sha
        }
        try:
            response = requests.post(create_branch_url, json=payload, headers=self.headers)
            if response.status_code == 201:
                logger.info(f"Branch '{new_branch}' created successfully.")
                return {"status": 201, "message": f"Branch '{new_branch}' created successfully."}
            elif response.status_code == 409:
                logger.info(f"Branch '{new_branch}' already exists after initial commit.")
                return {"status": 409, "message": f"Branch '{new_branch}' already exists."}
            elif response.status_code == 422:
                logger.error(f"branch already exists.: {new_branch}")
                return {"status": 201, "message": f"branch already exists.: {new_branch}"}
            else:
                logger.error(f"Failed to create branch. Status code: {response.status_code}")
                return {"status": response.status_code, "message": "Failed to create branch."}
        except Exception as e:
            logger.error(f"Exception occurred while creating branch: {str(e)}")
            return {"status": 500, "message": f"Exception occurred while creating branch. Url: {create_branch_url}"}


    async def create_initial_commit(self, file_path, commit_message, content, branch_name):
        """Create an initial commit by adding a file to the repository."""
        # Encode the content to      as required by the GitHub API
        encoded_content = base64.b64encode(content.encode()).decode()

        create_file_url = f'{self.base_url}/contents/{file_path}'
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch_name
        }
        try:
            response = requests.put(create_file_url, json=payload, headers=self.headers)
            if response.status_code == 201:
                response_data = response.json()
                commit_id = response_data["commit"]["sha"]  # Extract commit ID (SHA)
                logger.info(f"Initial commit created successfully in branch '{branch_name}'. Commit ID: {commit_id}")
                return {
                    "status": 201,
                    "message": f"Initial commit created successfully in branch '{branch_name}'.",
                    "commit_id": commit_id
                }
            else:
                logger.error(f"Failed to create initial commit. Status code: {response.status_code}")
                logger.error(f"Response: {response.json()}")
                return {"status": response.status_code, "message": "Failed to create initial commit."}
        except Exception as e:
            logger.error(f"Exception occurred while creating initial commit: {str(e)}")
            return {"status": 500, "message": f"Exception occurred while creating initial commit. Url: {create_file_url}"}

    async def delete_branch(self, branch_name):
        """Delete the branch."""
        pass

    async def check_in_code(self, branch_name, file_path, commit_message, content):
        pass

    async def check_repo_exists(self):
        try:
            repo_info = requests.get(self.base_url, headers=self.headers).json() 
            if repo_info.get('status') == 404:
                return {"status": 404, "message": f"Repository does not exist. Url: {self.base_url}"}
            return {"status": 200, "message": f"Repository exists. Url: {self.base_url}"}
        except Exception as e:
            logger.error(f"Repository does not exist.")
            return {"status": 404, "message": f"Repository does not exist. Url: {self.base_url}"}
        
    async def update_file(
        self,
        file_path: str,
        commit_message: str,
        content: str,
        branch_name: str,
    ):
        """Update an existing file in the repository."""
        # Encode the new content to Base64
        encoded_content = base64.b64encode(content.encode()).decode()

        # Construct the URL for the file to update
        file_url = f'{self.base_url}/contents/{file_path}'

        try:
            # Fetch the current file to retrieve the SHA
            get_response = requests.get(file_url, headers=self.headers, params={"ref": branch_name})
            if get_response.status_code != 200:
                logger.error(f"Failed to fetch the file. Status code: {get_response.status_code}")
                logger.error(f"Response: {get_response.json()}")
                return {"status": get_response.status_code, "message": "Failed to fetch the file."}

            file_data = get_response.json()
            current_sha = file_data["sha"]

            # Prepare payload for updating the file
            payload = {
                "message": commit_message,
                "content": encoded_content,
                "branch": branch_name,
                "sha": current_sha,
            }

            # Send the update request
            update_response = requests.put(file_url, json=payload, headers=self.headers)
            if update_response.status_code == 200:
                response_data = update_response.json()
                commit_id = response_data["commit"]["sha"]  # Extract commit ID (SHA)
                logger.info(f"File updated successfully in branch '{branch_name}'. Commit ID: {commit_id}")
                return {
                    "status": 200,
                    "message": f"File updated successfully in branch '{branch_name}'.",
                    "commit_id": commit_id,
                }
            else:
                logger.error(f"Failed to update the file. Status code: {update_response.status_code}")
                logger.error(f"Response: {update_response.json()}")
                return {"status": update_response.status_code, "message": "Failed to update the file."}

        except Exception as e:
            logger.error(f"Exception occurred while updating the file: {str(e)}")
            return {"status": 500, "message": f"Exception occurred while updating the file. Url: {file_url}"}
        

    async def commit_multiple_files(self, files_to_commit, commit, branch):
        try:
            # Step 1: Fetch the latest commit on the branch (or handle empty branch)
            ref_url = f"{self.base_url}/git/refs/heads/{branch}"
            ref_response = requests.get(ref_url, headers=self.headers)

            if ref_response.status_code == 200:
                ref_data = ref_response.json()
                base_tree_sha = ref_data["object"]["sha"]
            elif ref_response.status_code == 404:
                # Branch doesn't exist, create it later
                base_tree_sha = None
            else:
                return {"status": 500, "message": "Failed to fetch branch reference."}

            # Step 2: Prepare files for the tree
            commit_payload = []
            for file_path, content in files_to_commit.items():
                file_url = f"{self.base_url}/contents/{file_path}"
                encoded_content = base64.b64encode(content.encode()).decode()

                try:
                    # Fetch the file's SHA if it exists
                    get_response = requests.get(file_url, headers=self.headers, params={"ref": branch})
                    sha = get_response.json().get("sha") if get_response.status_code == 200 else None

                    commit_payload.append({
                        "path": file_path,
                        "mode": "100644",
                        "type": "blob",
                        "content": content,
                        "sha": sha,
                    })
                except Exception as e:
                    logger.error(f"Failed to fetch file {file_path}. Exception: {str(e)}")
                    return {"status": 500, "message": f"Error while preparing commit for {file_path}"}

            # Step 3: Create a tree with all the files
            tree_url = f"{self.base_url}/git/trees"
            tree_payload = {
                "base_tree": base_tree_sha,
                "tree": [
                    {
                        "path": file["path"],
                        "mode": "100644",
                        "type": "blob",
                        "content": file["content"],
                    } for file in commit_payload
                ],
            }
            tree_response = requests.post(tree_url, json=tree_payload, headers=self.headers)
            tree_response.raise_for_status()
            tree_data = tree_response.json()

            # Step 4: Create a commit with the new tree
            commit_url = f"{self.base_url}/git/commits"
            commit_payload = {
                "message": commit,
                "tree": tree_data["sha"],
                "parents": [base_tree_sha] if base_tree_sha else [],
            }
            commit_response = requests.post(commit_url, json=commit_payload, headers=self.headers)
            commit_response.raise_for_status()
            commit_data = commit_response.json()

            # Step 5: Update the branch reference or create it
            if base_tree_sha:
                # Update the branch reference to point to the new commit
                ref_update_payload = {"sha": commit_data["sha"]}
                requests.patch(ref_url, json=ref_update_payload, headers=self.headers)
            else:
                # Create the branch with the new commit
                ref_create_payload = {"ref": f"refs/heads/{branch}", "sha": commit_data["sha"]}
                requests.post(f"{self.base_url}/git/refs", json=ref_create_payload, headers=self.headers)

            return {
                "status": 201,
                "message": "Files committed successfully.",
                "commit_id": commit_data.get("sha"),
            }
        except Exception as e:
            logger.error(f"Exception occurred while creating commit: {str(e)}")
            return {"status": 500, "message": "Failed to create commit with all files."}

    async def validate_username(self, provided_username):
        """
        Validate if the provided username matches the repository owner or
        has access to the repository.
        """
        try:
            # Get repository 
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code != 200:
                logger.error("Failed to fetch repository details.")
                return {"status": response.status_code, "message": "Failed to fetch repository details."}

            repo_owner = response.json()['owner']['login']
            is_org = response.json()['owner']['type'] == 'Organization'

            # Check if the provided username matches the owner 
            if not is_org and repo_owner.lower() == provided_username.lower():
                logger.info("Username is valid and matches the repository owner.")
                return {"status": 200, "message": "Username is valid and matches the repository owner."}

            # If the owner is an organization, check if the username has access 
            if is_org:
                collaborator_check_url = f'{self.base_url}/collaborators/{provided_username}'
                collab_response = requests.get(collaborator_check_url, headers=self.headers)

                if collab_response.status_code == 204:
                    logger.info("Username is a valid has access to the repository.")
                    return {"status": 200, "message": "Username is a valid has access to the repository."}
                else:
                    raise GitUsernameNotAuthorized()
            logger.error("Username does not match repository owner or is not authorized.")
            return {"status": 401, "message": "Username does not match repository owner or is not authorized."}

        except Exception as e:
            logger.error(f"Failed to validate GitHub username: {str(e)}")
            return {"status": 500, "message": f"Error occurred while validating GitHub username. Url: {self.base_url}"}
        
    async def get_file_content_by_version_tag(self, file_path, ref='main'):
        """
        Fetch the content of a file from the GitHub repository.

        Args:
            file_path (str): The path of the file in the repository (e.g., 'pipeline/pipeline.json').
            branch (str): The branch to fetch the file from (default is 'main').

        Returns:
            dict: JSON object of the file content if successful, or an error message.
        """
        file_url = f'{self.base_url}/contents/{file_path}'
        try:
            response = requests.get(file_url, headers=self.headers, params={"ref": ref})
            if response.status_code == 200:
                file_data = response.json()
                content = base64.b64decode(file_data['content']).decode('utf-8')
                logger.info(f"File '{file_path}' fetched successfully.")
                return {
                    "status": 200,
                    "content": content,
                    "message": f"File '{file_path}' fetched successfully."
                }
            else:
                logger.error(f"Failed to fetch file '{file_path}'. Status code: {response.status_code}")
                return {"status": response.status_code, "message": f"Failed to fetch file '{file_path}'."}

        except Exception as e:
            logger.error(f"Exception occurred while fetching file '{file_path}': {str(e)}")
            return {"status": 500, "message": f"Error occurred while fetching file '{file_path}'."}
        
    async def get_tags(self):
        """
        Fetch the list of tags along with their descriptions, handling lightweight and annotated tags.

        Returns:
            dict: A dictionary containing the status and tags with descriptions or an error message.
        """
        try:
            # Fetch the list of tags
            response = requests.get(f"{self.base_url}/tags", headers=self.headers)
            if response.status_code != 200:
                return {
                    "status": response.status_code,
                    "message": response.json().get("message", "Failed to fetch tags.")
                }

            tags = response.json()
            detailed_tags = []
            
            for tag in tags:
                tag_name = tag["name"]

                # Fetch the tag reference
                ref_response = requests.get(
                    f"{self.base_url}/git/ref/tags/{tag_name}", headers=self.headers
                )
                if ref_response.status_code == 200:
                    ref_data = ref_response.json()
                    object_type = ref_data["object"]["type"]
                    object_sha = ref_data["object"]["sha"]
                    
                    if object_type == "tag":  
                    # Annotated tag which is created from github command 
                    # ex.  git tag -a <tag_name> -m "<tag_message>"
                    # git push origin <tag_name>

                        tag_response = requests.get(
                            f"{self.base_url}/git/tags/{object_sha}", headers=self.headers
                        )
                        if tag_response.status_code == 200:
                            tag_data = tag_response.json()
                            detailed_tags.append({
                                "name": tag_name,
                                "description": tag_data.get("message", ""),
                                "sha": object_sha
                            })
                        else:
                            detailed_tags.append({
                                "name": tag_name,
                                "description": "Failed to fetch tag description",
                                "sha": object_sha
                            })
                    elif object_type == "commit":
                        # Lightweight tag which is created from github ui
                        detailed_tags.append({
                            "name": tag_name,
                            "description": "Lightweight tag, no description available",
                            "sha": object_sha
                        })
                else:
                    detailed_tags.append({
                        "name": tag_name,
                        "description": "Failed to fetch tag reference",
                        "sha": None
                    })

            return {"status": 200, "tags": detailed_tags}
        except requests.exceptions.RequestException as e:
            return {"status": 500, "message": str(e)}
