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

class ChatBot:
    def __init__(self, model, client):
        self.model = model
        self.client = client
    
    def print_welcome_message(self):
        printmd("""
        [bold blue]Welcome to streaming Chatbot[/bold blue]
        You can ask the bot [bold]anything[/bold], and it will try to respond.
        Type 'exit' to end the chat.\n""")

    def prompt(self, message):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message},
            ],
            stream=True
        )
        printmd("\n[bold green]Response:[/bold green]", end="", flush=True)    
        for message in response:
            printmd(message.choices[0].delta.content, end="", flush=True)
        printmd("\n")

    def chat(self):

        self.print_welcome_message()
        while True:
            printmd("[bold cyan]You:[/bold cyan]", end=" ")
            user_input = input()
            if user_input.lower() == "exit":
                break
            try:
                self.prompt(user_input)
            except KeyboardInterrupt:
                printmd("\n[bold red]KeyboardInterrupt:[/bold red] Exiting the chat.")
                break
            except OpenAIError as e:
                printmd(f"[bold red]Error:[/bold red] {e}")
                break

        printmd("\nYou typed exit, [bold red]Goodbye![/bold red]\n")


if __name__ == "__main__":
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    chatbot = ChatBot(model=model, client=client)
    chatbot.chat()
    