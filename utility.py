import csv
import ffr_config
from base_logger import logger

def get_list_data():
    try:
        with open(ffr_config.LINK_LIST, 'rt') as csvfile:
            return sorted(list(csv.reader(csvfile)))
    except Exception:
        logger.exception("utility:get_list_data")

