import io
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class FolderData:
    df: pd.DataFrame
    bmp: io.BytesIO
