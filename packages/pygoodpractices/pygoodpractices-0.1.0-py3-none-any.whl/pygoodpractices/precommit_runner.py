import argparse
import subprocess
import sys


def run_all_files():
    """
    Runs all pre-commit hooks on all files in the repository.
    """
    command = ["pre-commit", "run", "--all-files"]
    try:
        subprocess.run(command, check=True)
        print("✅ Hooks successfully executed on all files.")
    except subprocess.CalledProcessError as error:
        print("❌ Error executing 'pre-commit run --all-files':", error)
        sys.exit(error.returncode)


def run_specific_files(files):
    """
    Runs pre-commit hooks on specific files.

    :param files: List of filenames.
    """
    command = ["pre-commit", "run", "--files"] + files
    try:
        subprocess.run(command, check=True)
        print("✅ Hooks successfully executed on the specified files.")
    except subprocess.CalledProcessError as error:
        print("❌ Error executing 'pre-commit run --files' on specific files:", error)
        sys.exit(error.returncode)


def main():
    """
    Main function that parses command-line arguments and runs pre-commit hooks
    on all files or specific files.

    Usage:
      - To run on all files:
          precommit-runner --all
      - To run on specific files:
          precommit-runner --files file1.py file2.py
    """
    parser = argparse.ArgumentParser(
        description="Run pre-commit hooks on all files or specific files."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run hooks on all files.")
    group.add_argument("--files", nargs="+", help="Run hooks on the specified files.")

    args = parser.parse_args()

    if args.all:
        run_all_files()
    elif args.files:
        run_specific_files(args.files)


if __name__ == "__main__":
    main()
