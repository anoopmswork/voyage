import logging
import datetime

from core import errors as err

# Get an instance of a logger
logger = logging.getLogger(__name__)

def is_adult(birthday):
    """
    To find whether an individual is adult using birthday date
    :param birthday:
    :return:
    """
    try:
        now = datetime.datetime.now().strftime("%d-%m-%Y")
        current_age=now-birthday
        print(current_age)
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))
