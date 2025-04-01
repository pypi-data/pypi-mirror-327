import os
import subprocess
from app.utils.logging_utils import logger
import time
import re
from app.utils.backup_diff_patch import apply_patch_backup

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
        # need to add a newline at the end of the file or git apply will fail
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

    except subprocess.CalledProcessError as e:
        try:
            logger.error(f"Git apply failed with return code: {e.returncode}")
            logger.error(f"Git apply stderr: {e.stderr}")
            logger.info("Applying backup diff patch")
            apply_patch_backup(temp_file, user_codebase_dir)
        except Exception as e:
            logger.error(f"Error applying changes: {str(e)}", exc_info=True)
            raise

    finally:
        os.remove(temp_file)


def correct_git_diff(git_diff: str, original_file_path: str) -> str:
    git_diff_lines_array = git_diff.split('\n')
    local_code_lines_array = []
    is_new_file = False
    corrected_lines = []
    git_diff_line_index = 0
    cumulative_line_offset = 0

    if git_diff_lines_array:
        for git_diff_line in git_diff_lines_array:
            logger.info(f"checking line: {git_diff_line}")
            if HUNK_HEADER_REGEX.match(git_diff_line):
                logger.info("Hunk header found!")
                break

            if git_diff_line.startswith(('diff --git a/dev/null', '--- /dev/null')):
                is_new_file = True
                create_file_mode = any('new file mode 100' in line for line in git_diff_lines_array[:3])

                if not create_file_mode:
                    mode_line = 'new file mode 100644'
                    git_diff_lines_array.insert(1, mode_line)
                    logger.info(f"Added missing '{mode_line}' to new file diff")

                break

    if not is_new_file:
        try:
            with open(original_file_path, 'r') as f:
                local_code_lines_array = f.read().splitlines()
        except FileNotFoundError:
            error_msg = (
                f"File {original_file_path} not found and diff does not indicate new file creation. "
            )
            raise FileNotFoundError(error_msg)

    while git_diff_line_index < len(git_diff_lines_array):
        git_diff_line_item = git_diff_lines_array[git_diff_line_index]
        hunk_match = HUNK_HEADER_REGEX.match(git_diff_line_item)

        if hunk_match:
            corrected_hunk_header, hunk_lines, git_diff_line_index, line_offset = _process_diff_hunk_with_local_code(
                git_diff_lines_array, git_diff_line_index, cumulative_line_offset, local_code_lines_array
            )
            cumulative_line_offset += line_offset
            corrected_lines.append(corrected_hunk_header)
            corrected_lines.extend(hunk_lines)
        else:
            if git_diff_line_item.strip() == '':
                corrected_lines.append(' ')
            else:
                corrected_lines.append(git_diff_line_item)
            git_diff_line_index += 1
    corrected_diff = '\n'.join(corrected_lines)
    return corrected_diff


def _find_local_code_start_line(local_code_lines_array: list, diff_hunk_lines_array: list) -> int:
    if not local_code_lines_array:
        return 0

    if len(diff_hunk_lines_array) < 3:
        error_msg = (
                f"Invalid git diff format: Expected at least 2 lines in the hunk, but got {len(diff_hunk_lines_array)} lines.\n"
                + "Hunk content:\n{}".format('\n'.join(diff_hunk_lines_array)))
        logger.error(error_msg)
        raise RuntimeError("Invalid git diff format.")

    context_and_deleted = []
    for line in diff_hunk_lines_array:
        if line.startswith(' ') or line.startswith('-'):
            # Remove the prefix character
            context_and_deleted.append(line[1:])

    if not context_and_deleted:
        error_msg = (
            "Invalid git diff format: No context or deleted lines found in the hunk.\n"
            "Each hunk must contain at least one context line (starting with space) "
            "or deleted line (starting with '-').\n"
            "Hunk content:\n{}".format('\n'.join(diff_hunk_lines_array)))
        raise RuntimeError(error_msg)

    pattern_length = len(context_and_deleted)
    for i in range(len(local_code_lines_array) - pattern_length + 1):
        matches = True
        for j in range(pattern_length):
            if i + j >= len(local_code_lines_array):
                matches = False
                break
            if local_code_lines_array[i + j] != context_and_deleted[j]:
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


def _process_diff_hunk_with_local_code(git_diff_lines_array: list,
                                       start_index: int,
                                       cumulative_line_offset: int,
                                       local_code_lines_array: list):
    git_diff_line_index = start_index + 1
    lines_delete_count = 0
    lines_add_count = 0
    diff_hunk_lines_array = []
    while git_diff_line_index < len(git_diff_lines_array):
        hunk_line_item = git_diff_lines_array[git_diff_line_index]
        if HUNK_HEADER_REGEX.match(hunk_line_item):
            logger.info("New hunk header found while parsing the hunk, breaking this loop")
            break
        else:
            diff_hunk_lines_array.append(hunk_line_item)
            git_diff_line_index += 1
    if not diff_hunk_lines_array:
        raise ValueError("Empty hunk found in git diff")
    local_code_start_index = _find_local_code_start_line(local_code_lines_array, diff_hunk_lines_array)
    for hunk_line_item in diff_hunk_lines_array:
        if hunk_line_item.startswith('+') and not hunk_line_item.startswith('+++'):
            lines_add_count += 1
        elif hunk_line_item.startswith('-') and not hunk_line_item.startswith('---'):
            lines_delete_count += 1
        else:
            lines_delete_count += 1
            lines_add_count += 1

    if local_code_start_index == 0:
        lines_delete_count = 0
        corrected_start_line_new = 1
    else:
        corrected_start_line_new = local_code_start_index + cumulative_line_offset

    line_offset = lines_add_count - lines_delete_count

    corrected_hunk_header = _format_hunk_header(
        local_code_start_index, lines_delete_count, corrected_start_line_new, lines_add_count
    )

    return corrected_hunk_header, diff_hunk_lines_array, git_diff_line_index, line_offset


def _format_hunk_header(start_old: int, count_old: int, start_new: int, count_new: int) -> str:
    old_part = f'-{start_old}'
    if count_old != 1:
        old_part += f',{count_old}'
    new_part = f'+{start_new}'
    if count_new != 1:
        new_part += f',{count_new}'
    return f'@@ {old_part} {new_part} @@'
