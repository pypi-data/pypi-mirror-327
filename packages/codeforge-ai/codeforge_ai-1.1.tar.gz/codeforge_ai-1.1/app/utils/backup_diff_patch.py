import os
import re
from app.utils.logging_utils import logger


def apply_patch_backup(diff_file_path,  base_directory):
    """
    Applies a git patch manually, handling file creation, deletion, and edits.

    Args:
        diff_file_path (str): Path to the .diff file.
        base_directory (str): Base directory for file paths in the diff. Defaults to the current directory.

    Returns:
        bool: True if the patch was applied successfully, False otherwise.
    """
    try:
        # Read the .diff file
        with open(diff_file_path, 'r') as diff_file:
            diff_lines = diff_file.readlines()
            logger.info(f"Diff files contents: {diff_lines}")

        file_changes = []
        current_file = None
        current_hunks = []
        file_action = None

        # Parse the diff file for changes
        for line in diff_lines:
            if line.startswith("diff --git"):
                # Commit current file processing
                if current_file:
                    file_changes.append((file_action, current_file, current_hunks))
                # Extract file path
                match = re.search(r'a/([\w./-]+) b/([\w./-]+)', line)
                if match:
                    logger.info(f"Matched items: {match}")
                    current_file = match.group(2)
                    logger.info(f"current_file: {current_file}")
                    current_hunks = []
            elif line.startswith("---"):
                if " /dev/null" in line:
                    file_action = "create"
                else:
                    file_action = "edit"
            elif line.startswith("+++"):
                if " /dev/null" in line:
                    file_action = "delete"
            elif line.startswith("@@"):
                current_hunks.append({"header": line.strip(), "lines": []})
            elif current_hunks and (line.startswith("+") or line.startswith("-") or line.startswith(" ")):
                # todo: check if this is skipping empty lines that don't have spaces
                current_hunks[-1]["lines"].append(line)

        # Commit the last file
        if current_file:
            file_changes.append((file_action, current_file, current_hunks))

        # Apply changes
        for action, file_path, hunks in file_changes:
            full_path = os.path.join(base_directory, file_path)
            logger.info(f"Applying changes to full path - {full_path}")
            if action == "create":
                create_file(full_path, hunks)
            elif action == "delete":
                delete_file(full_path)
            elif action == "edit":
                edit_file(full_path, hunks)
            else:
                raise ValueError(f"Unknown action: {action}")

        logger.info("Patch applied successfully.")
        return True

    except Exception as e:
        logger.info(f"Failed to apply backup patch: {e}")
        return False


def create_file(file_path, hunks):
    """
    Creates a new file from the provided hunks.

    Args:
        file_path (str): Path of the new file.
        hunks (list): List of hunks containing file content.
    """
    logger.info(f"Creating new file: {file_path}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as new_file:
        for hunk in hunks:
            for line in hunk["lines"]:
                if line.startswith("+") or line.startswith(" "):
                    new_file.write(line[1:])


def delete_file(file_path):
    """
    Deletes the specified file.

    Args:
        file_path (str): Path of the file to delete.
    """
    logger.info(f"Deleting file: {file_path}")
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        logger.error(f"File not found: {file_path}")


# Todo: Improve this by starting search from the line number from the hunk header
def edit_file(file_path, hunks):
    """
    Edits an existing file based on the provided hunks.

    Args:
        file_path (str): Path of the file to edit.
        hunks (list): List of hunks containing the changes.
    """
    logger.info(f"Editing file: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        original_lines = file.readlines()

    patched_lines = original_lines[:]
    logger.info(f"patched_lines, {patched_lines}")
    line_offset = 0

    for hunk in hunks:
        header = hunk["header"]
        logger.info(f"header, {header}")
        match = re.match(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", header)
        logger.info(f"match, {match}")
        if not match:
            raise ValueError(f"Invalid hunk header: {header}")

        start_old = int(match.group(1)) - 1
        start_new = int(match.group(3)) - 1
        current_index = start_old + line_offset

        for line in hunk["lines"]:
            logger.info(f"Checking line: {line}")
            if line.startswith("-"):
                if patched_lines[current_index].strip() != line[1:].strip():
                    raise ValueError(
                        f"Context mismatch at line {current_index}: "
                        f"Expected {repr(patched_lines[current_index].strip())}, "
                        f"Got {repr(line[1:].strip())}"
                    )
                logger.info(f"deleting line - {line}")
                del patched_lines[current_index]
                logger.info(f"After deletion, current_index-{current_index}, patched_lines-{patched_lines}")
            elif line.startswith("+"):
                logger.info(f"adding line - {line}")
                patched_lines.insert(current_index, line[1:])
                current_index += 1
                line_offset += 1
                logger.info(f"After addition, current_index-{current_index}, patched_lines-{patched_lines}")
            elif line.startswith(" "):
                if patched_lines[current_index].strip() != line[1:].strip():
                    raise ValueError(
                        f"Context mismatch at line {current_index + 1}: "
                        f"Expected {repr(patched_lines[current_index].strip())}, "
                        f"Got {repr(line[1:].strip())}"
                    )
                current_index += 1
                logger.info(f"Context line, current_index-{current_index}, patched_lines-{patched_lines}")

    with open(file_path, 'w') as file:
        file.writelines(patched_lines)
