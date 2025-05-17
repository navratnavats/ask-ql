import os
from db.connection import connect_to_mysql, list_available_databases, load_env_variables
from agents.sql_agent import create_sql_agent_executor
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text

EXITING_MSG= "Exiting..."

def show_additional_options():
    print("Additional options:")
    print("1. Try rephrasing your question")
    print("2. Switch database")
    print("3. Exit")


def prompt_for_question():
    user_input = input("Ask your question: ").strip()
    if not user_input:
        user_input = input("Ask your question: ").strip()
        if not user_input:
            print(EXITING_MSG)
            exit(0)
    return user_input


def switch_database():
    try:
        db = connect_to_mysql()
        agent = create_sql_agent_executor(db)
        return db, agent
    except (ValueError, IndexError) as e:
        print("Invalid selection. No change made.")
        return None, None
    except Exception as e:
        print("Error switching database:", e)
        return None, None

def handle_idk_response(sql_agent, db):
    while True:
        show_additional_options()
        next_action = input("Please select an option (1/2/3): ").strip()

        if next_action == "1":
            print("Try rephrasing your question.")
            return sql_agent, db, False

        elif next_action == "2":
            new_db, new_agent = switch_database()
            if new_db:
                db = new_db
                sql_agent = new_agent
            return sql_agent, db, False

        elif next_action == "3":
            print(EXITING_MSG)
            return None, None, True

        else:
            print("Invalid option. Try again.")

def handle_agent_response(sql_agent, db):
    user_input = prompt_for_question()

    if user_input.lower() in ("exit", "quit"):
        print(EXITING_MSG)
        return None, None, True

    if user_input.lower() in ("switch db", "switch database"):
        new_db, new_agent = switch_database()
        if new_db:
            db = new_db
            sql_agent = new_agent
        return sql_agent, db, False

    try:
        response = sql_agent.invoke(user_input)
        output = response.get("output", "No output found")
        print("Response:", output)

        if "I don't know" in output:
            return handle_idk_response(sql_agent, db)
        else:
            return sql_agent, db, False

    except Exception as e:
        print("Error:", e)
        print("Please try again.")
        return sql_agent, db, False

def main():
    db = connect_to_mysql()
    print("printing db", db)
    selected_db_name = db._engine.url.database
    print(f"Connected to database: {selected_db_name}")

    sql_agent = create_sql_agent_executor(db)
    print("SQL Agent created successfully.")
    print("You can now ask questions. Type 'exit' to quit.")
    print("-" * 30)

    exit_flag = False
    while not exit_flag:
        sql_agent, db, exit_flag = handle_agent_response(sql_agent, db)



if __name__ == "__main__":
    main()
