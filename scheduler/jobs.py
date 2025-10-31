from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from storage import db
from auth import twitter
import typer

scheduler = BackgroundScheduler()

def check_and_post():
    """Check database for due posts and send them."""
    posts = db.get_all_posts()
    now = datetime.now()

    for post in posts:
        post_id, message, platform, time_str = post
        post_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        if post_time <= now:
            typer.echo(f"🚀 Sending to {platform}: {message}")

            if platform.lower() == "twitter":
                twitter.post_to_twitter(message)

            # TODO: add LinkedIn logic later
            db.delete_post(post_id)
        else:
            typer.echo(f"⏳ Waiting for post {post_id}")

def start_scheduler():
    scheduler.add_job(check_and_post, "interval", minutes=1)
    scheduler.start()
    typer.echo("🕒 Scheduler started! Checking for due posts every 1 minute.")
