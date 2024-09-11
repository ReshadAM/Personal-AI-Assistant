# Standard library imports
import os
import sys

# Third-party imports
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI

# Loading in the environment variables
load_dotenv()

# GPT API Config from a .env file 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class MyAI:

    """AI Chatbot class using OpenAI GPT models."""


    def __init__(self) -> None:
        pass
    
    # function that will access the OPEN AI model via API call 
    def chat_with_gpt(self, prompt) -> str:
        try:

            # Setting up the path for the traning data
            directory = "JUNE_TRAINING_DATA"
            file_path = os.path.join(directory, 'June_training_data.txt')
            file_exists = os.path.isfile(file_path)

            # checking if the traning model file exists
            if not file_exists:
                raise FileNotFoundError(f"Training data file not found: {file_path}")

            # Assigning the traning model to a variable to be fed to the API 
            with open(file_path, "r") as file:
                specialized_behavior = file.read()
            # Sending a messege to the OPEN AI and recording output 
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": specialized_behavior},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        
        except FileNotFoundError as fileNotFound:
            print(f"Error: {fileNotFound}")
            sys.exit(1)
            
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)