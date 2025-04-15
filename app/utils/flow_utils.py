import re
import json

# Custom exceptions in your own package:
from app.exceptions.flow import FlowNameAlphanumeric, FlowNameMinimumLength


def validate_flow_name(flow_name: str):
    """
    Checks if the flow name is at least 3 characters long and strictly alphanumeric.
    Raises custom exceptions if validation fails.
    """
    if len(flow_name) < 3:
        raise FlowNameMinimumLength("Flow name must be at least 3 characters long.")

    if not re.match(r"^[A-Za-z0-9]+$", flow_name):
        raise FlowNameAlphanumeric("Flow name must contain only letters and digits.")


def json_parser(json_str: str) -> dict:
    """
    Parses the given JSON string into a Python dictionary.
    """
    return json.loads(json_str)


def create_flow_release_version(flow_version: str = None) -> str:
    """
    If no flow_version is provided, defaults to 1.0.0.
    Otherwise, increments the last number in the provided version string by 1.
    """
    if not flow_version:
        return "1.0.0"
    version_parts = flow_version.split(".")
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    return ".".join(version_parts)
