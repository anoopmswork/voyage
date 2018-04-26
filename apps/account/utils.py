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
        d2 = datetime.datetime.strptime(now, "%d-%m-%Y")
        d1 = datetime.datetime.strptime(birthday, "%d-%m-%Y")
        current_age = (d2 - d1).days / 365
        return False if current_age < 18 else True
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))
