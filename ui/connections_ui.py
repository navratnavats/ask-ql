from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def load_env_variables():
    load_dotenv()
    return (
        os.getenv("MYSQL_USER"),
        os.getenv("MYSQL_PASSWORD"),
        os.getenv("MYSQL_HOST"),
        os.getenv("MYSQL_PORT")
    )

def connect_to_db_and_list(db_type):
    if db_type == "mysql":
        username, password, host, port = load_env_variables()
        engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/", pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            return [row[0] for row in result]
    elif db_type == "sqlite":
        base_dir = "cli/db/sqlite_dbs"  # Optional folder to organize .db files
        return [f for f in os.listdir(base_dir) if f.endswith(".db")]
    else:
        raise ValueError("Unsupported DB type")

def connect_to_selected_db(db_type, selected_db):
    if db_type == "mysql":
        username, password, host, port = load_env_variables()
        db_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{selected_db}"
    elif db_type == "sqlite":
        db_file = f"cli/db/sqlite_dbs/{selected_db}"
        db_uri = f"sqlite:///{db_file}"
    else:
        raise ValueError("Unsupported DB type")

    return SQLDatabase.from_uri(db_uri)
