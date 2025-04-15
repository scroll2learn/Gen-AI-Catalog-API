import re
from app.exceptions.pipeline import PipelineNameAlphanumeric

def generate_unique_key(name: str) -> str:
    """
    Generate a unique key by converting the input string to lowercase, 
    replacing spaces with underscores, and removing special characters.
    
    :param name: The input string (pipeline name)
    :return: A valid unique key string
    """
    # Convert the string to lowercase
    lower_case_name = name.lower()
    
    # Replace spaces with underscores
    replaced_spaces = lower_case_name.replace(" ", "_")
    
    # Remove all special characters except underscores and alphanumeric
    unique_key = re.sub(r'[^a-z0-9_]', '', replaced_spaces)
    
    return unique_key

def validate_pipeline_name(pipeline_name: str):
    if re.match(r"^[a-zA-Z]+$", pipeline_name):
        raise PipelineNameAlphanumeric()

def create_pipeline_release_version(pipeline_version: str = None) -> str:
    if not pipeline_version:
        return "v1.0.0"
    # increment the flow version
    version_parts = pipeline_version.split(".")
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_pipeline_version = ".".join(version_parts)
    
    return new_pipeline_version

def pipeline_sample_json():
    pipeline_json = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "name": "sample_pipeline",
    "description": "Sample pipeline abiding by the schemas defined",
    "version": "1.0",
    "mode": "DEBUG",
    "parameters": [],
    "sources": [
        {
        "name": "input_data",
        "source_type": "File",
        "file_name": "examples/input.csv",
        "connection": {
            "name": "local_connection",
            "connection_type": "Local",
            "file_path_prefix": "examples/"
        }
        },
        {
        "name": "lookup_data",
        "source_type": "File",
        "file_name": "examples/lookup.csv",
        "connection": {
            "name": "local_connection",
            "connection_type": "Local",
            "file_path_prefix": "examples/"
        }
        }
    ],
    "targets": [
        {
        "name": "output_data",
        "type": "File",
        "connection": {
            "type": "File",
            "file_path": "examples/output.csv"
        },
        "load_mode": "overwrite"
        }
    ],
    "transformations": [
        {
        "name": "read_input_data",
        "dependent_on": [],
        "transformation": "Reader",
        "source": {
            "name": "input_data",
            "source_type": "File",
            "file_name": "input.csv",
            "connection": {
            "name": "local_connection",
            "connection_type": "Local",
            "file_path_prefix": "examples/"
            }
        },
        "read_options": {
            "header": True
        }
        },
        {
        "name": "filter_transformation",
        "dependent_on": ["read_input_data"],
        "transformation": "Filter",
        "condition": "age >= 18"
        },
        {
        "name": "read_lookup_data",
        "dependent_on": [],
        "transformation": "Reader",
        "source": {
            "name": "lookup_data",
            "source_type": "File",
            "file_name": "lookup.csv",
            "connection": {
            "name": "local_connection",
            "connection_type": "Local",
            "file_path_prefix": "examples/"
            }
        },
        "read_options": {
            "header": True
        }
        },
        {
        "name": "join_transformation",
        "dependent_on": ["read_input_data", "read_lookup_data"],
        "transformation": "Joiner",
        "conditions": [
            {
            "join_input": "read_lookup_data",
            "join_condition": "read_input_data.id = read_lookup_data.id",
            "join_type": "left"
            }
        ],
        "expressions": [
            {
            "target_column": "full_name",
            "expression": "concat(read_input_data.name, ' ', read_input_data.city)"
            }
        ],
        "advanced": {
            "hints": [
            {
                "join_input": "read_input_data",
                "hint_type": "broadcast"
            }
            ]
        }
        },
        {
        "name": "schema_transformation",
        "dependent_on": ["join_transformation"],
        "transformation": "SchemaTransformation",
        "derived_fields": [
            {
            "name": "full_address",
            "expression": "concat(address, ' ', city, ' ', state, ' ', zip)"
            },
            {
            "name": "is_adult",
            "expression": "case when age >= 18 then 'Yes' else 'No' end"
            }
        ]
        },
        {
        "name": "sort_transformation",
        "dependent_on": ["schema_transformation"],
        "transformation": "Sorter",
        "sort_columns": [
            {
            "column": "city",
            "order": "asc"
            }
        ]
        },
        {
        "name": "aggregate_transformation",
        "dependent_on": ["schema_transformation"],
        "transformation": "Aggregator",
        "group_by": ["city"],
        "aggregate": [
            {
            "expression": "avg(age)",
            "target_column": "average_age"
            }
        ],
        "pivot": [
            {
            "pivot_column": "city",
            "pivot_values": ["New York", "Los Angeles", "Chicago"]
            }
        ]
        }
    ]
    }

    return pipeline_json