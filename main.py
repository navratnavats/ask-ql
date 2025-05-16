from db.connection import connect_to_mysql
from agents.sql_agent import create_sql_agent_executor

db = connect_to_mysql()

selected_db_name = db._engine.url.database
print(f" Connected to database from main: {selected_db_name}")

sql_agent = create_sql_agent_executor(db)
print("SQL Agent created successfully.")
print("You can now use the SQL agent to interact with your database.")
print("---------------------------")
print("Agent ready to use. Type exit to quit")

while True:
    user_input = input("Ask your question: ")
    if user_input.lower() in ("exit", "quit"):
        print("Exiting...")
        break
    try:
        response = sql_agent.invoke(user_input)
        print("Response:", response.get("output", "No output found"))
    except Exception as e:
        print("Error:", e)
        print("Please try again.")