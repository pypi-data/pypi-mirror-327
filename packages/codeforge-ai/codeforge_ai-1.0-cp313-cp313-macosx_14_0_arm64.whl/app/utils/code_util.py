import os
import subprocess
from app.utils.logging_utils import logger
import time
import re

HUNK_HEADER_REGEX = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')

def use_git_to_apply_code_diff(git_diff: str):

    user_codebase_dir = os.environ.get("CODEFORGEAI_USER_CODEBASE_DIR")
    if not user_codebase_dir:
        raise ValueError("CODEFORGEAI_USER_CODEBASE_DIR environment variable is not set")

    # Create a temporary file with the diff content and a timestamp
    timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
    temp_file = os.path.join(user_codebase_dir, f'temp_{timestamp}.diff')

    with open(temp_file, 'w', newline='\n') as f:
        f.write(git_diff)
        # need to add a newline at the end of the file of git apply will fail
        f.write("\n")
    logger.info(f"Created temporary diff file: {temp_file}")

    try:
        # Apply the changes using git apply
        cmd = ['git', 'apply', '--verbose', '--ignore-whitespace', '--ignore-space-change', temp_file]
        logger.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=user_codebase_dir, check=True)

        logger.info(f"Git apply stdout: {result.stdout}")
        logger.error(f"Git apply stderr: {result.stderr}")
        logger.info(f"Git apply return code: {result.returncode}")

    except Exception as e:
        logger.error(f"Error applying changes: {str(e)}", exc_info=True)
        raise
    finally:
        os.remove(temp_file)

def correct_git_diff(git_diff: str, original_file_path: str) -> str:
    lines = git_diff.split('\n')
    is_new_file = False
    if lines and lines[0].startswith('diff --git a/dev/null'):
        is_new_file = True
        has_file_mode = any('new file mode 100' in line for line in lines[:3])
        if not has_file_mode:
            mode_line = 'new file mode 100644'
            lines.insert(1, mode_line)
            logger.info(f"Added missing '{mode_line}' to new file diff")

    original_content = []

    if not is_new_file:
        try:
            with open(original_file_path, 'r') as f:
                original_content = f.read().splitlines()
        except FileNotFoundError:
            error_msg = (
                f"File {original_file_path} not found and diff does not indicate new file creation. "
            )
            raise FileNotFoundError(error_msg)

    corrected_lines = []
    line_index = 0
    cumulative_line_offset = 0


    while line_index < len(lines):
        line = lines[line_index]
        hunk_match = HUNK_HEADER_REGEX.match(line)

        if hunk_match:
            corrected_hunk_header, hunk_lines, line_index, line_offset = _process_hunk_with_original_content(
                lines, line_index, cumulative_line_offset, original_content
            )
            cumulative_line_offset += line_offset
            corrected_lines.append(corrected_hunk_header)
            corrected_lines.extend(hunk_lines)
        else:
            corrected_lines.append(line)
            line_index += 1
    corrected_diff = '\n'.join(corrected_lines)
    return corrected_diff

def _find_correct_old_start_line(original_content: list, hunk_lines: list) -> int:
    if not original_content:
        return 0

    if len(hunk_lines) < 3:
        error_msg = (
            f"Invalid git diff format: Expected at least 2 lines in the hunk, but got {len(hunk_lines)} lines.\n"
            + "Hunk content:\n{}".format('\n'.join(hunk_lines)))
        logger.error(error_msg)
        raise RuntimeError("Invalid git diff format.")

    context_and_deleted = []
    for line in hunk_lines:
        if line.startswith(' ') or line.startswith('-'):
            # Remove the prefix character
            context_and_deleted.append(line[1:])

    if not context_and_deleted:
        error_msg = (
            "Invalid git diff format: No context or deleted lines found in the hunk.\n"
            "Each hunk must contain at least one context line (starting with space) "
            "or deleted line (starting with '-').\n"
            "Hunk content:\n{}".format('\n'.join(hunk_lines)))
        raise RuntimeError(error_msg)

    pattern_length = len(context_and_deleted)
    for i in range(len(original_content) - pattern_length + 1):
        matches = True
        for j in range(pattern_length):
            if j >= len(context_and_deleted):
                break
            if i + j >= len(original_content) or original_content[i + j] != context_and_deleted[j]:
                matches = False
                break
        if matches:
            return i + 1

    joined_context_and_deleted = '\n'.join(context_and_deleted)
    error_msg = (
        "Failed to locate the hunk position in the original file.\n"
        "This usually happens when the context lines in the diff don't match the original file content.\n"
        f"Context and deleted lines being searched:\n{joined_context_and_deleted}\n"
        "Please ensure the diff is generated against the correct version of the file."
    )
    logger.error(error_msg)
    raise RuntimeError(error_msg)

def _process_hunk_with_original_content(lines: list, start_index: int, cumulative_line_offset: int, original_content: list):

    line_index = start_index
    actual_count_old = 0
    actual_count_new = 0
    line_index += 1
    hunk_lines = []
    while line_index < len(lines):
        hunk_line = lines[line_index]
        if HUNK_HEADER_REGEX.match(hunk_line):
            break
        else:
            hunk_lines.append(hunk_line)
            line_index += 1
    start_line_old = _find_correct_old_start_line(original_content, hunk_lines)
    for hunk_line in hunk_lines:
        if hunk_line.startswith('+') and not hunk_line.startswith('+++'):
            actual_count_new += 1
        elif hunk_line.startswith('-') and not hunk_line.startswith('---'):
            actual_count_old += 1
        else:
            actual_count_old += 1
            actual_count_new += 1

    if start_line_old == 0:
        actual_count_old = 0
        corrected_start_line_new = 1
    else:
        corrected_start_line_new = start_line_old + cumulative_line_offset

    line_offset = actual_count_new - actual_count_old

    corrected_hunk_header = _format_hunk_header(
        start_line_old, actual_count_old, corrected_start_line_new, actual_count_new
    )

    return corrected_hunk_header, hunk_lines, line_index, line_offset

def _format_hunk_header(start_old: int, count_old: int, start_new: int, count_new: int) -> str:

    old_part = f'-{start_old}'
    if count_old != 1:
        old_part += f',{count_old}'
    new_part = f'+{start_new}'
    if count_new != 1:
        new_part += f',{count_new}'
    return f'@@ {old_part} {new_part} @@'
