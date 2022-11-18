import logging
from app.fitness.init import init

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize aiogram app
if __name__ == "__main__":
    init()
