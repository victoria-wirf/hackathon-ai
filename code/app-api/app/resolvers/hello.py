import strawberry
import logging
from .. import types
from ..auth import IsAuthenticated, IsAdmin
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

def get_ai_response(prompt: str) -> str:
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable is not set")
            return "Error: API key not configured"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error getting AI response: {str(e)}")
        return f"Error generating AI response: {str(e)}"

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def hello(self) -> types.Message:
        return types.Message(message="Welcome to Cillers, Vicky!")

    @strawberry.field(permission_classes=[IsAuthenticated])
    def hello2(self) -> types.Message:
        prompt = "Generate a creative welcome message for a user named Vicky"
        ai_response = get_ai_response(prompt)
        return types.Message(message=ai_response)

    @strawberry.field(permission_classes=[IsAdmin])
    def hello_admin(self) -> types.Message:
        return types.Message(message="Welcome to Cillers! You are an admin.")

