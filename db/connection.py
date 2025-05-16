from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def connect_to_mysql():
    load_dotenv()

    username = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    my_sql_host = os.getenv("MYSQL_HOST")
    my_sql_port = os.getenv("MYSQL_PORT")

    if not all([username, password, my_sql_host, my_sql_port]):
        print("One or more environment variables are missing!")
        exit()

    try:
        engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{my_sql_host}:{my_sql_port}/",
            pool_pre_ping=True
        )
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            db_list = [row[0] for row in result]
            print("📦 Databases available:")
            for idx, db in enumerate(db_list):
                print(f"{idx+1} - {db}")
    except Exception as e:
        print("Error during connection or query:", e)
        exit()

    select_db = input("Please select a database: ")
    if not select_db or not select_db.isdigit() or int(select_db) > len(db_list):
        print("Invalid database selection!")
        exit()

    selected_db = db_list[int(select_db) - 1]
    print("Selected database:", selected_db)

    # ✅ RETURN SQLDatabase object, not SQLAlchemy connection
    db_uri = f"mysql+pymysql://{username}:{password}@{my_sql_host}:{my_sql_port}/{selected_db}"
    return SQLDatabase.from_uri(db_uri)
