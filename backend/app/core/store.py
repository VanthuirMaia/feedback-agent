import pandas as pd

class DataStore:
    """Store em memória para os feedbacks carregados."""
    
    def __init__(self):
        self._df: pd.DataFrame | None = None

    def set(self, df: pd.DataFrame):
        self._df = df

    def get(self) -> pd.DataFrame | None:
        return self._df

    def clear(self):
        self._df = None

    @property
    def is_empty(self) -> bool:
        return self._df is None or self._df.empty


# Instância global
store = DataStore()