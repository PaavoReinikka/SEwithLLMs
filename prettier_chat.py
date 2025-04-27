import dotenv
import os
from openai import OpenAI
from openai import OpenAIError
from rich.console import Console
from rich.panel import Panel

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
        self.console = Console()

    def prompt(self, message):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message},
            ]
        )        
        return response.choices[0].message.content

    def chat(self):
        self.console.print(Panel(
            "Welcome to the [bold cyan]Mistral-7B-Instruct Chatbot[/bold cyan]\n"
            "This is a simple chatbot powered by the Mistral-7B-Instruct model.\n"
            "You can ask it [bold]anything[/bold], and it will try to respond.\n\n"
            "[bold yellow]Type 'exit' to end the chat.[/bold yellow]",
            title="Chatbot Introduction",
            style="bold blue",
        ))

        while True:
            user_input = self.console.input("[bold cyan]You:[/bold cyan] ")
            if user_input.lower() == "exit":
                break
            try:
                response = self.prompt(user_input)
                self.console.print(Panel(f"[bold green]Response:[/bold green] {response}"))
            except OpenAIError as e:
                self.console.print(Panel(f"[bold red]Error:[/bold red] {e}", style="bold red"))
                break    

        self.console.print(Panel(
            "You typed exit. [bold red]Goodbye![/bold red]",
            title="Session Ended",
            style="bold magenta"
        ))


if __name__ == "__main__":
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    chatbot = ChatBot(model=model, client=client)
    chatbot.chat()