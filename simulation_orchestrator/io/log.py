import os
import logging

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGER = logging.getLogger('SO-logger')
LOGGER.setLevel(LOG_LEVEL)

logging.basicConfig(
    format='%(asctime)s [%(threadName)s][%(filename)s:%(lineno)d][%(name)s-%(levelname)s]: %(message)s',
    level=LOG_LEVEL,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

logging.info(f"Using Debug Level '{LOG_LEVEL}'")
