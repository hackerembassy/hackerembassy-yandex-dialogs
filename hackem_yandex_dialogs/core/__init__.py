from asyncio import AbstractEventLoop
from typing import List

from aiohttp import web as aiohttp_web
from aiohttp.web import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from hackem_yandex_dialogs.core.config_manager import ConfigManager
from hackem_yandex_dialogs.core.config_manager.types.exceptions.feature_unavailable import (
    FeatureUnavailableError,
)
from hackem_yandex_dialogs.core.external.logging import AccessLogger
from hackem_yandex_dialogs.core.loader import ModuleLoader
from hackem_yandex_dialogs.core.task_manager import (
    BaseCoreTask,
    BaseSchedulerTask,
)


class BotCore:
    __slots__ = [
        "app",
        "project_name",
        "is_prod",
        "loop",
        "config",
        "scheduler",
        "__pending_core_tasks",
        "__pending_scheduler_tasks",
    ]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        app: Application,
        project_name: str,
        is_prod: bool,
        loop: AbstractEventLoop,
        config: ConfigManager,
        scheduler: AsyncIOScheduler | None,
    ) -> None:
        logger.info(f"Initializing {project_name}...")
        self.app = app
        self.project_name = project_name
        self.is_prod = is_prod
        self.loop = loop
        self.config = config
        self.scheduler = scheduler
        self.__pending_core_tasks: List[BaseCoreTask] = []
        self.__pending_scheduler_tasks: List[BaseSchedulerTask] = []

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

    def add_scheduler_task(self, task: BaseSchedulerTask):
        """Add scheduler task to run

        Args:
            task (BaseSchedulerTask): Task object
        """
        self.__pending_scheduler_tasks.append(task)

    def add_scheduler_tasks(self, *args: BaseSchedulerTask):
        """Add multiple scheduler tasks"""
        self.__pending_scheduler_tasks.extend(args)

    def push_pending_scheduler_tasks(self):
        """Push pending scheduler tasks to scheduler

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method
        """
        if not self.scheduler:
            raise FeatureUnavailableError(
                "Feature use_apscheduler required in order to call this method"
            )
        ready_tasks = [
            task
            for task in self.__pending_scheduler_tasks
            if hasattr(task, "name")
            and hasattr(task, "trigger")
            and hasattr(task, "force_reschedule")
        ]
        if not ready_tasks:
            return
        for task in ready_tasks:
            if task.force_reschedule:
                if self.scheduler.get_job(job_id=task.name):
                    self.scheduler.remove_job(job_id=task.name)
            self.scheduler.add_job(
                func=task.run_task,
                trigger=task.trigger,
                id=task.name,
                misfire_grace_time=1
                if not hasattr(task, "misfire_grace_time")
                else task.misfire_grace_time,
            )
            self.__pending_scheduler_tasks.remove(task)

    def cancel_scheduler_task(self, task_name: str) -> bool:
        """Cancel scheduler task

        Args:
            task_name (str): task name

        Raises:
            FeatureUnavailableError: feature use_apscheduler required in order to call this method

        Returns:
            bool: success
        """
        if not self.scheduler:
            raise FeatureUnavailableError(
                "Feature use_apscheduler required in order to call this method"
            )
        if self.scheduler.get_job(job_id=task_name):
            self.scheduler.remove_job(job_id=task_name)
        return True

    async def _startup(self):
        """Main startup logic

        Args:
            dispatcher (Dispatcher): aiogram dispatcher object
        """

        ModuleLoader(self.project_name, self.is_prod, self.config).load_all()

        if self.scheduler:
            self.scheduler.start()
            self.push_pending_scheduler_tasks()

        self.__run_core_tasks()
        await aiohttp_web._run_app(
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
