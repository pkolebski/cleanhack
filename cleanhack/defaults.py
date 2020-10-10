import os
from pathlib import Path

DATA_PATH = Path(os.path.dirname(__file__)).parent.joinpath('data').absolute()
