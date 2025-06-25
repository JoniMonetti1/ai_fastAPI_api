import os
from dotenv import load_dotenv
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()

class LLMService:
    def __init__(self):
        self.endpoint = "https://models.github.ai/inference"
        self.model = "meta/Llama-4-Scout-17B-16E-Instruct"
        self.token = os.environ["GITHUB_TOKEN"]
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )

    async def generate_response(self, system_prompt: str, user_prompt: str,
                         temperature: float = 0.7, top_p: float = 0.95,
                         max_tokens: int = 500) -> str:
        response = await self.client.complete(
            messages=[
                SystemMessage(system_prompt),
                UserMessage(user_prompt)
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            model=self.model
        )

        return response.choices[0].message.content.strip()

    async def close(self):
        await self.client.close()