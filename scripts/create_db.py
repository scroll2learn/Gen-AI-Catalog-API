import logging
import os
import time
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

host = os.environ.get('POSTGRES_HOST')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
database = os.environ.get('POSTGRES_DB')
port = os.environ.get('POSTGRES_PORT', 5432)
sample_db = os.environ.get('SAMPLE_DB', '')

logger = logging.getLogger(__name__)

def check_db_exists():
    conn = None
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (database,)
        )
        exists = cursor.fetchone()
        print("Database exists:", exists)
        if exists:
            cursor.close()
            return True
        else:
            print("Creating database...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
            cursor.close()
            logger.info(f"Database {database} created")
            time.sleep(2)  # Adding a 2-second delay
    except Exception as e:
        logger.error(f"Error while checking if database exists: {e}")
    finally:
        if conn:
            conn.close()

def create_catalogdb_schema():
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute("CREATE SCHEMA IF NOT EXISTS catalogdb;")
        conn.commit()
        logger.info("Schema 'catalogdb' created successfully.")
    except Exception as e:
        logger.error(f"Error creating schema 'catalogdb': {e}")
    finally:
        if conn:
            conn.close()

def create_pgvector_extension():
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        # Set search path to include catalogdb schema
        cursor.execute("SET search_path TO catalogdb, public;")
        # Create the vector extension only once
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        logger.info("pgvector extension created successfully.")
    except Exception as e:
        logger.error(f"Error creating pgvector extension: {e}")
    finally:
        if conn:
            conn.close()

def check_and_create_db(db_name):
    """Check if the database exists and create it if not."""
    conn = None
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if exists:
            print(f"Database '{db_name}' already exists. Skipping creation.")
            return False  # Database exists, no need to create
        else:
            print(f"Creating database '{db_name}'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            cursor.close()
            logger.info(f"Database {db_name} created successfully.")
            time.sleep(2)  # Ensure DB is ready
            return True  # Indicates DB was just created
    except Exception as e:
        logger.error(f"Error while checking/creating database {db_name}: {e}")
    finally:
        if conn:
            conn.close()
    return False

if __name__ == '__main__':
    check_db_exists()
    create_catalogdb_schema()
    create_pgvector_extension()
    sample_db_created = check_and_create_db(sample_db)
    if sample_db_created:
        print("Sample db created database created. Ready for import.")
