from enum import Enum

class ParameterType(str, Enum):
    USER = 'USER'
    SPARK_SESSION = 'SPARK_SESSION'
