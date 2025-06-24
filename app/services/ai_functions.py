import asyncio

from app.services.llm_service import LLMService

llm_service = LLMService()

async def generate_summary(content: str, max_length: int = 100) -> str:

    system_prompt = "You are a helpful assistant specialized in creating concise summaries."
    user_prompt = f"Create a concise summary (maximum {max_length} characters) of the following text:\n\n{content}"

    return await llm_service.generate_response(system_prompt, user_prompt)

async def generate_category(content: str, max_length: int = 50) -> str:


    system_prompt = "You are a helpful assistant specialized in categorizing content."
    user_prompt = f"Categorize the following content into a single category (maximum {max_length} characters):\n\n{content}"

    return await llm_service.generate_response(system_prompt, user_prompt)


async def generate_summary_and_category(content: str) -> tuple[str, str]:
    summary_task = generate_summary(content)
    category_task = generate_category(content)

    summary, category = await asyncio.gather(summary_task, category_task)

    return summary, category
