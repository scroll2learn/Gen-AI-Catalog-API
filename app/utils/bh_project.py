

def generate_github_secret_name(project_name: str) -> str:
    """
    Generate a GitHub secret name based on the project name.

    Args:
        project_name (str): The project name to format.

    Returns:
        str: A formatted GitHub secret name.
    """
    formatted_name = project_name.replace(" ", "_").lower()
    secret_name = f"github_{formatted_name}_secret"
    return secret_name
