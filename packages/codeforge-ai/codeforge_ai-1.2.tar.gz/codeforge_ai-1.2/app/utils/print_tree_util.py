import os

def print_file_tree(file_paths):
    """
    Prints a hierarchical representation of the file structure based on the given file paths.
    This function takes a list of file paths, organizes them into a tree structure,
    and prints the directory hierarchy along with the files in each directory.
    Args:
        file_paths (list): A list of strings representing file paths.
    Returns:
        None
    Example:
        file_paths = [
            '/home/user/documents/file1.txt',
            '/home/user/documents/file2.txt',
            '/home/user/pictures/image1.jpg'
        ]
        print_file_tree(file_paths)
    """
    file_tree = {}
    for path in file_paths:
        dir_path, file_name = os.path.split(path)
        file_tree.setdefault(dir_path, []).append(file_name)

    sorted_dirs = sorted(file_tree.keys())
    for dir_path in sorted_dirs:
        file_tree[dir_path].sort()

    def print_dir(dir_path, indent):
        if dir_path in printed_dirs:
            return
        printed_dirs.add(dir_path)
        print(f"{indent}{os.path.basename(dir_path)}")
        files = file_tree[dir_path]
        if files:
            for i, file_name in enumerate(files, 1):
                prefix = "└── " if i == len(files) else "├── "
                print(f"{indent}    {prefix}{file_name}")
        else:
            print(f"{indent}    (empty)")
        subdirs = [subdir for subdir in sorted_dirs if subdir.startswith(dir_path + os.sep)]
        for subdir in subdirs:
            print_dir(subdir, indent + "    ")

    printed_dirs = set()
    for dir_path in sorted_dirs:
        print_dir(dir_path, "")