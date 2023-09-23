from sys import platform

import aiohttp
import orjson
from aiohttp.client import ClientResponse

from hackem_yandex_dialogs import logger
from hackem_yandex_dialogs.utils.async_tools import run_async, run_sync
from hackem_yandex_dialogs.utils.datetime_tools import td_format

__all__ = (
    "run_async",
    "run_sync",
    "td_format",
    "make_request",
)


async def make_request(  # pylint: disable=too-many-arguments
    url: str,
    method: str = "get",
    params: dict = None,
    headers: dict = None,
    timeout: int = None,
    data: dict = None,
    json: dict = None,
    allow_redirects: bool = True,
    json_answer: bool = False,
    text_answer: bool = False,
    raise_for_status: bool = True,
) -> ClientResponse | str | dict:
    """Make web request

    Args:
        url (str): URL to be called
        method (str, optional): Call method: get or post. Defaults to "get".
        params (dict, optional): Request parameters. Defaults to None.
        headers (dict, optional): Request headers. Defaults to None.
        timeout (int, optional): Request timeout. Defaults to None.
        data (dict, optional): Request data (for post request). Defaults to None.
        json (dict, optional): Request json data (for post request). Defaults to None.
        allow_redirects (bool, optional): Allow redirects during request execution. Defaults to True.
        json_answer (bool, optional): Get answer as json. Defaults to False.
        text_answer (bool, optional): Get answer as string. Defaults to False.
        raise_for_status (bool, optional): Raise an Error if request status != 200. Defaults to True

    Raises:
        ConnectionError: Timeout exceeded
        ValueError: Invalid request method

    Returns:
        ClientResponse | str | dict: Request response
    """
    if not json_answer and not text_answer and platform in ["linux", "linux2"]:
        logger.warning(
            "Since aiohttp can freeze while getting data "
            "from answer outside opened session, "
            "you need to toggle json_answer or text_answer "
            "in order to get json or text answer as well."
        )
    try:
        async with aiohttp.ClientSession(
            json_serialize=lambda x: orjson.dumps(  # pylint: disable=no-member
                x
            ).decode(),
            raise_for_status=raise_for_status,
        ) as session:
            match method:
                case "get":
                    req = await session.get(
                        url, params=params, headers=headers, timeout=timeout
                    )
                    return (
                        req
                        if not json_answer and not text_answer
                        else await req.json(
                            content_type=None,
                            loads=orjson.loads,  # pylint: disable=no-member
                        )
                        if json_answer
                        else await req.text()
                    )
                case "post":
                    req = await session.post(
                        url,
                        params=params,
                        json=json,
                        data=data,
                        headers=headers,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                    )
                    return (
                        req
                        if not json_answer and not text_answer
                        else await req.json(
                            content_type=None,
                            loads=orjson.loads,  # pylint: disable=no-member
                        )
                        if json_answer
                        else await req.text()
                    )
                case _:
                    raise ValueError(f"Invalid request method: {method}")
    except (  # pylint: disable=invalid-name,broad-exception-caught
        Exception
    ) as e:
        logger.exception(e)
        raise ConnectionError(e) from e


def decl(number: int, titles: list):
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < number % 100 < 20:
        idx = 2
    elif number % 10 < 5:
        idx = cases[number % 10]
    else:
        idx = cases[5]

    return titles[idx]


def rreplace(string: str, old: str, new: str, occurrence: int):
    splitted = string.rsplit(old, occurrence)
    return new.join(splitted)


def native_join(data: list):
    return rreplace(", ".join(data), ", ", " и ", 1)
