from aioalice.types.alice_request import AliceRequest

from hackem_yandex_dialogs import dp


@dp.request_handler()
async def unknown_command_handler(alice_request: AliceRequest):
    print(alice_request)
    return alice_request.response("Я не понимаю тебя")
