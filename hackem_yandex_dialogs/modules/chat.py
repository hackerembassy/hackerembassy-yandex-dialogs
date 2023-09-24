import random

from aioalice.types.alice_request import AliceRequest

from hackem_yandex_dialogs import dp


@dp.request_handler(commands=[""])
async def startup_handler(alice_request: AliceRequest):
    commands = [
        "статус спейса",
        "кто в спейсе?",
        "кто планирует придти?",
        "я планирую придти вечером",
        "я планирую придти ближе к вечеру",
        "я планирую придти к 21:00",
        "я не планирую придти",
        "сколько человек внутри?",
        "сколько человек планирует придти?",
        "открыт ли спейс?",
    ]
    return alice_request.response(
        "Привет! С помощью этого навыка ты можешь узнать статус спейса, "
        "кто внутри и кто планирует придти, а также отметиться планирующим придти.\n\n"
        f"Чтобы воспользоваться мной, скажи, например: «Алиса, {random.choice(commands)}»",
        buttons=[
            "Статус спейса",
            "Кто внутри?",
            "Кто планирует придти?",
            "Я планирую придти в спейс",
        ],
    )


@dp.request_handler(commands=["привет"])
async def hello_handler(alice_request: AliceRequest):
    return alice_request.response("Пока")


@dp.request_handler(commands=["пока"])
async def bye_handler(alice_request: AliceRequest):
    return alice_request.response("Привет")


@dp.request_handler(commands=["иди нахуй", "иди на хуй", "заткнись"])
async def bye_bye_handler(alice_request: AliceRequest):
    return alice_request.response("Ок", end_session=True)


@dp.request_handler(commands=["спасибо"])
async def thanks_handler(alice_request: AliceRequest):
    return alice_request.response("Обращайся ахпер джан")


@dp.request_handler(commands=["пенисы", "я съебываю"])
async def rickroll_handler(alice_request: AliceRequest):
    return alice_request.response(
        "Да",
        tts='<speaker audio="dialogs-upload/b293af34-45ce-45a1-8756-abbd1e57a0d1/503cf12a-79d3-4996-9255-d1bcd345376c.opus">',
    )
