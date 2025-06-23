from app.services.llm_service import LLMService

def generate_summary(content: str, max_length: int = 100) -> str:
    llm_service = LLMService()

    system_prompt = "You are a helpful assistant specialized in creating concise summaries."
    user_prompt = f"Create a concise summary (maximum {max_length} characters) of the following text:\n\n{content}"

    return llm_service.generate_summary(system_prompt, user_prompt)