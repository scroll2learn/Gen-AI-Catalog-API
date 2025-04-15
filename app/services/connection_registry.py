import asyncio
import base64
import json
import logging
import os
from google.cloud import bigquery
from app.connections.destination.models.gcs import DestinationGCS
from app.connections.destination.models.mysql import DestinationMySql
from app.connections.destination.models.oracle import DestinationOracle
from app.connections.destination.models.s3 import DestinationS3
from app.connections.source.models.gcs import SourceGCS
from app.connections.source.models.mysql import SourceMySql
from app.connections.source.models.oracle import SourceOracle
from app.connections.source.models.s3 import SourceS3
from app.enums.bh_project import Status
from app.models.data_source import DataSource
from app.models.data_source_layout import DataSourceLayout
from app.models.layout_fields import LayoutFields
from app.utils.data_source_utils import get_text_embedding
import asyncpg
import aiomysql
import oracledb
from random import choices
from string import ascii_lowercase, digits
from typing import List, Optional
from app.connections.destination.models.connection_local import DestinationLocal
from app.connections.destination.models.postgres import DestinationPostgres
from app.connections.source.models.connection_local import SourceLocal
from app.exceptions.connection_registry import NotValidConnectionType
from fastapi import HTTPException
from google.api_core.exceptions import NotFound
from sqlalchemy import select, func
from google.oauth2 import service_account
from app.models.connection_registry import (
    ConnectionRegistry,
    ConnectionRegistryCreate,
    ConnectionRegistryUpdate,
    ConnectionRegistryReturn,
    ConnectionConfig,
    ConnectionConfigCreate,
    ConnectionConfigUpdate,
    ConnectionConfigReturn
)
from app.connections.destination.models.bigquery import DestinationBigquery
from app.connections.destination.models.snowflake import DestinationSnowflake
from app.connections.source.models.bigquery import SourceBigQuery
from app.connections.source.models.postgres import SourcePostgres
from app.connections.source.models.snowflake import SourceSnowflake
from app.enums.connection_registry import ConnectionStatusEnum, ConnectionTypes, GeographyEnum, SourceType
from app.services.base import BaseService
from app.services.aes import decrypt_string, encrypt_string
from app.core.config import Config
from app.utils.normalization import normalise_key, normalise_name

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionRegistryService(BaseService):
    model: ConnectionRegistry = ConnectionRegistry
    create_model: ConnectionRegistryCreate = ConnectionRegistryCreate
    update_model: ConnectionRegistryUpdate = ConnectionRegistryUpdate
    return_schema: ConnectionRegistryReturn = ConnectionRegistryReturn


