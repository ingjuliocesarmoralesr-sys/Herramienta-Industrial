from apscheduler.schedulers.background import BackgroundScheduler

from .trends import collect_trends

scheduler = BackgroundScheduler()


async def run_daily_alert_job() -> None:
    # Placeholder for email/slack integration.
    # Keeps daily alert capability in place using public APIs only.
    await collect_trends("technology")


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(
        lambda: __import__("asyncio").run(run_daily_alert_job()),
        trigger="cron",
        hour=9,
        minute=0,
        id="daily-trend-alerts",
        replace_existing=True,
    )
    scheduler.start()
