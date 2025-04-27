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
        self.total_tokens = 0  # Tracks the total token usage

    def prompt(self, message):
        # Add the user's message to the conversation history
        self.messages.append({"role": "user", "content": message})

        # Send the conversation history to the model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        # Extract the model's response and token usage
        model_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": model_response})
        self.total_tokens += response.usage.total_tokens  # Update token count

        return model_response

    def chat(self):
        printmd("""
        [bold blue]Welcome to the Advanced Mistral-7B-Instruct Chatbot[/bold blue]
        This chatbot keeps track of the conversation history and token usage.
        You can ask it [bold]anything[/bold], and it will try to respond.
        Type 'exit' to end the chat.\n
        """)

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            try:
                response = self.prompt(user_input)
                printmd(f"\n[bold green]Response:[/bold green] {response}\n")
                printmd(f"[bold yellow]Total Tokens Used:[/bold yellow] {self.total_tokens}\n")
            except OpenAIError as e:
                printmd(f"[bold red]Error:[/bold red] {e}")

        printmd("\n[bold red]Goodbye![/bold red]\n")
        printmd(f"[bold yellow]Final Token Count:[/bold yellow] {self.total_tokens}")


if __name__ == "__main__":
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    chatbot = ChatBot(model=model, client=client)
    chatbot.chat()