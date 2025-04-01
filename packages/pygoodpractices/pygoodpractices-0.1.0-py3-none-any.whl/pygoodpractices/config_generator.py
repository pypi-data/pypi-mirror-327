import os

CONFIGS = {
    ".pre-commit-config.yaml": """\
default_language_version:
  python: python
repos:
-   repo: https://github.com/asottile/seed-isort-config
    rev: v1.9.3
    hooks:
    - id: seed-isort-config
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: v4.3.21
    hooks:
    - id: isort
-   repo: https://github.com/ambv/black
    rev: stable
    hooks:
    - id: black
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    - id: flake8
""",
    ".flake8": """\
[flake8]
max-line-length = 88
max-complexity = 18
select = B,C,E,F,W,T4,B9
ignore = E203, E266, E501, W503, F403, F401
""",
    "isort.cfg": """\
[settings]
line_length = 88
multi_line_output = 3
include_trailing_comma = True
known_third_party = celery,django,environ,pyquery,pytz,redis,requests,rest_framework
""",
    "pyproject.toml": """\
[tool.black]
line-length = 88
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
""",
}


def create_config_files():
    """
    Creates configuration files if they do not exist.

    This function iterates over the `CONFIGS` dictionary, where the keys are
    the filenames and the values are their respective contents. If a file does
    not exist, it creates the file and writes the corresponding content. If the
    file already exists, a message is displayed indicating that it was not overwritten.

    :global dict CONFIGS: A dictionary where keys are filenames and values are file contents.

    :side effects:
        - Creates files in the filesystem if they do not exist.
        - Prints messages to the console indicating whether files were created or already exist.

    :example:
        >>> CONFIGS = {".flake8": "[flake8]\\nmax-line-length = 88"}
        >>> create_config_files()
        ✅ File created: .flake8
    """

    for filename, content in CONFIGS.items():
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(content)
            print(f"✅ Archivo creado: {filename}")
        else:
            print(f"⚠️ Archivo ya existe: {filename}")


if __name__ == "__main__":
    create_config_files()
