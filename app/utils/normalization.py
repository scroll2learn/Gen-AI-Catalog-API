"""
Functions to normalize keys used throughout the API
"""

import re


def normalise_key(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9]+', '', value).lower()

def normalise_name(value: str) -> str:
    return value.replace(" ", "_").lower()