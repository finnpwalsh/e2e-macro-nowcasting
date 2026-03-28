from dataclasses import dataclass

@dataclass(frozen=True)
class DataSignature:
    n_rows: int
    columns: list[str]
    dtypes: dict[str, str]
    row_fingerprint: str
    n_train: int | None = None
    n_valid: int | None = None


@dataclass(frozen=True)
class FeatureSignature:
    n_features: int
    features: list[str]
    feature_dtypes: dict[str, str]
    feature_fingerprint: str