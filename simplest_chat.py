import dotenv
import os
from openai import OpenAI
from openai import OpenAIError
from rich import print as printmd

# Load environment variables from .env file
dotenv.load_dotenv()
api_key = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

# Check if the API key is set
if not api_key:
    raise ValueError("HUGGINGFACE_ACCESS_TOKEN environment variable not set")

# Initialize the OpenAI API client
client = OpenAI(
    api_key=api_key,
    base_url="https://api-inference.huggingface.co/v1/",
)

# Define the model to use
model = "mistralai/Mistral-7B-Instruct-v0.3"

def prompt(message, verbose=False):
  response = client.chat.completions.create(
    model=model,
    messages=[
      {"role": "user", "content": message},
    ]
  )
  if verbose:
    printmd(response.choices[0].message.content)
    
  return response.choices[0].message.content


def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        try:
            response = prompt(user_input)
            printmd(f"Response: {response}\n")
        except OpenAIError as e:
            printmd(f"Error: {e}")

    printmd("\nYou typed exit, [bold red]Goodbye![/bold red]\n")

if __name__ == "__main__":
    printmd("""
    [bold blue]Welcome to the Mistral-7B-Instruct Chatbot[/bold blue]
    This is a simple chatbot powered by the Mistral-7B-Instruct model.
    You can ask it [bold]anything[/bold], and it will try to respond.
    Type 'exit' to end the chat.\n""")
    
    chat()