from aiohttp.abc import AbstractAccessLogger
from loguru import logger


class AccessLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        logger.info(
            f'{request.headers.get("X-Real-IP", request.remote)} '
            f'"{request.method} {request.path} '
            f"done in {round(time*1000, 2)}ms: {response.status}"
        )
