from hackem_yandex_dialogs import PROJECT_NAME, app, config, is_prod, loop
from hackem_yandex_dialogs.core import BotCore

core = BotCore(app, PROJECT_NAME, is_prod, loop, config)

core.start()
