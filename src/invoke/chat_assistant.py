from openai import AzureOpenAI
from typing import List, Dict
from config import config  # your Config class

# Initialize Azure OpenAI Client
client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.OPENAI_API_VERSION,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    azure_deployment=config.AZURE_OPENAI_DEPLOYMENT_NAME
)

SYSTEM_PROMPT = """You are a helpful assistant. You can generate a report by appending new user content to your system prompt context."""


def chat_with_gpt(user_prompt: str, history: List[Dict[str, str]] = None) -> str:
    """
    Sends the user prompt to Azure OpenAI and returns the response.

    Args:
        user_prompt (str): The user question or content to add.
        history (List[Dict[str, str]]): Optional conversation history.

    Returns:
        str: Response from ChatGPT.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=config.AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()


def chat_with_files(user_prompt: str, files: List[str], history: List[Dict[str, str]] = None) -> str:
    """
    Chat with GPT using user prompt and raw file contents.

    Args:
        user_prompt (str): The question or instruction for GPT.
        files (List[str]): List of raw file content strings.
        history (List[Dict[str, str]]): Optional chat history.

    Returns:
        str: Response from GPT.
    """
    file_context = "\n\n".join(files)
    system_prompt = f"{SYSTEM_PROMPT}\n\nHere is the relevant code context:\n{file_context}"

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=config.AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    prompt = "Summarize the importance of Pydantic settings in Python apps."
    answer = chat_with_gpt(prompt)
    print("ChatGPT:", answer)
