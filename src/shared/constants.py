from enum import Enum
from pathlib import Path

ROOT_DIR=Path(__file__).parents[1]
DATASET_DIR=Path(ROOT_DIR, 'data', 'kneeKL224')

MODELS_DIR=Path(ROOT_DIR)

class ClassifierTypes(Enum):
    BinaryCnn = 1,
    BinaryShallow = 2,
    MulticlassCnn = 3,
    MulticlassShallow = 4
