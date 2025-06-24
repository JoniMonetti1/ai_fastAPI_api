from app.services.llm_service import LLMService

llm_service = LLMService()

def generate_summary(content: str, max_length: int = 100) -> str:

    system_prompt = "You are a helpful assistant specialized in creating concise summaries."
    user_prompt = f"Create a concise summary (maximum {max_length} characters) of the following text:\n\n{content}"

    return llm_service.generate_response(system_prompt, user_prompt)

def generate_category(content: str, max_length: int = 50) -> str:


    system_prompt = "You are a helpful assistant specialized in categorizing content."
    user_prompt = f"Categorize the following content into a single category (maximum {max_length} characters):\n\n{content}"

    return llm_service.generate_response(system_prompt, user_prompt)
