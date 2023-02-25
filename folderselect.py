import io
import pandas as pd
from pathlib import Path

from folderdata import FolderData


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, usecols=(3, 4), index_col=0, names=["time", str(path)])


def read_bmp(path: Path) -> io.BytesIO:
    bmp = path.read_bytes()
    return io.BytesIO(bmp)


def folder_select(question: str) -> FolderData:
    """
    ファイルのデータ番号を尋ねるダイアログを出す。
    尋ねる文面はquestionで指示する。
    csvとcsvのパスとbmpを取得し、csvはDataFrameに、bmpはBytesIOに変換される。
    FolderDataオブジェクトを返し、
    dfはDataFrame、csv_pathはpathのリスト、bmpはbmpのbytes、bmp_nameはbmpのファイル名になっている。
    """
    while True:
        num = input(question).rjust(4, "0")

        csv1 = Path(f"data/ALL{num}/F{num}CH1.CSV")
        csv2 = csv1.with_stem(f"F{num}CH2")
        bmp = csv1.with_name(f"F{num}TEK.BMP")

        functions = {".csv": read_csv, ".bmp": read_bmp}
        data: dict[Path, pd.DataFrame | bytes] = {}

        for path in (csv1, csv2, bmp):
            func = functions[path.suffix.lower()]

            try:
                data[path] = func(path)
            except FileNotFoundError:
                print(f"file not found -> {path.resolve()}")
                break
            else:
                print(path)
        else:
            df = data[csv1].join(data[csv2])
            return FolderData(df=df, bmp=data[bmp])
