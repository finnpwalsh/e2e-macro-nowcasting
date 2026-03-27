from __future__ import annotations

from typing import Protocol

import pandas as pd
import numpy as np


class Scorer(Protocol):
    def score(
            self,
            *,
            y: pd.Series,
            y_hat: pd.Series | np.ndarray,
    ) -> dict[str, float]: ...