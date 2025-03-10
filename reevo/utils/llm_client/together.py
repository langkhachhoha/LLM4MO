import logging
from typing import Optional
from .base import BaseClient
from together import Together
import yaml
import os

config_file = "/home/ihbkaiser/reevo/cfg/llm_client/together.yaml"
with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
os.environ["TOGETHER_API_KEY"] = config.get("api_key", None)


logger = logging.getLogger(__name__)

class TogetherClient(BaseClient):
    def __init__(
        self,
        model: str,
        temperature: float = 1.0,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(model, temperature)
        
        self.client = Together()
        self.model = model
        self.temperature = temperature
    
    def _chat_completion_api(self, messages: list[dict], temperature: float, n: int = 1):
        response_cur = self.client.chat.completions.create(model = self.model, messages = messages, 
                                                           temperature = temperature, n = n)
        return response_cur.choices
