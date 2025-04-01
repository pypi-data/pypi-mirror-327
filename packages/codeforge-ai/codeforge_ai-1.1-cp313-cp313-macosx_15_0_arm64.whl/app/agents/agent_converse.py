import os
import base64
from typing import List, Tuple, Union, Dict, Any, Iterator
import json

import botocore
import tiktoken
from langchain_aws import ChatBedrockConverse
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from pydantic import BaseModel, Field
from app.utils.file_util import process_attachments
from app.agents.prompts import template
from app.utils.logging_utils import logger
from app.utils.print_tree_util import print_file_tree


# Convert chat history from tuples to standardized message format
def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List[Union[HumanMessage, AIMessage]]:
    logger.info("Formatting chat history")
    buffer = []
    for human, ai in chat_history:
        # Convert each message pair into structured message objects
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


# Process and format images for AI model consumption
# Input: List of dictionaries containing image data
# Output: List of formatted image objects ready for model input
def process_images(images: list) -> List[Dict[str, Any]]:
    """Process base64 image into the format expected by Claude"""

    formatted_image_list = []

    for image in images:
        formatted_image_list.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image["fileType"],
                "data": image["content"]
            }
        })
    return formatted_image_list


# Configure AWS credentials
# First try to use specified profile, otherwise fall back to default credentials
# This allows for flexible deployment environments
aws_profile = os.environ.get("CODEFORGEAI_AWS_PROFILE")
if aws_profile:
    logger.info(f"Using AWS Profile: {aws_profile}")
else:
    logger.info("No AWS profile specified, using default credentials")

# Model selection configuration
# Maps friendly names to actual model identifiers
model_id = {
    "sonnet3.5": "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    "sonnet3.5-v2": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "opus": "us.anthropic.claude-3-opus-20240229-v1:0",
    "sonnet": "us.anthropic.claude-3-sonnet-20240229-v1:0",
    "haiku": "us.anthropic.claude-3-haiku-20240307-v1:0",
}[os.environ.get("CODEFORGEAI_AWS_MODEL", "sonnet3.5-v2")]
logger.info(f"Using Claude Model: {model_id}")


# Create an instance of the AI model with streaming capability
# Optional callback handler for processing streaming responses
def create_streaming_model(streaming_callback: BaseCallbackHandler = None):
    return ChatBedrockConverse(
        model=model_id,
        temperature=0.1,
        max_tokens=4096,
        top_p=0,
        callbacks=[streaming_callback] if streaming_callback else None,
        credentials_profile_name=aws_profile if aws_profile else None,
        config=botocore.config.Config(read_timeout=900)
    )


# Combine multiple source code files into a single string
# Includes file paths and contents
# Also calculates and displays token usage statistics
def get_combined_docs_from_files(files: List[str]) -> str:
    combined_contents: str = ""
    print_file_tree(files)
    user_codebase_dir: str = os.environ["CODEFORGEAI_USER_CODEBASE_DIR"]
    for file_path in files:
        try:
            full_file_path = os.path.join(user_codebase_dir, file_path)
            docs = TextLoader(full_file_path).load()
            for doc in docs:
                combined_contents += f"File: {file_path}\n{doc.page_content}\n\n"
        except Exception as error:
            logger.error(f"Error processing file {file_path}: {str(error)}")
            logger.debug("Stack trace:", exc_info=True)

    token_count = len(tiktoken.get_encoding("cl100k_base").encode(combined_contents))
    print(f"Codebase token count: {token_count:,}")
    print(f"Max Claude Token limit: 200,000")
    print("--------------------------------------------------------")
    return combined_contents


# Combine codebase and additional attachments into a single context string
# Used to provide complete context to the AI model
def extract_codebase_and_attachments(attachments: List, codebase: str) -> str:
    attachment_content = process_attachments(attachments) if attachments else ""
    return f"CodeBase:{codebase}\n\n Attachments Documents:\n{attachment_content}"


# Process attachments and prepare them for AI model input
# Separates images from other file types and formats them appropriately
def enrich_prompt(attachments: list, codebase: str) -> Tuple:
    files = []
    images = []

    for attachment in attachments:
        fileType: str = attachment["fileType"]
        if fileType.startswith("image/"):
            images.append(attachment)
        else:
            files.append(attachment)

    formatted_image_list = process_images(images)
    codebase_and_attachments = extract_codebase_and_attachments(files, codebase)
    enriched_prompt = template.format(codebase_and_attachments=codebase_and_attachments)

    return formatted_image_list, enriched_prompt


# Extract and process chat-related data from the incoming request
# Returns formatted images and enriched prompt for model consumption
def extract_chat_data(request: Dict) -> Tuple:
    attachments: List = request["attachments"]
    codebase: str = get_combined_docs_from_files(request["config"].get("files", []))

    formatted_image_list, enriched_prompt = enrich_prompt(attachments, codebase)
    return formatted_image_list, enriched_prompt


# Main function to handle streaming responses from the AI model
# Processes input data, formats messages, and yields response tokens
# Supports both text-only and multimodal interactions
def stream_response(input_data: Dict[str, Any]) -> Iterator[str]:

    # Uncomment the following for easier debugging
    # set_verbose(True)

    llm = create_streaming_model()
    formatted_image_list, enriched_prompt = extract_chat_data(input_data)
    formatted_chat_history = _format_chat_history(input_data.get("chat_history", []))

    messages = [HumanMessage(content=enriched_prompt)]
    messages.extend(formatted_chat_history)
    messages.extend([
        HumanMessage(content=[{"type": "text", "text": input_data["question"]}] + formatted_image_list)
    ])

    for token in llm.stream(messages):
        if hasattr(token, 'content'):
            content = json.dumps({'content': token.content})
        else:
            content = json.dumps({'content': str(token)})
        yield f"data: {content}\n\n"


if __name__ == "__main__":
    # Example usage with streaming
    question = "How are you?"
    input_data = {
        "question": question,
        "chat_history": [],
        "attachments": [],
        "config": {"files": []}
    }

    # Stream text-only response
    print("Streaming text-only response:")
    for token in stream_response(input_data):
        print(token, end="", flush=True)
    print("\n")

    # Stream multimodal response
    print("Streaming multimodal response:")
    with open("sample_image.jpg", "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    input_data["image"] = Field(base64_image=base64_image)
    input_data["question"] = "What's in this image?"

    for token in stream_response(input_data):
        print(token, end="", flush=True)
    print("\n")
