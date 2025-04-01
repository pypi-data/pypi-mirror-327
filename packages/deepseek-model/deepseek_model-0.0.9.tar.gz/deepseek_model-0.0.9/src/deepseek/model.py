"""Model file"""

import os
from typing import List, Dict
from together import Together
from together.types import ChatCompletionChunk

from .helper import prompt_preview, search_file_type, strip_thinking


def get_question_structure(question: str) -> List[Dict[str, str]]:
    """Compose question structure"""
    return [
        {
            "role": "user",
            "content": question,
        }
    ]


def structure_file_to_conversation(
    module: str, extension_name: str, folder_location: str = "."
):
    """Structure file types"""
    conversation = []
    for filename in search_file_type(folder_location, extension_name):
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            if content != "":
                conversation.extend(
                    [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Module: {module}; Filename: {filename}",
                                }
                            ],
                        },
                        {
                            "role": "assistant",
                            "content": [{"type": "text", "text": content}],
                        },
                    ]
                )
    return conversation


def interact(
    question: str,
):
    """Call Claude API"""
    model = "deepseek-ai/DeepSeek-R1"
    client = Together()

    if os.environ.get("DEBUG"):
        prompt_preview(question)

    messages = []

    if question == "":
        raise ValueError("Nothing to ask")

    messages = [
        {
            "role": "user",
            "content": question,
        }
    ]

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    full_response = ""
    usage = None

    for chunk in stream:
        if not isinstance(chunk, ChatCompletionChunk):
            raise ValueError("Unexpected chunk type")

        if isinstance(chunk.choices, List):
            if len(chunk.choices) != 0:
                if chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        print(content, end="", flush=True)

        if chunk.usage:
            usage = chunk.usage

    with os.fdopen(3, "w") as fd3:
        fd3.write(strip_thinking(full_response))

    if usage:
        print("\n\nUsage: " + usage.model_dump_json())
