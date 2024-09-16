import os
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql.base import SQLDatabaseChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Database connection
db = SQLDatabase.from_uri("postgresql://postgres:password@localhost:5432/chinook")

# Callback manager for streaming output
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Local LLM setup (Llama 2 7B)
llm = LlamaCpp(
    model_path="llama-2-7b-chat.Q5_K_M.gguf",
    n_gpu_layers=40,  # Adjust based on your GPU memory
    n_batch=512,
    n_ctx=4096,
    f16_kv=True,  # GPU acceleration
    callback_manager=callback_manager,
    verbose=True,
)

# Custom prompt template
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here
Reasoning: Explanation of the reasoning behind the answer

Only use the following tables:
{table_info}

Very important: do not include quotes around the query when calling the database.
If you get an error while executing the SQLQuery, rewrite the query and try again.

Question: {input}"""

PROMPT = PromptTemplate(
    input_variables=["input", "table_info"],
    template=_DEFAULT_TEMPLATE,
)

# Create the SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)

# Function to get table info
def get_table_info():
    return db.get_table_info()

# Main chat function
def chat_with_db(question):
    try:
        table_info = get_table_info()
        result = db_chain.invoke(input=question, table_info=table_info)
        return result
    except Exception as e:
        print(f"Error in chat_with_db: {e}")
        return str(e)

# Example usage
if __name__ == "__main__":
    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        
        if question.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        response = chat_with_db(question)
        print(response)
        print()  # Add a blank line for better readability