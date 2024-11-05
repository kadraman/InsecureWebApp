"""Application entry point."""
from iwa import create_app
import os

os.environ["SESSION_SECRET"]="YourSessionSecret"

app = create_app()
app.run()