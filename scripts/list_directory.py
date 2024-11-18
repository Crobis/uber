from pathlib import Path

def list_directory(directory: Path, level: int = 0, exclude_dirs=None):
    """
    Recursively lists a directory's contents with indentation for subdirectories and files,
    excluding specified directories.

    Args:
        directory (Path): The directory to list.
        level (int): The current indentation level (default is 0).
        exclude_dirs (list): List of directory names to exclude.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    # Ensure the provided path is a directory
    if not directory.is_dir():
        print(f"{'  ' * level}[Error] {directory} is not a directory.")
        return

    # Print the current directory name
    print(f"{'  ' * level}{directory.name}/")

    # Iterate over directory contents
    for item in sorted(directory.iterdir()):
        if item.is_dir():
            if item.name in exclude_dirs:
                # Skip directories in the exclusion list
                print(f"{'  ' * (level + 1)}[Excluded] {item.name}/")
                continue
            # Recursively list subdirectory
            list_directory(item, level + 1, exclude_dirs)
        else:
            # Print files with padding
            print(f"{'  ' * (level + 1)}{item.name}")



excluded = ["CACHE", "node_modules", "old", "uploads"]
root_directory = Path("C:/work/gitprojects/uber")
list_directory(root_directory, exclude_dirs=excluded)