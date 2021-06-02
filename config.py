from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), ".env")

# Load file from the path.
load_dotenv(dotenv_path)

BOT_TOKEN = getenv('BOT_TOKEN', "")
CHAT_NAME = getenv('CHAT_NAME', "")
INSIDE_CHANNEL = getenv('INSIDE_CHANNEL', "")
