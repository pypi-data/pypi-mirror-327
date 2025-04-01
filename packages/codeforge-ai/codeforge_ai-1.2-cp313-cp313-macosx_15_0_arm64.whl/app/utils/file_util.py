from typing import List, Dict


def process_attachments(attachments: List[Dict[str, str]]) -> str:
    if not attachments:
        return ""
    processed_content = "Attached Files:\n\n"
    for attachment in attachments:
        processed_content += f"[File: {attachment['fileName']}]\n"
        processed_content += f"{attachment['content']}\n\n"

    return processed_content.strip()
