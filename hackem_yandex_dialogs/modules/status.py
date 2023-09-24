from aioalice.types.alice_request import AliceRequest

from hackem_yandex_dialogs import dp
from hackem_yandex_dialogs.models.status import Status
from hackem_yandex_dialogs.utils import decl, native_join
from hackem_yandex_dialogs.utils.hackem_api import make_api_request


@dp.request_handler(regexp=r"статус( спейса|)")
async def status_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс."
        )
    status = Status(**ans)
    print(status)
    inside_count = len(status.inside)
    going_count = len(status.planning_to_go)
    inside_status = (
        f"Внутри {inside_count} {decl(inside_count, ['человек', 'человека', 'человек'])}"
        if status.inside
        else "Внутри никого нет"
    )
    going_status = (
        f"Планиру{'ет' if going_count == 1 else 'ют'} зайти еще {going_count} {decl(going_count, ['человек', 'человека', 'человек'])}"
        if status.planning_to_go
        else "Пока что никто не планирует приходить в спейс"
    )
    return alice_request.response(
        f"На данный момент спейс {'открыт' if status.is_open else 'закрыт'}. {inside_status}. {going_status}"
    )


@dp.request_handler(regexp=r"сколько (человек|людей) (в спейсе|внутри)")
async def status_inside_count_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс"
        )
    status = Status(**ans)
    print(status)
    if not status.inside:
        return alice_request.response("На данный момент в спейсе никого нет")
    inside_count = len(status.inside)
    return alice_request.response(
        f"Внутри спейса {inside_count} {decl(inside_count, ['человек', 'человека', 'человек'])}"
    )


@dp.request_handler(
    regexp=r"сколько (человек|людей) (придет|планирует при(д|й)ти)"
)
async def status_planning_count_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс"
        )
    status = Status(**ans)
    print(status)
    if not status.planning_to_go:
        return alice_request.response(
            "Пока что никто не планирует приходить в спейс"
        )
    going_count = len(status.planning_to_go)
    return alice_request.response(
        f"Планиру{'ет' if going_count == 1 else 'ют'} придти в спейс еще {going_count} {decl(going_count, ['человек', 'человека', 'человек'])}"
    )


@dp.request_handler(regexp=r"(открыт ли |)спейс( открыт| закрыт|)")
async def status_state_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс"
        )
    status = Status(**ans)
    print(status)
    return alice_request.response(
        f"На данный момент спейс {'открыт' if status.is_open else 'закрыт'} пользователем {status.changed_by}"
    )


@dp.request_handler(regexp=r"кто (в спейсе|внутри)")
async def status_who_inside_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс"
        )
    status = Status(**ans)
    print(status)
    if not status.inside:
        return alice_request.response("На данный момент в спейсе никого нет")
    inside_count = len(status.inside)
    return alice_request.response(
        f"Внутри спейса {inside_count} {decl(inside_count, ['человек', 'человека', 'человек'])}. А именно: {native_join([x.username for x in status.inside])}"
    )


@dp.request_handler(regexp=r"кто планирует( зайти| при(д|й)ти|)( в спейс|)")
async def status_who_planning_handler(alice_request: AliceRequest):
    ans = await make_api_request("api/status", False)
    if "error" in ans:
        return alice_request.response(
            "Не удалось получить статус спейса. Возможно, в нем умер хасс"
        )
    status = Status(**ans)
    print(status)
    if not status.planning_to_go:
        return alice_request.response(
            "Пока что никто не планирует приходить в спейс"
        )
    going_count = len(status.planning_to_go)
    return alice_request.response(
        f"Планиру{'ет' if going_count == 1 else 'ют'} придти в спейс еще {going_count} {decl(going_count, ['человек', 'человека', 'человек'])}. А именно: {native_join([x.username for x in status.planning_to_go])}"  # pylint: disable=not-an-iterable
    )
