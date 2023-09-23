import logging
import sys
from unittest.mock import patch

LOGGER = logging.getLogger(__name__)

sys.path.append("./")

from datetime import timedelta  # noqa: e402


def test_format():
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.utils import td_format
    formatted = td_format(
        timedelta(days=1, hours=4, minutes=30, seconds=20), "en"
    )
    LOGGER.info(formatted)
    assert formatted == "1 day, 4 hours, 30 minutes, 20 seconds"


def test_ru_format():
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.utils import td_format
    formatted = td_format(
        timedelta(days=2, hours=22, minutes=12, seconds=20), "ru"
    )
    LOGGER.info(formatted)
    assert formatted == "2 дня, 22 часа, 12 минут, 20 секунд"


def test_format_ago():
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.utils import td_format
    formatted = td_format(
        timedelta(days=1, hours=4, minutes=30, seconds=20), "en", True
    )
    LOGGER.info(formatted)
    assert formatted == "1 day, 4 hours, 30 minutes, 20 seconds ago"


def test_ru_format_ago():
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.utils import td_format
    formatted = td_format(
        timedelta(days=2, hours=22, minutes=12, seconds=20), "ru", True
    )
    LOGGER.info(formatted)
    assert formatted == "2 дня, 22 часа, 12 минут, 20 секунд назад"
