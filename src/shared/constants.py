# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

from enum import Enum
from pathlib import Path

# Diretórios
ROOT_DIR=Path(__file__).parents[1]
DATASET_DIR=Path(ROOT_DIR, 'data', 'kneeKL224')
MODELS_DIR=Path(ROOT_DIR)

# Enum dos tipos de classificadores
class ClassifierTypes(Enum):
    BinaryCnn = 1,
    BinaryShallow = 2,
    MulticlassCnn = 3,
    MulticlassShallow = 4
