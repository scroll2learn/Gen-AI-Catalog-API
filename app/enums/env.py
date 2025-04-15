from enum import Enum, auto

class FlowConnectionType(str ,Enum):
    AWS_S3 = 'aws_s3'
    GCS = 'gcs'
    SFTP = 'sftp'
    HTTP = 'http'
    EMAIL = 'email'