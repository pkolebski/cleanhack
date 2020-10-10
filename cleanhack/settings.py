TWITTER_DATA_PATH = None
PROCESSED_TWITTER_DATA = None

try:
    from .user_settings import *  # silence pyflakes
except ImportError:
    pass
