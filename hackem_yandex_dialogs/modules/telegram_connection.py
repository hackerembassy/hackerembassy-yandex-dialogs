from aioalice.types.alice_request import AliceRequest

from hackem_yandex_dialogs import dp
from hackem_yandex_dialogs.states import TelegramConnectionState


@dp.request_handler(regexp="подключ(и|ить) (телеграм|Telegram)")
async def connect_telegram_handler(alice_request: AliceRequest):
    has_screen = (
        "screen"
        in alice_request._raw_kwargs.get(  # pylint: disable=protected-access
            "meta", {}
        ).get("interfaces", {})
    )
    if not has_screen:
        return alice_request.response(
            "К сожалению, я не могу подключить Telegram на устройстве без экрана.\n\n"
            "Чтобы это сделать, открой приложение «Яндекс» или «Дом с Алисой» и скажи "
            "«Алиса, попроси хакер спейс подключить телеграм»"
        )
    await dp.storage.set_state(
        alice_request.session.user_id,
        TelegramConnectionState.AWAITING_USERNAME,
    )
    return alice_request.response(
        "Отлично! Воспользуйся клавиатурой и отправь мне свой юзернейм Telegram, "
        "обязательно без собачки, и после этого я смогу отмечать тебя на любом устройстве",
        buttons=["Отмена"],
    )


@dp.request_handler(regexp="отключ(и|ить) (телеграм|Telegram)")
async def disconnect_telegram_handler(alice_request: AliceRequest):
    return alice_request.response(
        "Хорошо. Твой Telegram юзернейм удален из хранилища.\n\n"
        "Если захочешь указать его снова - ты знаешь, что делать",
        user_state_update={"telegram_username": ""},
    )


@dp.request_handler(
    commands=["отмена"], state=TelegramConnectionState.AWAITING_USERNAME
)
async def connect_telegram_cancel_handler(alice_request: AliceRequest):
    await dp.storage.reset_state(alice_request.session.user_id)
    return alice_request.response(
        "Подключение Telegram отменено. Если передумаешь - ты знаешь, что делать"
    )


@dp.request_handler(state=TelegramConnectionState.AWAITING_USERNAME)
async def connect_telegram_username_handler(alice_request: AliceRequest):
    await dp.storage.reset_state(alice_request.session.user_id)
    telegram_username = alice_request.request.original_utterance
    return alice_request.response(
        f"Готово! Установлен юзернейм Telegram - {telegram_username}.\n\n"
        "Если захочешь его изменить, просто попроси меня настроить его еще раз",
        user_state_update={"telegram_username": telegram_username},
    )
