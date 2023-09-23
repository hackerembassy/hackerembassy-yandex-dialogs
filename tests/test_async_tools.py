import sys
from asyncio import sleep
from unittest.mock import patch

import pytest

sys.path.append("./")


@pytest.mark.asyncio
async def test_asynctools():
    """If uvloop and nest_asyncio disabled - RuntimeError will be raised.
    Because this behavior isn't intended in project - we test that no RuntimeError is raised in normal mode
    """
    with patch("sys.argv", ["hackem_yandex_dialogs"]):
        from hackem_yandex_dialogs.utils import run_async

        async def coro2():
            await sleep(3)
            return 2 + 2

        async def coro1():
            run_async(coro2)
            return 2 + 2

    run_async(coro1)
