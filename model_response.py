import os
from typing import Dict, Any

from loguru import logger
from openai import OpenAI


class ModelResponse:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def call_model(self, system_prompt: str, user_prompt: str, model: str="gpt-4o", out_structure=None) -> str:
        if not out_structure:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=out_structure
        )
        if response.choices[0].message.parsed:
            logger.debug(f"ModelOutput: {response.choices[0].message}")
            return response.choices[0].message.parsed
        return None

    def render_prompt(self, template: Dict[str, Any], **kwargs) -> str:
        return template["prompt"].format(**kwargs)
