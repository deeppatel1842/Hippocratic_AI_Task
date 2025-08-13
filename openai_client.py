import os
import openai
from dotenv import load_dotenv
from config_loader import config

class OpenAIClient:
    
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_settings = config.get_openai_settings()
    
    def call_model(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """ OpenAI API calls using configuration defaults """
        # Use config defaults if not specified
        if max_tokens is None:
            max_tokens = self.openai_settings["max_tokens"]
        if temperature is None:
            temperature = self.openai_settings["temperature"]
            
        resp = openai.ChatCompletion.create(
            model=self.openai_settings["model"],
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message["content"]
