# pdf_extractor/cli.py
import click
from pathlib import Path
from dotenv import load_dotenv
import os
from .extractors import GeminiExtractor, OpenAIExtractor
from .utils import process_pdf
from .key_manager import KeyManager


@click.group()
def cli():
    """PDF Text Extractor CLI"""
    pass


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option(
    "--model",
    "-m",
    type=click.Choice(["gemini", "openai"]),
    default="gemini",
    help="AI model to use for text extraction",
)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--api-key", help="API key for the chosen model (optional if stored)")
def extract(pdf_path: str, model: str, output: str, api_key: str):
    """Extract text from PDF using AI models."""
    load_dotenv()

    # Try to get API key from different sources
    key_manager = KeyManager()
    if not api_key:
        api_key = key_manager.get_key(model)
        if not api_key:
            api_key = os.getenv(f"{model.upper()}_API_KEY")
            if not api_key:
                raise click.ClickException(
                    f"No API key found for {model}. Please provide it via --api-key option "
                    f"or store it using 'extract-pdf keys add {model} YOUR_KEY'"
                )

    # Select extractor based on model choice
    extractors = {"gemini": GeminiExtractor, "openai": OpenAIExtractor}

    extractor_class = extractors[model]
    extractor = extractor_class(api_key=api_key)
    extractor.initialize_client()

    # Process PDF
    output_path = output or Path(pdf_path).stem + "_extracted.txt"
    text = process_pdf(pdf_path, extractor, output_path)
    click.echo(f"Text extracted and saved to {output_path}")


@cli.group()
def keys():
    """Manage API keys"""
    pass


@keys.command()
@click.argument("model", type=click.Choice(["gemini", "openai"]))
@click.argument("api_key")
def add(model: str, api_key: str):
    """Store an API key for a model"""
    key_manager = KeyManager()
    key_manager.add_key(model, api_key)
    click.echo(f"API key for {model} stored successfully")


@keys.command()
@click.argument("model", type=click.Choice(["gemini", "openai"]))
def delete(model: str):
    """Delete stored API key for a model"""
    key_manager = KeyManager()
    key_manager.delete_key(model)
    click.echo(f"API key for {model} deleted")


@keys.command()
def list():
    """List all stored API keys (partial preview)"""
    key_manager = KeyManager()
    stored_keys = key_manager.list_keys()
    if not stored_keys:
        click.echo("No API keys stored")
        return

    click.echo("Stored API keys:")
    for model, preview in stored_keys.items():
        click.echo(f"{model}: {preview}")


def main():
    cli()


if __name__ == "__main__":
    main()
