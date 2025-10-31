import typer
from storage import db
from scheduler import jobs

app = typer.Typer()

@app.command()
def add_post(message: str, platform: str, time: str):
    """Add a new social media post."""
    db.add_post(message, platform, time)
    typer.echo(f"✅ Post saved for {platform} at {time}")

@app.command()
def list_posts():
    """List all scheduled posts."""
    posts = db.get_all_posts()

    if not posts:
        typer.echo("No posts scheduled yet.")
        return

    typer.echo("📅 Scheduled Posts:")
    for post in posts:
        typer.echo(f"{post[0]}. {post[2]} → {post[1]} at {post[3]}")

@app.command()
def run_scheduler():
    """Run the background scheduler."""
    jobs.start_scheduler()
    typer.echo("📡 Scheduler is active. Press Ctrl+C to stop.")

    # Keep app running so scheduler can do its work
    try:
        while True:
            pass
    except KeyboardInterrupt:
        typer.echo("\n🛑 Scheduler stopped.")

if __name__ == "__main__":
    db.create_table()
    app()
