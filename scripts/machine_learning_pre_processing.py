import pandas as pd
from pathlib import Path

def remove_duplicate_rows(path: str, file_name: str) -> pd.DataFrame:
    """
    This function removes duplicate rows from a csv file.

    Parameters
    ----------
    path : str
        The path to the csv file.
    file_name : str
        The name of the csv file.

    """
    df = pd.read_csv(Path(path, file_name), index_col=0)
    df.drop_duplicates(inplace=True, keep='first')
    return df