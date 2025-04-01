"""
initializer.py - Script to initialize the pre-commit setup.

This script imports and executes `install_precommit` and `create_config_files` 
to ensure that pre-commit is installed and configuration files are created.

Usage:
    python initializer.py

Author: petudeveloper
Version: 0.1.0
"""

from pygoodpractices.config_generator import create_config_files
from pygoodpractices.installer import install_precommit


def initialize_pygoodpractices():
    """
    Initializes the pre-commit setup.

    This function:
    - Installs `pre-commit` if not already installed.
    - Generates necessary configuration files.

    :side effects:
        - Installs pre-commit using pip.
        - Creates configuration files in the project directory.
        - Prints messages indicating progress and success.

    :example:
        >>> initialize_pygoodpractices()
        ✅ Pre-commit installed successfully.
        ✅ Configuration files created.
    """
    install_precommit()
    create_config_files()


if __name__ == "__main__":
    initialize_pygoodpractices()
