from celery import Celery
from celery.schedules import crontab

from config import settings

from .tasks import remove_irrelevant_documents

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.result_backend_transport_options = {
    "global_keyprefix": f"{settings.APP_REDIS_PREFIX}:",
}

celery.conf.timezone = "Europe/Moscow"


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):  # noqa ARG001
    sender.add_periodic_task(
        crontab(hours="*/24"),
        celery.task(remove_irrelevant_documents).s(),
        name="remove irrelevant documents",
    )
