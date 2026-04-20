from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config
from classification_model.processing.data_manager import pre_pipeline_preparation


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    pre_processed = pre_pipeline_preparation(dataframe=input_data)
    validated_data = pre_processed[config.model_config_.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleTitanicDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class TitanicDataInputSchema(BaseModel):
    pclass: Optional[int] = None
    sex: Optional[str] = None
    age: Optional[float] = None
    sibsp: Optional[int] = None
    parch: Optional[int] = None
    fare: Optional[float] = None
    cabin: Optional[str] = None
    embarked: Optional[str] = None
    title: Optional[str] = None


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
