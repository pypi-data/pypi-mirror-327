from typing import Dict, Any


def parse_markdown_to_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        content = file.read()

    parts = content.split('\n', 1)
    title = parts[0].lstrip('# ').strip()
    body = parts[1].strip() if len(parts) > 1 else ""

    return {
        "title": title,
        "content": body
    }