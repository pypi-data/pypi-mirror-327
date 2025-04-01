import subprocess
import sys


def install_precommit():
    """
    Installs and sets up pre-commit hooks for the project.

    This function ensures that `pre-commit` is installed and then initializes it
    in the current repository by running the necessary setup commands.

    :raises RuntimeError: If the installation or initialization process fails.

    :side effects:
        - Installs `pre-commit` using `pip` if not already installed.
        - Runs `pre-commit install` to activate hooks.
        - Prints messages indicating success or failure.

    :example:
        >>> install_precommit()
        ✅ Pre-commit installed and initialized successfully.
    """
    python_executable = sys.executable
    try:
        # Check if pre-commit is installed
        subprocess.run(
            [python_executable, "-m", "pip", "install", "--quiet", "pre-commit"],
            check=True,
        )
        print("✅ Pre-commit installed successfully.")

        # Initialize pre-commit in the repository
        subprocess.run(["pre-commit", "install"], check=True)
        print("✅ Pre-commit hooks installed successfully.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Error installing or setting up pre-commit: {e}")


if __name__ == "__main__":
    install_precommit()
