import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent as create_sql_agent_from_langchain
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

def create_sql_agent_executor(db):
    llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPEN_API_KEY"), model="gpt-4.1-mini")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_sql_agent_from_langchain(llm=llm, toolkit=toolkit, verbose=True)
