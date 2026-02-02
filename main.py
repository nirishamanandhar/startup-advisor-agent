import os
from dotenv import load_dotenv

from chat_logic import LLMService, ConversationManager

load_dotenv()


def run_chatbot():
    api_key = os.getenv("groq_key")
    # base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    base_url = "https://api.groq.com/openai/v1"

    # initialize llm and conversation manager
    llm_engine = LLMService(api_key, base_url)
    chat_session = ConversationManager(
        "You are a startup ecosystem helper in Ireland."
        "Your task is to help startup founders navigate"
        "their journey to get relevant advice and support"
        "to succeed in Ireland and scale globally."
    )
    print("type 'exit' to stop the conversation")

    # chatbot interaction loop
    while True:
        user_text = input("\nYou: ")
        if user_text.lower() == "exit":
            break

        chat_session.add_message("user", user_text)
        response_stream = llm_engine.get_response(chat_session.get_history())

        full_reply = ""
        try:
            for chunk in response_stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    full_reply += content
                    print(content, end="", flush=True)

        except Exception as e:
            print(f"no response: {e}")
        chat_session.add_message("assistant", full_reply)


if __name__ == "__main__":
    run_chatbot()
