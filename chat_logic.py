from openai import OpenAI


class LLMService:
    """handles logic of communicating with the LLM"""
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        # if using
        # self.client = OpenAI() 

    def get_response(self, messages: list, stream=True):
        try:
            return self.client.chat.completions.create(
                # model="gemini-3-flash-preview",
                model="openai/gpt-oss-20b",
                messages=messages,
                temperature=0.7,
                seed=42,
                stream=stream,
                max_tokens=300,
            )
        except Exception as e:
            print(f"connection error: {e}")
            return None


class ConversationManager:
    """handles memory for the chatbot"""
    def __init__(self, system_prompt: str, max_history=3):
        self.history = [{"role": "system", "content": system_prompt}]
        self.max_history = max_history

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        print(len(self.history))
        if len(self.history) > self.max_history + 1:
            system_prompt = self.history[0]
            recent_conversation = self.history[-(self.max_history):]
            self.history = [system_prompt] + recent_conversation
        print(self.history)

    def get_history(self):
        """ if it is needed for production to trim or analyze"""
        return self.history
