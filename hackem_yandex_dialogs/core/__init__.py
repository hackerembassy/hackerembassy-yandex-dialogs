from asyncio import AbstractEventLoop
from typing import List

from aiohttp import web as aiohttp_web
from aiohttp.web import Application
from loguru import logger

from hackem_yandex_dialogs.core.config_manager import ConfigManager
from hackem_yandex_dialogs.core.external.logging import AccessLogger
from hackem_yandex_dialogs.core.loader import ModuleLoader
from hackem_yandex_dialogs.core.task_manager import BaseCoreTask


class BotCore:
    __slots__ = [
        "app",
        "project_name",
        "is_prod",
        "loop",
        "config",
        "__pending_core_tasks",
    ]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        app: Application,
        project_name: str,
        is_prod: bool,
        loop: AbstractEventLoop,
        config: ConfigManager,
    ) -> None:
        logger.info(f"Initializing {project_name}...")
        self.app = app
        self.project_name = project_name
        self.is_prod = is_prod
        self.loop = loop
        self.config = config
        self.__pending_core_tasks: List[BaseCoreTask] = []

    def add_core_task(self, task: BaseCoreTask):
        """Add core task to run. Core tasks running once on startup

        Args:
            task (BaseCoreTask): Task object
        """
        self.__pending_core_tasks.append(task)

    def add_core_tasks(self, *args: BaseCoreTask):
        """Add multiple core tasks. Core tasks running once on startup"""
        self.__pending_core_tasks.extend(args)

    def __run_core_tasks(self):
        """Run core tasks"""
        ready_tasks = [
            task for task in self.__pending_core_tasks if hasattr(task, "name")
        ]
        if not ready_tasks:
            return
        logger.info(
            f"Core tasks to be runned: {', '.join([task.name for task in ready_tasks])}"
        )
        for task in ready_tasks:
            logger.info(f"Running core task {task.name}...")
            self.loop.create_task(task.run_task())
            self.__pending_core_tasks.remove(task)

    async def _startup(self):
        """Main startup logic

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object
        """

        ModuleLoader(self.project_name, self.is_prod, self.config).load_all()

        self.__run_core_tasks()
        await aiohttp_web._run_app(  # pylint: disable=protected-access
            self.app,
            host=self.config.get_item("app", "host"),
            port=self.config.get_item("app", "port"),
            access_log_class=AccessLogger,
        )

    async def _shutdown(self):
        """Main shutdown logic

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object
        """
        logger.warning("Shutting down...")
        return

    def start(self):
        """Start bot"""
        logger.info(f"Starting {self.project_name}...")
        self.loop.run_until_complete(self._startup())
