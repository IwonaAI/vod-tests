import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.vod.film/")
SEARCH_PHRASE = os.getenv("SEARCH_PHRASE", "the pickup")
LOGIN_MODAL_TIMEOUT = int(os.getenv("LOGIN_MODAL_TIMEOUT", "65"))  # seconds to wait for login modal after playback

# Potential future config values (placeholder for extension):
# RESULT_WAIT_TIMEOUT = int(os.getenv("RESULT_WAIT_TIMEOUT", "30"))
