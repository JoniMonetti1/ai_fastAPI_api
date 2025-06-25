import asyncio

from app.services.llm_service import LLMService

llm_service = None

async def get_llm_service():
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service

async def cleanup_llm_service():
    global llm_service
    if llm_service:
        await llm_service.close()
        llm_service = None

async def generate_summary(content: str, max_length: int = 100) -> str:
    system_prompt = (
        "You are a helpful assistant specialized in creating concise summaries. "
        "Focus on the main points and key information."
    )
    user_prompt = f"Create a concise summary (maximum {max_length} characters) of the following text:\n\n{content}"

    llm_service = await get_llm_service()
    try:
        return await llm_service.generate_response(system_prompt, user_prompt, max_tokens=150)
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return "Summary generation failed"


async def generate_category(content: str, max_length: int = 50) -> str:
    system_prompt = (
        "You are a helpful assistant specialized in categorizing content. "
        "Choose from common categories like: Work, Personal, Study, Ideas, Tasks, "
        "Meeting Notes, Research, or create a relevant single-word category."
    )
    user_prompt = f"Categorize the following content into a single category (maximum {max_length} characters):\n\n{content}"

    llm_service = await get_llm_service()
    try:
        return await llm_service.generate_response(system_prompt, user_prompt, max_tokens=50)
    except Exception as e:
        print(f"Category generation failed: {e}")
        return "General"


async def generate_summary_and_category(content: str) -> tuple[str, str]:
    if not content or len(content.strip()) < 10:
        return "Content too short for processing", "General"

    try:
        summary_task = generate_summary(content)
        category_task = generate_category(content)

        summary, category = await asyncio.gather(summary_task, category_task)

        summary = summary[:500] if summary else "No summary available"
        category = category[:50] if category else "General"

        return summary, category
    except Exception as e:
        print(f"Error generating summary and category: {e}")
        return "Error generating summary", "General"
