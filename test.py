from sqlalchemy import create_engine,text


# Connect without selecting a specific DB
engine = create_engine(f"mysql+pymysql://root:root@localhost:3306")

with engine.connect() as conn:
    result = conn.execute(text("SHOW DATABASES;"))
    for row in result:
        print(row[0])
