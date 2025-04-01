# pdf_extractor/extractors/gemini_extractor.py
from pathlib import Path
from google import genai
import PIL.Image
from .base import BaseExtractor


class GeminiExtractor(BaseExtractor):
    def initialize_client(self):
        self.client = genai.Client(api_key=self.api_key)

    def extract_text_from_image(self, image_path: Path) -> str:
        pil_image = PIL.Image.open(image_path)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Extract and return ONLY the text from this image. Format it exactly as it appears.",
                pil_image,
            ],
        )
        return response.text
