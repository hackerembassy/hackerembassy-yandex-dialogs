from hackem_yandex_dialogs import (
    PROJECT_NAME,
    app,
    config,
    is_prod,
    loop,
    scheduler,
)
from hackem_yandex_dialogs.core import BotCore

core = BotCore(app, PROJECT_NAME, is_prod, loop, config, scheduler)

core.start()
