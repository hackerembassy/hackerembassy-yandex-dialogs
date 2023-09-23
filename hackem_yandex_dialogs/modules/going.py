from aioalice.types.alice_request import AliceRequest
from loguru import logger

from hackem_yandex_dialogs import config, dp
from hackem_yandex_dialogs.utils.hackem_api import make_api_request


@dp.request_handler(
    regexp=r"я( сегодня|) (планирую|приду|зайду|заеду|заскочу|приеду|забегу|иду)( в спейс|)( сегодня|)( в спейс|)( придти| зайти| заехать| приехать| заскочить| забежать|)( в спейс|)( сегодня|) .+"
)
async def going_handler(alice_request: AliceRequest):
    message = None
    try:
        intents = (
            alice_request._raw_kwargs[  # pylint: disable=protected-access
                "request"
            ]["nlu"]["intents"]
        )
        if len(intents.keys()) > 0:
            for intent_name, intent_data in intents.items():
                match intent_name:
                    case "coming":
                        message = (
                            intent_data.get("slots", {})
                            .get("when", {})
                            .get("value", None)
                        )
                    case _:
                        continue
    except Exception as error:  # pylint: disable=broad-exception-caught
        logger.exception(error)
    await make_api_request(
        "api/setgoing",
        username=config.get_item("app", "username"),
        isgoing=True,
        message=message,
    )
    return alice_request.response(
        f"Теперь ты планируешь придти в спейс {message if message else ''}"
    )


@dp.request_handler(
    regexp=r"я( сегодня| больше|) не (планирую|приду|зайду|заеду|приеду|заскочу|забегу|иду)( в спейс|)( сегодня|)( в спейс|)( придти| зайти| заехать| приехать| заскочить| забежать|)( в спейс|)( сегодня|) .+"
)
async def not_going_handler(alice_request: AliceRequest):
    await make_api_request(
        "api/setgoing",
        username=config.get_item("app", "username"),
        isgoing=False,
    )
    return alice_request.response("Теперь ты не планируешь придти в спейс")
