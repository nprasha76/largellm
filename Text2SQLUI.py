import gradio as gr
import re
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

# Load the model and connect to DB (do this only once)
model = "qwen2.5"  # Replace with your model
llm = ChatOllama(model=model, base_url="http://localhost:11434")  # Replace with your Ollama base URL
try:
    db = SQLDatabase.from_uri("sqlite:///tview_db.db")  # Replace with your DB path
    sql_chain = create_sql_query_chain(llm, db)
except Exception as e:
    print(f"Error connecting to database: {e}")
    db = None  # Set db to None if connection fails
    sql_chain = None


def extract_sql_from_string(input_string):
    """
    Extracts the SQL query from a string, handling potentially unmatched backticks.
    Extracts ONLY the SQL statement.

    Args:
        input_string: The string containing the SQL query.

    Returns:
        The SQL query as a string, or None if no SQL query is found.
    """

    # 1. Remove "SQLQuery:" (case-insensitive) - Optional, if needed.
    input_string = re.sub(r"SQLQuery:\s*", "", input_string, flags=re.IGNORECASE)

    # 2. Extract content within backticks (handling unmatched backticks)
    match = re.search(r"```([\s\S]*?)```|``([\s\S]*?)``|`([\s\S]*?)`|```([\s\S]*)|``([\s\S]*)|`([\s\S]*)", input_string)

    if match:
        sql_query = ""
        for group in match.groups():  # Find which group contains the match
            if group is not None:
                sql_query = group.strip()
                break
    else:  # If there are no backticks, assume the rest of the string is the query
        sql_query = input_string.strip()

    return sql_query if sql_query else None  # Return None if the string is empty after cleaning


def convert_to_sql(question):
    if db is None or sql_chain is None:  # Handle DB connection failure
        return "Database connection failed. Please check the logs."

    try:
        response = sql_chain.invoke({'question': question+'You MUST RETURN ONLY MYSQL QUERY STRICTLY.'})
        print(response)
        print(extract_sql_from_string(response))
        return extract_sql_from_string(response)
    except Exception as e:
        return f"Error generating SQL: {e}"


with gr.Blocks() as demo:
    question_input = gr.Textbox(label="Enter your question")
    sql_output = gr.Textbox(label="SQL Query")
    convert_button = gr.Button("Convert to SQL")

    convert_button.click(
        convert_to_sql,
        inputs=question_input,
        outputs=sql_output
    )

demo.launch()

