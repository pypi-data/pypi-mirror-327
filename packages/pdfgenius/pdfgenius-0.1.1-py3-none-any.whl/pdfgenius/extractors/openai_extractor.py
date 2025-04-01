# pdf_extractor/extractors/openai_extractor.py
import base64
from pathlib import Path
from openai import OpenAI
from .base import BaseExtractor


class OpenAIExtractor(BaseExtractor):
    def initialize_client(self):
        self.client = OpenAI(api_key=self.api_key)

    def encode_image(self, image_path: Path) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def extract_text_from_image(self, image_path: Path) -> str:
        base64_image = self.encode_image(image_path)
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract and return ONLY the text from this image. Format it exactly as it appears.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
