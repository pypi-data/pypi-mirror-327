# pdf_extractor/utils.py
from pathlib import Path
from pdf2image import convert_from_path
from typing import List, Optional, Type
from .extractors.base import BaseExtractor


def process_pdf(
    pdf_path: str, extractor: BaseExtractor, output_path: Optional[str] = None
) -> str:
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    extracted_text = []

    # Create temporary directory for images
    temp_dir = Path("temp_images")
    temp_dir.mkdir(exist_ok=True)

    try:
        for i, image in enumerate(images):
            temp_image_path = temp_dir / f"page_{i}.png"
            image.save(temp_image_path)

            try:
                text = extractor.extract_text_from_image(temp_image_path)
                extracted_text.append(f"--- Page {i+1} ---\n{text}\n")
            except Exception as e:
                print(f"Error processing page {i+1}: {e}")
            finally:
                temp_image_path.unlink(missing_ok=True)

    finally:
        temp_dir.rmdir()

    full_text = "\n".join(extracted_text)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    return full_text
