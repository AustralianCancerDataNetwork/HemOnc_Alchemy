import pandas as pd
from .identifiers import safe_identifier

def looks_denormalised_text(series: pd.Series, col_name: str) -> bool:
    if "html" in col_name or "alldays" in col_name:
        return False

    non_null = series.dropna().astype(str)
    if len(non_null) == 0:
        return False
    return any(("|" in v) or (";" in v) for v in non_null)



def infer_pipe_groups(
    df: pd.DataFrame,
    columns: list[str],
) -> list[list[str]]:
    """
    Group columns that have identical pipe-count vectors across rows and try name it
    """
    groups = []
    cols = sorted(set(columns))
    df = df.rename(columns=lambda c: safe_identifier(c).lower())
    for c1, c2 in zip(cols[:-1], cols[1:]):
        if c1 in c2 or c2 in c1:
            n1 = df[c1].fillna("").astype("string").str.count(r"\|").add(1)
            n2 = df[c2].fillna("").astype("string").str.count(r"\|").add(1)
            if n1.eq(n2).all():
                groups.append([c1, c2])
    return groups
            
