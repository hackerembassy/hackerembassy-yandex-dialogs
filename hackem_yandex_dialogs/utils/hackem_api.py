from hackem_yandex_dialogs import PROJECT_NAME, config
from hackem_yandex_dialogs.utils import make_request


async def make_api_request(method: str, post: bool = True, **data):
    return await make_request(
        f"https://gateway.hackerembassy.site/{method}",
        "post" if post else "get",
        headers={"User-Agent": f"rf0x3d/1.0.0 ({PROJECT_NAME})"},
        json={"token": config.get_item("app", "api_token"), **data},
        json_answer=True,
    )
