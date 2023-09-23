from aioalice.types.alice_request import AliceRequest

from hackem_yandex_dialogs import dp


@dp.request_handler(commands=["привет"])
async def hello_handler(alice_request: AliceRequest):
    return alice_request.response("Пока")


@dp.request_handler(commands=["пока"])
async def bye_handler(alice_request: AliceRequest):
    return alice_request.response("Привет")


@dp.request_handler(commands=["иди нахуй", "иди на хуй"])
async def bye_bye_handler(alice_request: AliceRequest):
    return alice_request.response("Ок", end_session=True)


@dp.request_handler(commands=["спасибо"])
async def thanks_handler(alice_request: AliceRequest):
    return alice_request.response("Обращайся брат")
