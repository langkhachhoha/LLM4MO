import http.client
import json
from openai import OpenAI


class InterfaceAPI:
    def __init__(self, api_key, model_LLM="gpt-3.5-turbo", debug_mode=False, temperature=0.7):
        self.api_key = api_key
        self.model_LLM = model_LLM
        self.temperature = temperature
        self.debug_mode = debug_mode
        self.n_trial = 5

    def get_response(self, prompt_content):
        response = None
        n_trial = 0
        client = OpenAI(api_key=self.api_key)   

        while n_trial < self.n_trial:
            try:
                completion = client.chat.completions.create(
                    model=self.model_LLM,
                    messages=[
                        {"role": "system", "content": "You are an expert in the domain of optimization heuristics helping to design heuristics that can effectively solve optimization problems."},
                        {"role": "user", "content": prompt_content}
                    ],
                    temperature=self.temperature
                )
                response = completion.choices[0].message.content
                break
            except Exception as e:
                n_trial += 1
                if self.debug_mode:
                    print(f"Error in API. Restarting the process... Trial {n_trial}")
                    print("Error message:", str(e))
                continue

        return response
