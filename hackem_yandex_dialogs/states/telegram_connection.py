from aioalice.utils.helper import Helper, HelperMode, Item


class TelegramConnectionState(Helper):
    mode = HelperMode.snake_case

    AWAITING_USERNAME = Item()
