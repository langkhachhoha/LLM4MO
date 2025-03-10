import time
from typing import Optional
import time
import logging
import concurrent
from random import random
from tqdm import tqdm


logger = logging.getLogger(__name__)

class BaseClient(object):
    def __init__(
        self,
        model: str,
        temperature: float = 1.0,
    ) -> None:
        self.model = model
        self.temperature = temperature
    
    def _chat_completion_api(self, messages: list[dict], temperature: float, n: int = 1):
        raise NotImplemented
    
    def chat_completion(self, n: int, messages: list[dict], temperature: Optional[float] = None) -> list[dict]:
        """
        Generate n responses using OpenAI Chat Completions API
        """
        temperature = temperature or self.temperature
        time.sleep(random())
        for attempt in range(10):
            try:
                response_cur = self._chat_completion_api(messages, temperature, n)
            except Exception as e:
                logger.exception(e)
                logger.info(f"Attempt {attempt+1} failed with error: {e}")
                logger.info("Retrying in 60 seconds...")
                time.sleep(65)
            else:
                break
        if response_cur is None:
            logger.info("Code terminated due to too many failed attempts!")
            exit()
            
        return response_cur
    
    def multi_chat_completion(self, messages_list: list[list[dict]], n: int = 1, temperature: Optional[float] = None, lite = False):
        """
        An example of messages_list:
        
        messages_list = [
            [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
            [
                {"role": "system", "content": "You are a knowledgeable guide."},
                {"role": "user", "content": "How are you?"},
            ],
            [
                {"role": "system", "content": "You are a witty comedian."},
                {"role": "user", "content": "Tell me a joke."},
            ]
        ]
        param: n: number of responses to generate for each message in messages_list
        """
        if lite:
        # If messages_list is not a list of list (i.e., only one conversation), convert it to a list of list
            assert isinstance(messages_list, list), "messages_list should be a list."
            if not isinstance(messages_list[0], list):
                messages_list = [messages_list]
            
            if len(messages_list) > 1:
                assert n == 1, "Currently, only n=1 is supported for multi-chat completion."
            if "gpt" not in self.model:
                # Transform messages if n > 1
                messages_list *= n
                n = 1

            with concurrent.futures.ThreadPoolExecutor() as executor:
                args = [dict(n=n, messages=messages, temperature=temperature) for messages in messages_list]
                choices = executor.map(lambda p: self.chat_completion(**p), args)

            contents: list[str] = []
            for choice in choices:
                for c in choice:
                    contents.append(c.message.content)
            return contents
        else:
            assert isinstance(messages_list, list), "messages_list should be a list."
            if not isinstance(messages_list[0], list):
                messages_list = [messages_list]
            if len(messages_list) > 1:
                assert n == 1, "Currently, only n=1 is supported for multi-chat completion."
            if "gpt" not in self.model:
                messages_list *= n
                n = 1
            args = [dict(n=n, messages=messages, temperature=temperature) for messages in messages_list]
            contents: list[str] = []
            batch_size = 10
            for i in tqdm(range(0, len(args), batch_size), desc="Batch Progress"):
                batch_args = args[i:i+batch_size]
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    batch_choices = executor.map(lambda p: self.chat_completion(**p), batch_args)
                for choice in batch_choices:
                    for c in choice:
                        contents.append(c.message.content)
                if i + batch_size < len(args):
                    print("\033[5m\033[31m🌡️ Overheat\033[0m")
                    for remaining in range(30, 0, -1):
                        print(f"❄️❄️ Cooling down: Waiting {remaining} seconds...", end='\r')
                        time.sleep(1)
                    print(" " * 30, end='\r')
            return contents