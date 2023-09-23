import logging
import sys
from unittest.mock import patch

LOGGER = logging.getLogger(__name__)

sys.path.append("./")


def test_cfgmgr():
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.core.config_manager import ConfigManager
        from hackem_yandex_dialogs.core.config_manager.providers import (
            IniProvider,
            TomlProvider,
        )

    config_ini = ConfigManager(IniProvider(".config.ini"))
    config_toml = ConfigManager(TomlProvider("config.toml"))

    LOGGER.info(config_ini.__dict__)
    LOGGER.info(config_toml.__dict__)

    assert config_ini.get_item(
        "core", "supported_modules"
    ) == config_toml.get_item("core", "supported_modules")
