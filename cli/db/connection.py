from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def list_available_databases():
    username, password, my_sql_host, my_sql_port = load_env_variables()
    try:
        engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{my_sql_host}:{my_sql_port}/",
            pool_pre_ping=True
        )
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            db_list = [row[0] for row in result]
            return db_list
    except Exception as e:
        print("Error during connection or query:", e)
        exit()

def connect_to_mysql():
    username, password, my_sql_host, my_sql_port = load_env_variables()
    db_list = list_available_databases()
    print("📦 Databases available:")
    for idx, db in enumerate(db_list):
        print(f"{idx+1} - {db}")
    print("-" * 30)

    print("Please select a database by entering the corresponding number:")
    
    select_db = input("Please select a database: ")
    if not select_db or not select_db.isdigit() or int(select_db) > len(db_list):
        print("Invalid database selection!")
        exit()

    selected_db = db_list[int(select_db) - 1]
    print("Selected database:", selected_db)

    db_uri = f"mysql+pymysql://{username}:{password}@{my_sql_host}:{my_sql_port}/{selected_db}"
    return SQLDatabase.from_uri(db_uri)


def load_env_variables():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        username = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        my_sql_host = os.getenv("MYSQL_HOST")
        my_sql_port = os.getenv("MYSQL_PORT")

        return username, password, my_sql_host, my_sql_port
    except ImportError:
        print("Error loading environment variables. Make sure you have 'python-dotenv' installed.")
        exit(1)