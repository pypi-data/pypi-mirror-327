# pdf_extractor/extractors/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseExtractor(ABC):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    @abstractmethod
    def extract_text_from_image(self, image_path: Path) -> str:
        """Extract text from a single image"""
        pass

    @abstractmethod
    def initialize_client(self):
        """Initialize the AI client"""
        pass
