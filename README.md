# Aiogram Template

## Table of contents

Did you know that GitHub supports table of
contents [by default](https://github.blog/changelog/2021-04-13-table-of-contents-support-in-markdown-files/) 🤔

## About

This is the Telegram Bot.

### Technologies

- [Python 3.13](https://www.python.org/downloads/) & [UV](https://docs.astral.sh/uv)
- [Aiogram 3](https://docs.aiogram.dev/en/latest/) & [aiogram-dialog](https://aiogram-dialog.readthedocs.io/)
- Formatting and linting: [Ruff](https://docs.astral.sh/ruff/), [pre-commit](https://pre-commit.com/)
- Deployment: [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/),
  [GitHub Actions](https://github.com/features/actions)

## Development

### Getting started
1. Install [Python 3.13+](https://www.python.org/downloads/), [UV](https://docs.astral.sh/uv/getting-started/installation/),
   [Docker](https://docs.docker.com/engine/install/)
2. Install project dependencies with [UV](https://docs.astral.sh/uv/concepts/projects/sync/#syncing-the-environment).
   ```bash
   uv sync
   ```
3. Start development server:
   ```bash
   uv run -m src.bot
   ```
   > Follow provided instructions if needed

> [!TIP]
> Edit `settings.yaml` according to your needs, you can view schema in
> [config_schema.py](src/config_schema.py) and in [settings.schema.yaml](settings.schema.yaml)

**Set up PyCharm integrations**

1. Run configurations ([docs](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html#createExplicitly)).
   Right-click the `__main__.py` file in the project explorer, select `Run '__main__'` from the context menu.
2. Ruff ([plugin](https://plugins.jetbrains.com/plugin/20574-ruff)).
   It will lint and format your code. Make sure to enable `Use ruff format` option in plugin settings.
3. Pydantic ([plugin](https://plugins.jetbrains.com/plugin/12861-pydantic)). It will fix PyCharm issues with
   type-hinting.
4. Conventional commits ([plugin](https://plugins.jetbrains.com/plugin/13389-conventional-commit)). It will help you
   to write [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

### Deployment

We use Docker with Docker Compose plugin to run the service on servers.

1. Copy the file with settings: `cp settings.example.yaml settings.yaml`
2. Change settings in the `settings.yaml` file according to your needs
   (check [settings.schema.yaml](settings.schema.yaml) for more info)
3. Install Docker with Docker Compose
4. Build a Docker image: `docker compose build --pull`
5. Run the container: `docker compose up --detach`
6. Check the logs: `docker compose logs -f`

# How to update dependencies

## Project dependencies

1. Run `uv lock --upgrade` to update all dependencies
2. Run `uv pip list --outdated` to check for outdated dependencies
3. Run `uv add <package>@latest` to add a new dependency if needed

## Pre-commit hooks

1. Run `uv run pre-commit autoupdate`

Also, Dependabot will help you to keep your dependencies up-to-date, see [dependabot.yml](.github/dependabot.yml).
