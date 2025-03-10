import logging
from typing import Optional
from .base import BaseClient
from litellm import completion
import os
import yaml
ROOT_DIR = os.getcwd()

config_file = "/home/ihbkaiser/reevo/cfg/llm_client/gemini.yaml"
with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
os.environ["GEMINI_API_KEY"] = config.get("api_key", None)


logger = logging.getLogger(__name__)

class GeminiClient(BaseClient):
    def __init__(
        self,
        model: str,
        temperature: float = 1.0,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(model, temperature)
        
        
        self.model = model
        self.temperature = temperature
    
    def _chat_completion_api(self, messages: list[dict], temperature: float, n: int = 1):
        response_cur = completion(model=self.model, messages=messages, temperature=temperature, n=n)
        return response_cur.choices
