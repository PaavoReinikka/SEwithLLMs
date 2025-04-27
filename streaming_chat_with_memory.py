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
        self.messages = []  # Stores the conversation history
        self.total_tokens = 0
    
    def print_welcome_message(self):
        printmd("""
        [bold blue]Welcome to streaming Chatbot[/bold blue]
        You can ask the bot [bold]anything[/bold], and it will try to respond.
        Type 'exit' to end the chat.\n""")

    def prompt(self, message):
        # Add the user's message to the conversation history
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        content = ""
        printmd("\n[bold green]Response:[/bold green]", end="", flush=True)    
        for msg in response:
            content += msg.choices[0].delta.content
            self.total_tokens += 1 # stream response is one token
            printmd(msg.choices[0].delta.content, end="", flush=True)
        
        self.total_tokens += int(1.2 * len(message.split())) # Estimate tokens for user input
        self.messages.append({"role": "assistant", "content": content})
        printmd(f"\n\n[bold yellow]Total tokens used:[/bold yellow] {self.total_tokens}\n")

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
                printmd(f"[bold red]API error:[/bold red] {e}")
                break

        printmd("\nYou typed exit, [bold red]Goodbye![/bold red]\n")


if __name__ == "__main__":
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    chatbot = ChatBot(model=model, client=client)
    chatbot.chat()
    