import os
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
print('Will use log level:', LOG_LEVEL)

LOGGER = logging.getLogger('SO-logger')

logging.basicConfig(
    format='%(asctime)s [%(threadName)s][%(filename)s:%(lineno)d][%(name)s-%(levelname)s]: %(message)s',
    level=LOG_LEVEL,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