class ConnectionConfigService(BaseService):
    model: ConnectionConfig = ConnectionConfig
    create_model: ConnectionConfigCreate = ConnectionConfigCreate
    update_model: ConnectionConfigUpdate = ConnectionConfigUpdate
    return_schema: ConnectionConfigReturn = ConnectionConfigReturn


    async def get_with_values(self, id: int, skip_encryption: bool = False) -> ConnectionConfigReturn:
        item: ConnectionConfig = await self.get(id)
        response = ConnectionConfigReturn(**item.__dict__)
        response.connection_name = item.connection_name
        iv_bytes = os.urandom(16)
        response.init_vector = base64.b64encode(iv_bytes).decode('utf-8')
        # Fetch and decrypt secret values
        secret_name = await self.make_secret_name(item.connection_name, item.connection_config_name)
        decrypted_config = await self.context.aws_service.secrets.get_secret(secret_name)
        
        if not skip_encryption:
            if isinstance(decrypted_config, dict) and 'config' in decrypted_config:
                decrypted_config_str = json.dumps(decrypted_config['config'])
                encrypted_values, _iv = encrypt_string(decrypted_config_str, response.init_vector)
                response.config = encrypted_values
            else:
                print(f'Config is not in expected format, please check secret {secret_name}')
        else:
            response.config = decrypted_config.get('config', {})

        return response



    async def create(self, item_body: ConnectionConfigCreate, authorized: Optional[dict] = None) -> ConnectionConfig:
        # Create and return model (without encrypted/decrypted data)
        # Make secret after creation has happened, in case of unique key violations
        secret_name = await self.make_secret(item_body)
        item_body.secret_name = secret_name
        item = await super().create(item_body, authorized=authorized)

        return item

    async def update_config(self, id: int, item_body: ConnectionConfigUpdate, authorized: Optional[dict] = None) -> ConnectionConfig:
        existing_obj = await self.model_update(id, item_body, avoid=['config', 'init_vector'])
        # Make secret after update has happened, in case of unique key violations
        secret_body = ConnectionConfigUpdate(
            **existing_obj.__dict__,
            config=item_body.config,
            init_vector=item_body.init_vector,
        )
        await self.make_secret(secret_body, existing_obj)
        return existing_obj

    async def make_secret(self, item_body: ConnectionConfigCreate, existing_obj: Optional[ConnectionConfig] = None) -> None:
        # Prepare details of secret
        """
        Create a secret in GCP/AWS for the given connection config.

        This takes the given connection config and makes a secret in GCP/AWS.
        The secret will have the name: <connection_name>-<connection_config_name>
        The secret will contain the following data:
        - conn_type: The type of connection (destination/source)
        - config: The decrypted config for the connection
        - custom_metadata: Any custom metadata provided in the connection config

        If the connection config has a config field, it is decrypted and validated
        based on the type of connection. If the config is not valid, a ValueError is raised.

        If the config is valid, the secret is created/updated in GCP/AWS.
        """
        logger.info("Starting make_secret process for connection config.")
    
        config_obj = existing_obj if existing_obj else item_body
        try:
            connection: ConnectionRegistry = await self.context.connection_registry.get(config_obj.connection_id)
            logger.info(f"Retrieved connection: {connection.connection_name}, Type: {connection.connection_type}")
        except Exception as e:
            logger.error(f"Error fetching connection details: {e}", exc_info=True)
            raise
        secrets_body = {'conn_type': connection.connection_name}

        if item_body.config:
            try:
                logger.info(f"Decrypting config for connection {connection.connection_name}")
                decrypted_config = decrypt_string(item_body.config, init_vector=item_body.init_vector)
                decrypted_config_dict = json.loads(decrypted_config)
                logger.info(f"Decryption successful for connection {connection.connection_name}")

                source_type = decrypted_config_dict.get('source_type' if connection.connection_type != ConnectionTypes.DESTINATION.value else 'destination_type')
                logger.info(f"Validating config for source type: {source_type}")

                config_data = None
                if connection.connection_type == ConnectionTypes.DESTINATION.value:
                    if source_type == SourceType.BIGQUERY.value:
                        validated_data = DestinationBigquery(**decrypted_config_dict)
                    elif source_type == SourceType.SNOWFLAKE.value:
                        validated_data = DestinationSnowflake(**decrypted_config_dict)
                    elif source_type == SourceType.LOCAL.value:
                        validated_data = DestinationLocal(**decrypted_config_dict)
                    elif source_type == SourceType.POSTGRES.value:
                        validated_data = DestinationPostgres(**decrypted_config_dict)
                    elif source_type == SourceType.MYSQL.value:
                        validated_data = DestinationMySql(**decrypted_config_dict)
                    elif source_type == SourceType.ORACLE.value:
                        validated_data = DestinationOracle(**decrypted_config_dict)
                    elif source_type == SourceType.S3.value:
                        validated_data = DestinationS3(**decrypted_config_dict)
                    elif source_type == SourceType.GCS.value:
                        validated_data = DestinationGCS(**decrypted_config_dict)
                    else:
                        raise NotValidConnectionType()
                else:
                    if source_type == SourceType.SNOWFLAKE.value:
                        validated_data = SourceSnowflake(**decrypted_config_dict)
                    elif source_type == SourceType.BIGQUERY.value:
                        validated_data = SourceBigQuery(**decrypted_config_dict)
                    elif source_type == SourceType.LOCAL.value:
                        validated_data = SourceLocal(**decrypted_config_dict)
                    elif source_type == SourceType.POSTGRES.value:
                        validated_data = SourcePostgres(**decrypted_config_dict)
                    elif source_type == SourceType.MYSQL.value:
                        validated_data = SourceMySql(**decrypted_config_dict)
                    elif source_type == SourceType.ORACLE.value:
                        validated_data = SourceOracle(**decrypted_config_dict)
                    elif source_type == SourceType.S3.value:
                        validated_data = SourceS3(**decrypted_config_dict)
                    elif source_type == SourceType.GCS.value:
                        validated_data = SourceGCS(**decrypted_config_dict)
                    else:
                        raise NotValidConnectionType()

                config_data = validated_data.dict() if hasattr(validated_data, "dict") else validated_data.dict_with_serialized_enum()
                secrets_body['config'] = config_data
                logger.info(f"Validation successful for {source_type}")

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse decrypted config JSON: {e}")
                raise ValueError(f"Failed to parse decrypted config JSON: {e}")
            except Exception as e:
                logger.error(f"Error decrypting or validating config: {e}")
                raise ValueError(f"Error decrypting config: {e}")

        if item_body.custom_metadata:
            secrets_body.update(item_body.custom_metadata)
            logger.info(f"Added custom metadata to secrets body.")

        try:
            # Generate secret name
            secret_name = await self.make_secret_name(connection.connection_name, config_obj.connection_config_name)
            logger.info(f"Creating/updating secret: {secret_name}")

            # Store secret in AWS (error handling included)
            await self.context.aws_service.secrets.new_secret(secret_name, json.dumps(secrets_body))
            logger.info(f"Successfully stored secret: {secret_name}")
            return secret_name

        except Exception as e:
            logger.error(f"Error storing secret in AWS: {e}", exc_info=True)
            raise

    async def make_secret_name(self, connection_name: str, connection_config_name: str) -> str:
        """
        Returns secret_name for storing connection secret values"
        """
        return f'{Config.CONNECTOR_PREFIX}-{normalise_key(connection_name)}-{normalise_key(connection_config_name)}'

    async def delete(self, id: int, authorized: Optional[dict] = None) -> bool:
        item: ConnectionConfig = await self.get(id)
        try:
            # Generate the secret name based on the connection and configuration names
            secret_name = await self.make_secret_name(item.connection_name, item.connection_config_name)
            await self.context.aws_service.secrets.delete_secret(secret_name)
        except NotFound:
            pass
        response = await super().delete(id, authorized=authorized)
        return response
    
    async def get_credentials(self, id: int, skip_encryption: bool = False) -> List[str]:
        item: ConnectionConfig = await self.get(id)
        response = ConnectionConfigReturn(**item.__dict__)
        response.connection_name = item.connection_name
        iv_bytes = os.urandom(16)
        response.init_vector = base64.b64encode(iv_bytes).decode('utf-8')
        secret_name = await self.make_secret_name(item.connection_name, item.connection_config_name)
        decrypted_config = await self.context.aws_service.secrets.get_secret(secret_name)
        return decrypted_config
    
    async def get_schemas_from_db_credentials(self, id: int) -> List[str]:
        credentials = await self.get_credentials(id)
        db_config = credentials['config']
        conn_type = credentials['conn_type']

        try:
            if conn_type == "postgres":
                db_host = db_config['host']
                db_port = db_config['port']
                db_name = db_config['database']
                db_user = db_config['username']
                db_password = db_config['password']

                # Connect to PostgreSQL
                conn = await asyncpg.connect(
                    host=db_host, port=db_port, database=db_name,
                    user=db_user, password=db_password
                )

                # Fetch schemas from PostgreSQL
                rows = await conn.fetch("SELECT schema_name FROM information_schema.schemata;")
                schemas = [row['schema_name'] for row in rows]

                await conn.close()

            elif conn_type == "mysql":
                db_host = db_config['host']
                db_port = db_config['port']
                db_user = db_config['username']
                db_password = db_config['password']

                # Connect to MySQL
                conn = await aiomysql.connect(
                    host=db_host, port=db_port,
                    user=db_user, password=db_password
                )
                # Fecth MySQL lists databases, not schemas (because mysql does not support schemas)
                async with conn.cursor() as cur:
                    await cur.execute("SHOW DATABASES;")  
                    rows = await cur.fetchall()
                    schemas = [row[0] for row in rows]

                conn.close()

            elif conn_type == "oracle":
                db_host = db_config.get('host')
                db_port = db_config.get('port')
                service_name = db_config.get('service_name')
                sid = db_config.get('sid')
                db_user = db_config.get('username')
                db_password = db_config.get('password')

                dsn = f"{db_host}:{db_port}/" + (service_name if service_name else sid)

                try:
                   
                    conn = await asyncio.to_thread(oracledb.connect, user=db_user, password=db_password, dsn=dsn)       
                    cur = await asyncio.to_thread(conn.cursor)
                    await asyncio.to_thread(cur.execute, "SELECT username FROM all_users")
                    rows = await asyncio.to_thread(cur.fetchall)
                    schemas = [row[0] for row in rows]

                    await asyncio.to_thread(cur.close)
                    await asyncio.to_thread(conn.close)

                except oracledb.DatabaseError as e:
                    raise HTTPException(status_code=500, detail=f"Oracle Database connection error: {str(e)}")
                
            elif conn_type == "bigquery":
                # Fetch dataset IDs from BigQuery

                project_id = db_config["project_id"]
                cred_info = db_config["credentials_json"] 

                creds = service_account.Credentials.from_service_account_info(cred_info)
                client = bigquery.Client(credentials=creds, project=project_id)

                datasets = list(client.list_datasets())
                if datasets:
                    schemas = [dataset.dataset_id for dataset in datasets]
                else:
                    schemas = []

            else:
                raise HTTPException(status_code=400, detail="Unsupported database type")

            return schemas

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


    async def get_tables_from_db_schema(self, id: int, schema: Optional[str] = None):
        credentials = await self.get_credentials(id)
        db_config = credentials['config']
        conn_type = credentials['conn_type']
        if conn_type == "postgres":
            db_host = db_config['host']
            db_port = db_config['port']
            db_name = db_config['database']
            db_user = db_config['username']
            db_password = db_config['password']
            try:
                # Connect to PostgreSQL
                conn = await asyncpg.connect(
                    host=db_host, port=db_port, database=db_name,
                    user=db_user, password=db_password
                )

                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = $1;
                """
                rows = await conn.fetch(query, schema)
                tables = [row['table_name'] for row in rows]

                await conn.close()
                return tables

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"PostgreSQL connection error: {str(e)}")

        elif conn_type == "mysql":
            db_host = db_config['host']
            db_port = db_config['port']
            db_user = db_config['username']
            db_password = db_config['password']
            db_name = db_config['database']  # MySQL uses database, not schema

            try:
                # Connect to MySQL
                conn = await aiomysql.connect(
                    host=db_host, port=db_port, user=db_user,
                    password=db_password, db=db_name
                )

                async with conn.cursor() as cur:
                    await cur.execute("SHOW TABLES;")
                    rows = await cur.fetchall()
                    tables = [row[0] for row in rows]

                conn.close()
                return tables

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"MySQL connection error: {str(e)}")

        elif conn_type == "oracle":
            db_host = db_config['host']
            db_port = db_config['port']
            service_name = db_config.get('service_name')
            sid = db_config.get('sid')
            db_user = db_config['username']
            db_password = db_config['password']
            
            dsn = f"{db_host}:{db_port}/" + (service_name if service_name else sid)

            try:
                # Connect to Oracle 
                conn = await asyncio.to_thread(oracledb.connect, user=db_user, password=db_password, dsn=dsn)
                conn = await asyncio.to_thread(oracledb.connect, user=db_user, password=db_password, dsn=dsn)       
                cur = await asyncio.to_thread(conn.cursor)
                query = "SELECT table_name FROM all_tables WHERE owner = :1"
                await asyncio.to_thread(cur.execute, query, (schema,))
                rows = await asyncio.to_thread(cur.fetchall)
                tables = [row[0] for row in rows]
                conn.close()
                return tables

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Oracle connection error: {str(e)}")

        elif conn_type == "bigquery":
            project_id = db_config["project_id"]
            cred_info = db_config["credentials_json"]  
            try:
                creds = service_account.Credentials.from_service_account_info(cred_info)
                client = bigquery.Client(credentials=creds, project=project_id)

                if not schema:
                    raise HTTPException(status_code=400, detail="Schema (dataset) is required for BigQuery")

                dataset_ref = client.dataset(schema)  # schema is the dataset name
                tables = list(client.list_tables(dataset_ref))  
                table_names = [table.table_id for table in tables]

                return table_names

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"BigQuery error: {str(e)}")

        else:
            raise HTTPException(status_code=500, detail="Unsupported database type")


    async def get_table_metadata(self, conn, conn_type, schema, table):
        """
        Fetch table metadata for PostgreSQL, MySQL, and Oracle etc.
        """
        if conn_type == "postgres":
            query = """
            SELECT 
                c.column_name AS name,
                c.data_type,
                c.ordinal_position,
                c.is_nullable,
                c.column_default AS default,
                c.character_maximum_length AS max_length,
                CASE 
                    WHEN kcu.column_name IS NOT NULL THEN TRUE 
                    ELSE FALSE 
                END AS is_primary_key
            FROM information_schema.columns c
            LEFT JOIN information_schema.key_column_usage kcu
                ON c.table_name = kcu.table_name 
                AND c.column_name = kcu.column_name 
                AND c.table_schema = kcu.table_schema
            LEFT JOIN information_schema.table_constraints tc
                ON kcu.constraint_name = tc.constraint_name 
                AND kcu.table_schema = tc.table_schema
                AND tc.constraint_type = 'PRIMARY KEY'
            WHERE c.table_schema = $1 AND c.table_name = $2;
            """
            rows = await conn.fetch(query, schema, table)

        elif conn_type == "mysql":
            query = """
            SELECT 
                COLUMN_NAME AS name,
                DATA_TYPE AS data_type,
                ORDINAL_POSITION AS ordinal_position,
                IS_NULLABLE AS is_nullable,
                COLUMN_DEFAULT AS `default`,  -- Use backticks to avoid syntax error
                CHARACTER_MAXIMUM_LENGTH AS max_length,
                CASE 
                    WHEN COLUMN_KEY = 'PRI' THEN TRUE 
                    ELSE FALSE 
                END AS is_primary_key
            FROM information_schema.columns
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
            """

            async with conn.cursor() as cur:
                await cur.execute(query, (schema, table))
                rows = await cur.fetchall()
                columns = []
                for row in rows:
                    columns.append({
                        "name": row[0],
                        "data_type": row[1],
                        "ordinal_position": row[2],
                        "is_nullable": row[3],
                        "default": row[4],
                        "max_length": row[5],
                        "is_primary_key": row[6],
                    })
                return columns

        elif conn_type == "oracle":
            query = """
            SELECT 
                c.column_name AS name,
                c.data_type,
                c.column_id AS ordinal_position,
                c.nullable AS is_nullable,
                c.data_default AS "default",
                c.data_length AS max_length,
                CASE 
                    WHEN pk.constraint_type = 'P' THEN 1 ELSE 0
                END AS is_primary_key
            FROM all_tab_columns c
            LEFT JOIN (
                SELECT cols.column_name, cons.constraint_type
                FROM all_cons_columns cols
                JOIN all_constraints cons 
                    ON cols.constraint_name = cons.constraint_name 
                    AND cons.owner = :1  -- Ensure correct schema filter
                WHERE cons.constraint_type = 'P' 
                    AND cols.table_name = :2
            ) pk ON c.column_name = pk.column_name
            WHERE c.owner = :1 AND c.table_name = :2
            """

            cur = await asyncio.to_thread(conn.cursor)      
            await asyncio.to_thread(cur.execute, query, (schema, table, schema, table)) 

            rows = await asyncio.to_thread(cur.fetchall)
            columns = []
            for row in rows:
                columns.append({
                    "name": row[0],
                    "data_type": row[1],
                    "ordinal_position": row[2],
                    "is_nullable": row[3],
                    "default": row[4],
                    "max_length": row[5],
                    "is_primary_key": row[6],
                })
            return columns

        elif conn_type == "bigquery":
            try:
                query = f"""
                SELECT column_name AS name, data_type, ordinal_position, is_nullable
                FROM `{schema}.INFORMATION_SCHEMA.COLUMNS`
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
                """
                query_job = conn.query(query)
                rows = query_job.result()
                return [{
                    "name": row["name"],
                    "data_type": row["data_type"],
                    "ordinal_position": row["ordinal_position"],
                    "is_nullable": row["is_nullable"] == "YES",
                    "default": None,
                    "max_length": None,
                    "is_primary_key": False
                } for row in rows]

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"BigQuery metadata error: {str(e)}")

        else:
            raise HTTPException(status_code=500, detail="Unsupported database type")

        return [dict(row) for row in rows]
    
    async def get_table_relationships(self, conn, conn_type, schema, table):
        """
        Fetch table relationships (one-to-one, one-to-many, many-to-one, many-to-many)
        for PostgreSQL, MySQL, and Oracle.
        """
        if conn_type == "postgres":
            query = """
            SELECT DISTINCT ccu.table_name AS related_table
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND (kcu.table_name = $1 OR ccu.table_name = $1)
                AND tc.table_schema = $2;
            """
            rows = await conn.fetch(query, table, schema)
        
        elif conn_type == "mysql":
            query = """
            SELECT DISTINCT REFERENCED_TABLE_NAME AS related_table
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE (TABLE_NAME = %s OR REFERENCED_TABLE_NAME = %s)
                AND TABLE_SCHEMA = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL;
            """
            async with conn.cursor() as cur:
                await cur.execute(query, (table, table, schema))
                rows = await cur.fetchall()
        
        elif conn_type == "oracle":
            query = """
            SELECT DISTINCT a.TABLE_NAME AS related_table
            FROM all_cons_columns a
            JOIN all_constraints c
                ON a.constraint_name = c.constraint_name
            WHERE c.constraint_type = 'R'
                AND c.OWNER = :1
                AND (a.table_name = :2 OR a.table_name IN (
                    SELECT table_name FROM all_cons_columns WHERE constraint_name = c.r_constraint_name
                ));
            """
            cur = await asyncio.to_thread(conn.cursor)
            await asyncio.to_thread(cur.execute, query, (schema, table))
            rows = await asyncio.to_thread(cur.fetchall)
        
        elif conn_type == "bigquery":
            # BigQuery does not explicitly store relationships in INFORMATION_SCHEMA
            rows = []  # No direct query available
        
        else:
            return ""
        
        related_tables = [row[0] for row in rows]
        return ", ".join(related_tables) if related_tables else ""


    async def create_data_source_and_layout_for_each_table(self, connection_config_id: int, schema: str, tables: list, bh_project_id: int, authorized: dict = None):
        """
        Create DataSource and Layout for tables in PostgreSQL, MySQL, and Oracle.
        """
        created_data_sources = []
        async with self.context.db_session as session:
            try:
                last_id_query = select(func.max(DataSource.data_src_id))
                last_layout_field_id_query = select(func.max(LayoutFields.lyt_fld_id))
                result = await session.execute(last_id_query)
                field_result = await session.execute(last_layout_field_id_query)
                last_id = result.scalar()  
                field_last_id = field_result.scalar()
                last_id = last_id if last_id is not None else 0 
                field_last_id = field_last_id if field_last_id is not None else 0

                field_last_id = field_last_id + 1
                new_id = last_id + 1  
                credentials = await self.get_credentials(connection_config_id)
                db_config = credentials.get('config')
                conn_type = credentials.get('conn_type')
                db_host = db_config.get('host')
                db_port = db_config.get('port')
                db_user = db_config.get('username')
                db_password = db_config.get('password')
                db_name = db_config.get('database')  # MySQL/Oracle compatibility
                service_name = db_config.get('service_name')
                sid = db_config.get('sid')

                if conn_type == "postgres":
                    conn = await asyncpg.connect(
                        host=db_host, port=db_port, database=db_name, 
                        user=db_user, password=db_password
                    )

                elif conn_type == "mysql":
                    conn = await aiomysql.connect(
                        host=db_host, port=db_port, user=db_user,
                        password=db_password, db=db_name
                    )

                elif conn_type == "oracle":
                    dsn = f"{db_host}:{db_port}/" + (service_name if service_name else sid)
                    conn = await asyncio.to_thread(oracledb.connect, user=db_user, password=db_password, dsn=dsn)
                elif conn_type == "bigquery":
                    project_id = db_config["project_id"]
                    cred_info = db_config["credentials_json"]  
                    creds = service_account.Credentials.from_service_account_info(cred_info)
                    conn = bigquery.Client(credentials=creds, project=project_id)

                else:
                    raise HTTPException(status_code=500, detail="Unsupported database type")
                data_source_ids = []
                for table in tables:
                    relationships = await self.get_table_relationships(conn, conn_type, schema, table)
                    data_source = DataSource(
                        data_src_id=new_id,
                        data_src_name=table,
                        connection_config_id=connection_config_id,
                        data_src_status_cd=1,
                        data_src_status=Status.ACTIVE.value,
                        created_by=authorized['user_detail_id'] if authorized else None,
                        bh_project_id=bh_project_id,
                        data_src_key=f"{bh_project_id}_{table}",
                        data_src_relationships=relationships
                    )
                    if authorized:
                        data_source = self.insert_user_fields(data_source, authorized, type="create")

                    session.add(data_source)
                    await session.flush()

                    data_layout = DataSourceLayout(
                        data_src_id=data_source.data_src_id,
                        data_src_lyt_name=table,
                        data_src_lyt_fmt_cd=1,
                        data_src_lyt_type_cd=1,
                        data_src_lyt_is_mandatory=True,
                        data_src_lyt_key=f"{bh_project_id}_{table}",
                        created_by=authorized['user_detail_id'] if authorized else None,
                    )
                    session.add(data_layout)
                    await session.flush()
                    created_data_sources.append({
                        "data_src_id": data_source.data_src_id,
                        "table": table
                    })

                    columns = await self.get_table_metadata(conn, conn_type, schema, table)
                    for column in columns:
                        layout_field = LayoutFields(
                            lyt_fld_id=field_last_id,
                            lyt_fld_name=column['name'],
                            lyt_fld_order=column['ordinal_position'],
                            lyt_fld_is_pk=column['is_primary_key'],
                            lyt_fld_data_type_cd=self.map_column_data_type_cd(column['data_type']),
                            lyt_fld_data_type=self.map_column_data_type(column['data_type']),
                            lyt_fld_source_data_type=column['data_type'],
                            lyt_fld_key=normalise_name(column['name']),
                            lyt_id=data_layout.data_src_lyt_id,
                            created_by=authorized['user_detail_id'] if authorized else None,
                            lyt_fld_length=column['max_length'],
                        )
                        session.add(layout_field)
                        field_last_id += 1
                    data_source_ids.append(new_id)
                    new_id += 1        
                await session.commit()
                conn.close()
                
            except Exception as e:
                await session.rollback()
                raise Exception(f"Error creating data source and layout: {str(e)}")

        return created_data_sources, data_source_ids
    
    def map_column_data_type(self, column_type: str):
        """
        Maps a column type to its corresponding data type.

        Args:
            column_type (str): The column type to map.

        Returns:
            str: The mapped data type.
        """
        column_type = column_type.lower()

        mapping = {
            # Integer types
            "smallint": "Integer",
            "int": "Integer",
            "integer": "Integer",
            "bigint": "Long",
            "tinyint": "Byte",
            "mediumint": "Integer",

            # String types
            "varchar": "String",
            "character varying": "String",
            "char": "String",
            "text": "String",
            "tinytext": "String",
            "mediumtext": "String",
            "longtext": "String",
            "clob": "String",

            # Boolean type
            "boolean": "Boolean",
            "bool": "Boolean",

            # Date & Time types
            "date": "Date",
            "datetime": "Timestamp",
            "timestamp": "Timestamp",
            "time": "Time",
            "year": "Date",

            # Numeric types
            "decimal": "Decimal",
            "numeric": "Decimal",
            "double": "Double",
            "double precision": "Double",
            "float": "Float",
            "real": "Float",

            # JSON types
            "json": "Json",
            "jsonb": "Json",

            # Array types
            "array": "Array",

            # Binary types
            "binary": "Binary",
            "varbinary": "Binary",
            "blob": "Binary",
            "tinyblob": "Binary",
            "mediumblob": "Binary",
            "longblob": "Binary",

            # Others
            "uuid": "String",
            "enum": "String",
            "set": "String",
            "xml": "String"
        }

        return mapping.get(column_type, "Unknown")  # Default to "Unknown" if no match is found


    def map_column_data_type_cd(self, column_type: str):
        # Map SQL column types to integer codes for lyt_fld_data_type_cd
        return 0
        #TODO will remove later
        # if column_type == 'integer':
        #     return 1  # Example: map Integer to code 1
        # elif column_type == 'character varying':
        #     return 2  # Example: map String to code 2
        # elif column_type == 'boolean':
        #     return 3  # Example: map Boolean to code 3
        # else:
        #     return 99  # Unknown type
