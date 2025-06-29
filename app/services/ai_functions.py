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


async def generate_summary(content: str, max_length: int = 150) -> str:
    system_prompt = (
        "You are a helpful assistant specialized in creating concise summaries. "
        "Focus on the main points and key information from the content. "
        "The content may include Notion-specific formatting such as headings, toggle lists, "
        "callout blocks, tables, and other structured elements. "
        "Extract the essential information while preserving the original meaning, "
        "regardless of the formatting structure."
    )
    user_prompt = f"Create a concise summary (maximum {max_length} characters) of the following text which may contain Notion formatting:\n\n{content}"

    llm_service = await get_llm_service()
    try:
        return await llm_service.generate_response(system_prompt, user_prompt, max_tokens=200)
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return "Summary generation failed"

async def generate_title_and_category(content: str, max_length: int = 50) -> tuple[str, str]:
    system_prompt = (
        "You are a helpful assistant specialized in generating titles and categorizing content. "
        "For titles: Create a concise, descriptive title that captures the essence of the content. "
        "For categories: Choose from common categories like: Work, Personal, Study, Ideas, Tasks, "
        "Meeting Notes, Research, or create a relevant single-word category."
        "Your response should be strictly formatted ONLY and DIRECT just as: \n1. Title:\n2. Category:\n\n"
        "Example 1: \n1. Title: Project Update\n2. Category: Work\n"
        "Example 2: \n1. Title: Grocery List\n2. Category: Personal\n"
        "Do not include any additional text or explanations, just the title and category. YOU DONT HAVE TO ADD nothing like \'Here is your response:\' or something like that.\n\n"
    )
    user_prompt = f"For the following content:\n\n{content}\n\nProvide:\n1. A concise title (max {max_length} characters)\n2. A single category word or phrase"

    llm_service = await get_llm_service()
    try:
        response = await llm_service.generate_response(system_prompt, user_prompt, max_tokens=100)
        parts = response.split("\n")
        title = parts[0].replace("1. Title:", "").strip() if len(parts) > 0 else "Untitled"
        category = parts[1].replace("2. Category:", "").strip() if len(parts) > 1 else "General"
        return title, category
    except Exception as e:
        print(f"Title and category generation failed: {e}")
        return "Untitled", "General"


# async def generate_summary_and_category(content: str) -> tuple[str, str]:
#     if not content or len(content.strip()) < 10:
#         return "Content too short for processing", "General"
#
#     try:
#         summary_task = generate_summary(content)
#         category_task = generate_category(content)
#
#         summary, category = await asyncio.gather(summary_task, category_task)
#
#         summary = summary[:500] if summary else "No summary available"
#         category = category[:50] if category else "General"
#
#         return summary, category
#     except Exception as e:
#         print(f"Error generating summary and category: {e}")
#         return "Error generating summary", "General"

async def enhance_note_for_notion(content: str) -> str:
    system_prompt = (
        "You are a specialized note enhancement assistant that transforms raw notes into well-structured Notion-ready content. "
        "Your expertise includes:\n"
        "1. Preserving the original meaning while improving clarity and readability\n"
        "2. Organizing information with appropriate Notion formatting elements\n"
        "3. Adding proper heading hierarchy (H1, H2, H3) where appropriate\n"
        "4. Converting bullet points into toggle lists when containing sub-items\n"
        "5. Creating callout blocks for important information\n"
        "6. Adding tables for structured data when appropriate\n"
        "7. Suggesting tags/properties based on content\n"
        "8. Breaking walls of text into scannable sections\n\n"
        "Maintain the user's original intent and voice while enhancing structure and readability. "
        "Focus on creating a note that is both well-organized and visually appealing in Notion."
        "Use actual line breaks, not \\n characters in your response."
    )

    user_prompt = f"Enhance and structure the following note for Notion, maintaining its original meaning but improving organization and readability:\n\n{content}"

    llm_service = await get_llm_service()
    try:
        response = await llm_service.generate_response(system_prompt, user_prompt, max_tokens=1000)
        return response
    except Exception as e:
        print(f"Enhance failed: {e}")
        return content