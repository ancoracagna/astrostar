import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

admins = [408531138]
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()
