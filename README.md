# Hacker Embassy Yandex Dialogs

[![Python 3.10](https://img.shields.io/badge/python-^3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://mit-license.org/)

# About

This dialog uses public Hacker Embassy Telegram bot API to interact with hackerspace via Yandex Alice powered devices

Features:

- Ask for hackerspace status, inside and planning to go users
- Check-in for planning to go (needs Telegram username assignment)

# Hosting

At the moment, dialog's hosted on [rf0x1d](https://github.com/rfoxxxy)'s machine located in Nuremberg, Germany

# Dependencies

- Python 3.10+
- Poetry 1.3.1+

All dependencies declared in the `pyproject.toml` file and installed on the server using `poetry install`

# Local deployment

- Install [Python](https://www.python.org/downloads/) version 3.10+
- Install [Poetry](https://python-poetry.org/docs/)
- Go to the cloned repository directory
- Install dependencies using `poetry install`
- Write config file named `config.toml` (example declared in `config-example.toml`, you can ask [rf0x1d](https://github.com/rfoxxxy) or [@tectonick](https://github.com/tectonick) for an API token if you want to use check-in feature)
- Start the application with `poetry run python3 -m hackem_yandex_dialogs`

# Yandex Dialog access

If you're using Yandex Station/Auto/Alice/etc. and want to use this dialog, you can ask [rf0x1d](https://github.com/rfoxxxy) for an access, or you can create private dialog by yourself on [Yandex Dialogs dev portal](https://dialogs.yandex.ru/developer)
