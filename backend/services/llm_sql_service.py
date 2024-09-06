import google.generativeai as genai
from config import GOOGLE_API_KEY
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from templates import sql_template, sql_query_template
from dotenv import load_dotenv
from fastapi import HTTPException
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=GOOGLE_API_KEY)
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

# Initialize chat history
chat_history = [AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database.")]

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Connect to the SQLite database
        self.db = SQLDatabase.from_uri("sqlite:///Data/sqlite/db.sqlite")
        print("Connection established with SQLite database")
        
        # Define SQL chain
        def get_schema(_):
            return self.db.get_table_info()
        
        self.sql_chain = (
            RunnablePassthrough.assign(schema=get_schema)
            | ChatPromptTemplate.from_template(sql_template)
            | model
            | StrOutputParser()
        )
        print("SQL Chain initialized successfully")

    def get_db(self):
        return self.db
    
    def get_sql_chain(self):
        return self.sql_chain


async def upload_sql_file(sql_file):
    UPLOAD_DIR = os.path.join(os.getcwd(), "Data")
    UPLOAD_DIR = os.path.join(UPLOAD_DIR, "sqlite")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, "db.sqlite")
    
    if not sql_file.filename.endswith('.sqlite'):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file must have a .sqlite extension"
        )
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await sql_file.read())

    return file_path


def get_response(user_query: str, chat_history: list):
    if user_query.strip():
        chat_history.append(HumanMessage(content=user_query))

    db_manager = DatabaseManager()
    db = db_manager.get_db()
    sql_chain = db_manager.get_sql_chain()
    
    if db is None:
        return "Database connection is not established."
    if sql_chain is None:
        return "SQL Chain is not initialized."
    
    template = sql_query_template
    prompt = ChatPromptTemplate.from_template(template)
    
    try:
        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                response=lambda vars: db.run(vars["query"]),
            )
            | prompt
            | model
            | StrOutputParser()
        )
        
        response = chain.invoke({
            "question": user_query,
            "chat_history": chat_history,
        })

        chat_history.append(AIMessage(content=response))

        return response
    except Exception as e:
        return f"Error in get_response: {e}"
