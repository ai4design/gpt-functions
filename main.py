import os
import json
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "Eu fui demitido sem justa causa, o que posso fazer?",
        },
    ],
)

output = completion.choices[0].message.content
print(output)

#########################

# --------------------------------------------------------------
# Use OpenAI’s Function Calling Feature
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "get_flight_info",
        "description": "Get the legal information",
        "parameters": {
            "type": "object",
            "properties": {
                "law": {
                    "type": "string",
                    "description": "A lei a qual se refere",
                },
                "question": {
                    "type": "string",
                    "description": "O que é possível fazer?",
                },
            },
            "required": ["law", "question"],
        },
    }
]

user_prompt = "Eu fui demitido sem justa causa, o que posso fazer?"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": user_prompt}],
    # Add function calling
    functions=function_descriptions,
    function_call="auto",  # specify the function call
)

# It automatically fills the arguments with correct info based on the prompt
# Note: the function does not exist yet

output = completion.choices[0].message
print(output)

# --------------------------------------------------------------
# Add a Function
# --------------------------------------------------------------


def get_law_info(loc_law, loc_question):
    """Get the legal context information"""

    # Example output returned from an API or database
    law_info = {
        "law": law,
        "question": question,
    }

    return json.dumps(law_info)

# Use the LLM output to manually call the function
# The json.loads function converts the string to a Python object

law = json.loads(output.function_call.arguments).get("law")
question = json.loads(output.function_call.arguments).get("question")
params = json.loads(output.function_call.arguments)
type(params)

print(law)
print(question)
print(params)

# Call the function with arguments

chosenlaw_info = eval(output.function_call.name)
law_info = chosenlaw_info(**params)

print(law_info)

# --------------------------------------------------------------
# Add function result to the prompt for a final answer
# --------------------------------------------------------------

# The key is to add the function output back to the messages with role: function
second_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": user_prompt},
        {"role": "function", "name": output.function_call.name, "content": law_info},
    ],
    functions=function_descriptions,
)
response = second_completion.choices[0].message.content
print(response)law_infolaw_infodef ask_and_reply(prompt):
    """Give LLM a given prompt and get an answer."""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": prompt}],
        # add function calling
        functions=function_descriptions_multiple,
        function_call="auto",  # specify the function call
    )

    output = completion.choices[0].message
    return output


# Scenario 1: Check flight details

user_prompt = "When's the next flight from Amsterdam to New York?"
print(ask_and_reply(user_prompt))

# Get info for the next prompt

law = json.loads(output.function_call.arguments).get("law")
question = json.loads(output.function_call.arguments).get("question")
chosen_function = eval(output.function_call.name)
output = chosenlaw_info(law, question)

print(law)
print(question)
print(output)

# --------------------------------------------------------------
# Make It Conversational With Langchain
# --------------------------------------------------------------

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)

# Start a conversation with multiple requests

user_prompt = """
Eu fui demitido após 1 ano de trabalho sem justa causa, o que posso fazer?
"""

# Returns the function of the first request

first_response = llm.predict_messages(
    [HumanMessage(content=user_prompt)], functions=function_descriptions_multiple
)

print(first_response)
