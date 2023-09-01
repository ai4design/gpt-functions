import os
import json
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# --------------------------------------------------------------
# Use OpenAI’s Function Calling Feature
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "get_law_info",
        "description": "Get the legal information",
        "parameters": {
            "type": "object",
            "properties": {
                "law": {
                    "type": "string",
                    "description": "The law in question",
                },
                "question": {
                    "type": "string",
                    "description": "The query about the law",
                },
            },
            "required": ["law", "question"],
        },
    }
]


def get_law_info(law, question):
    """Get the legal context information"""
    # Example output returned from an API or database
    return {
        "law": law,
        "question": question,
    }


def ask_and_reply(prompt):
    """Give LLM a given prompt and get an answer."""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": prompt}],
        functions=function_descriptions,
        function_call="auto",  # specify the function call
    )

    return completion.choices[0].message


# Scenario: Legal advice

user_prompt = "Eu fui demitido sem justa causa, o que posso fazer?"
output = ask_and_reply(user_prompt)

law = json.loads(output.function_call.arguments).get("law")
question = json.loads(output.function_call.arguments).get("question")
chosen_function = eval(output.function_call.name)
law_info = chosen_function(law, question)

print(law)
print(question)
print(law_info)


# --------------------------------------------------------------
# Make It Conversational With Langchain
# --------------------------------------------------------------

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)

user_prompt = "Eu fui demitido após 1 ano de trabalho sem justa causa, o que posso fazer?"
first_response = llm.predict_messages(
    [HumanMessage(content=user_prompt)], functions=function_descriptions
)

print(first_response)
