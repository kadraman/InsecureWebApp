
import logging
import os

logger = logging.getLogger(__name__)


def get_file_path(basepath, filename):
    site_root = os.path.realpath(os.path.dirname(basepath))
    file_path = os.path.join(site_root, "data", filename)
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.debug("File path: " + file_path)
    return file_path
