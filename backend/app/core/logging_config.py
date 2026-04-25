import logging
import sys
from .config import settings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d — %(message)s"


def setup_logging():
    """统一日志配置，所有模块使用同一个 logger"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("wishing-well")
