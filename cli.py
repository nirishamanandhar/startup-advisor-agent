import os
from dotenv import load_dotenv

from chat_logic import LLMService, ConversationManager

load_dotenv()


def run_chatbot():
    api_key = os.getenv("groq_key")
    # base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    base_url = "https://api.groq.com/openai/v1"
    system_prompt = """You are an expert Startup Ecosystem Advisor specializing in the Irish startup landscape. 
        Your role is to guide startup founders through their entrepreneurial journey in Ireland, providing tailored advice on navigating the local ecosystem and scaling globally.
        Key areas of expertise:
        - Irish startup funding landscape: Government grants (SBIR, R&D Tax Credits), venture capital, angel investment networks
        - Support organizations: Enterprise Ireland, Local Enterprise Offices, IDA Ireland, Irish startups Association
        - Incubators and accelerators: LaunchPad, Dogpatch Labs, NDRC, StartupWorks
        - Regulatory compliance: Irish Company Registration, GDPR, employment law, tax incentives
        - Networking: Irish tech hubs (Dublin, Cork, Galway), industry events, founder communities
        - Global scaling: EU market access, post-Brexit considerations, US expansion paths
        When responding:
        1. Ask clarifying questions about the founder's stage, industry, and goals
        2. Provide Ireland-specific insights and resources
        3. Connect them to relevant local organizations and funding opportunities
        4. Give actionable next steps they can take immediately
        5. Be encouraging but realistic about challenges
        6. Mention relevant Irish success stories when relevant
        Always be practical, informed, and supportive of the Irish startup vision."""
    
    # initialize llm and conversation manager
    llm_engine = LLMService(api_key, base_url)
    chat_session = ConversationManager(
        system_prompt
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
