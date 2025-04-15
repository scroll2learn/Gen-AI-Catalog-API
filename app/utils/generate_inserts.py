from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import JSON, JSONB  # Import JSON types specific to PostgreSQL
import sqlalchemy
from faker import Faker
import re

# Database connection details
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/bighammer_db"

# Initialize Faker
faker = Faker()

# Tables to exclude from data generation
exclude_tables = ['alembic_version', 'app_user', 'bh_user']

# Mapping function to infer and generate data based on column types and names
def generate_data(column):
    column_name_lower = column.name.lower()
    if "email" in column_name_lower:
        return faker.email()
    elif "password" in column_name_lower:
        return faker.password()
    elif re.search(r"(info|details|json)", column_name_lower) or isinstance(column.type, (JSON, JSONB)):
        # Provide an empty JSON object for JSON/JSONB columns or columns with specific keywords
        return '{}'
    elif isinstance(column.type, sqlalchemy.Integer):
        return faker.random_int(min=1, max=1000)
    elif isinstance(column.type, sqlalchemy.String):
        return faker.word()
    elif isinstance(column.type, sqlalchemy.Boolean):
        return faker.boolean()
    # Add more conditions for other data types as needed

# Function to generate an INSERT statement for a given table and data dictionary
def generate_insert_statement(table, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join([f"'{value}'" if isinstance(column.type, sqlalchemy.String) else str(value) 
                              for column, value in zip(table.columns, data.values())])
    return f"INSERT INTO {table.name} ({columns}) VALUES ({placeholders});\n"

# Connect to the database and reflect the schema
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
metadata.reflect(engine)

with open('test.sql', 'w') as file:
    for table_name, table in metadata.tables.items():
        if table_name in exclude_tables:
            continue  # Skip tables in the exclude list
        
        for _ in range(5):  # Assuming we want to generate 5 rows per table
            data = {column.name: generate_data(column) for column in table.columns}
            insert_statement = generate_insert_statement(table, data)
            file.write(insert_statement)

print("Generated test data INSERT statements in 'test.sql'.")
