from aioalice.types.alice_request import AliceRequest
from loguru import logger

from hackem_yandex_dialogs import dp
from hackem_yandex_dialogs.states import TelegramConnectionState
from hackem_yandex_dialogs.utils.hackem_api import make_api_request


@dp.request_handler(
    regexp=r"я( сегодня|) (планирую|при(й|)ду|зайду|заеду|заскочу|приеду|забегу|иду)( в спейс|)( сегодня|)( в спейс|)( при(д|й)ти| зайти| заехать| приехать| заскочить| забежать|)( в спейс|)( сегодня|) .+"
)
async def going_handler(alice_request: AliceRequest):
    message = None
    has_screen = (
        "screen"
        in alice_request._raw_kwargs.get(  # pylint: disable=protected-access
            "meta", {}
        ).get("interfaces", {})
    )
    telegram_username = (
        alice_request._raw_kwargs.get(  # pylint: disable=protected-access
            "state", {}
        )
        .get("user", {})
        .get("telegram_username")
    )
    if not telegram_username:
        if not has_screen:
            return alice_request.response(
                "Мы еще не знакомы, так что я не могу тебя отметить.\n\n"
                "Чтобы указать свой Telegram юзернейм, открой приложение "
                "«Яндекс» или «Дом с Алисой» и скажи "
                "«Алиса, попроси хакер спейс подключить телеграм». "
                "После подключения, я смогу отмечать тебя на любом устройстве"
            )
        await dp.storage.set_state(
            alice_request.session.user_id,
            TelegramConnectionState.AWAITING_USERNAME,
        )
        return alice_request.response(
            "Мы еще не знакомы, так что я не могу тебя отметить.\n\n"
            "Воспользуйся клавиатурой и отправь мне свой Telegram "
            "юзернейм, и после этого "
            "я смогу отмечать тебя на любом устройстве",
            buttons=["Отмена"],
        )
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
        username=telegram_username,
        isgoing=True,
        message=message,
    )
    return alice_request.response(
        f"Теперь ты планируешь придти в спейс {message if message else ''}",
        buttons=["Статус спейса", "Я больше не планирую придти"],
    )


@dp.request_handler(
    regexp=r"я( сегодня| больше|) не (планирую|при(й|)ду|зайду|заеду|приеду|заскочу|забегу|иду)( в спейс|)( сегодня|)( в спейс|)( при(д|й)ти| приходить| зайти| заехать| приехать| заскочить| забежать|)( в спейс|)( сегодня|) .+"
)
async def not_going_handler(alice_request: AliceRequest):
    has_screen = (
        "screen"
        in alice_request._raw_kwargs.get(  # pylint: disable=protected-access
            "meta", {}
        ).get("interfaces", {})
    )
    telegram_username = (
        alice_request._raw_kwargs.get(  # pylint: disable=protected-access
            "state", {}
        )
        .get("user", {})
        .get("telegram_username")
    )
    if not telegram_username:
        if not has_screen:
            return alice_request.response(
                "Мы еще не знакомы, так что я не могу тебя отметить.\n\n"
                "Чтобы указать свой Telegram юзернейм, открой приложение "
                "«Яндекс» или «Дом с Алисой» и скажи "
                "«Алиса, попроси хакер спейс подключить телеграм». "
                "После подключения, я смогу отмечать тебя на любом устройстве"
            )
        await dp.storage.set_state(
            alice_request.session.user_id,
            TelegramConnectionState.AWAITING_USERNAME,
        )
        return alice_request.response(
            "Мы еще не знакомы, так что я не могу тебя отметить.\n\n"
            "Воспользуйся клавиатурой и отправь мне свой Telegram "
            "юзернейм, и после этого "
            "я смогу отмечать тебя на любом устройстве",
            buttons=["Отмена"],
        )
    await make_api_request(
        "api/setgoing",
        username=telegram_username,
        isgoing=False,
    )
    return alice_request.response(
        "Теперь ты не планируешь придти в спейс",
        buttons=["Статус спейса", "Я планирую придти"],
    )
