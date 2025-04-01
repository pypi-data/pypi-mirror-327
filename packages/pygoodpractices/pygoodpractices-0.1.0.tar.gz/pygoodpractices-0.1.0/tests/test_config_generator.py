import os
import shutil
import tempfile

import pytest
from pygoodpractices.config_generator import create_config_files


# A fixture to create and clean up a temporary directory
@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    # Change to the temporary directory
    orig_dir = os.getcwd()
    os.chdir(temp_dir)
    yield temp_dir
    os.chdir(orig_dir)
    shutil.rmtree(temp_dir)


def test_create_config_files(temp_project_dir):
    """
    Test that the create_config_files function correctly creates the configuration files.
    """
    # Assume CONFIGS is defined in the module and contains the expected files.
    # Before running, ensure no config file exists.
    # Run the function to create config files.
    create_config_files()

    # List of expected configuration filenames
    expected_files = [
        ".pre-commit-config.yaml",
        ".flake8",
        "isort.cfg",
        "pyproject.toml",
    ]

    # Check that each expected file exists in the temporary directory.
    for filename in expected_files:
        assert os.path.exists(filename), f"{filename} was not created."
