import logging

formatter = logging.Formatter("\033[35mCODE_FORGE_AI\033[0m:     %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
