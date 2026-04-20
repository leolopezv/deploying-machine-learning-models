from typing import Any, List, Optional

from pydantic import BaseModel

try:
    from regression_model.processing.validation import HouseDataInputSchema
except ImportError:
    # Fallback schema when regression_model is not available
    class HouseDataInputSchema(BaseModel):
        MSSubClass: Optional[int] = None
        MSZoning: Optional[str] = None
        LotFrontage: Optional[float] = None
        LotArea: Optional[int] = None
        Street: Optional[str] = None
        Alley: Optional[str] = None
        LotShape: Optional[str] = None
        LandContour: Optional[str] = None
        Utilities: Optional[str] = None
        LotConfig: Optional[str] = None
        LandSlope: Optional[str] = None
        Neighborhood: Optional[str] = None
        Condition1: Optional[str] = None
        Condition2: Optional[str] = None
        BldgType: Optional[str] = None
        HouseStyle: Optional[str] = None
        OverallQual: Optional[int] = None
        OverallCond: Optional[int] = None
        YearBuilt: Optional[int] = None
        YearRemodAdd: Optional[int] = None
        RoofStyle: Optional[str] = None
        RoofMatl: Optional[str] = None
        Exterior1st: Optional[str] = None
        Exterior2nd: Optional[str] = None
        MasVnrType: Optional[str] = None
        MasVnrArea: Optional[float] = None
        ExterQual: Optional[str] = None
        ExterCond: Optional[str] = None
        Foundation: Optional[str] = None
        BsmtQual: Optional[str] = None
        BsmtCond: Optional[str] = None
        BsmtExposure: Optional[str] = None
        BsmtFinType1: Optional[str] = None
        BsmtFinSF1: Optional[float] = None
        BsmtFinType2: Optional[str] = None
        BsmtFinSF2: Optional[float] = None
        BsmtUnfSF: Optional[float] = None
        TotalBsmtSF: Optional[float] = None
        Heating: Optional[str] = None
        HeatingQC: Optional[str] = None
        CentralAir: Optional[str] = None
        Electrical: Optional[str] = None
        FirstFlrSF: Optional[int] = None
        SecondFlrSF: Optional[int] = None
        LowQualFinSF: Optional[int] = None
        GrLivArea: Optional[int] = None
        BsmtFullBath: Optional[float] = None
        BsmtHalfBath: Optional[float] = None
        FullBath: Optional[int] = None
        HalfBath: Optional[int] = None
        BedroomAbvGr: Optional[int] = None
        KitchenAbvGr: Optional[int] = None
        KitchenQual: Optional[str] = None
        TotRmsAbvGrd: Optional[int] = None
        Functional: Optional[str] = None
        Fireplaces: Optional[int] = None
        FireplaceQu: Optional[str] = None
        GarageType: Optional[str] = None
        GarageYrBlt: Optional[float] = None
        GarageFinish: Optional[str] = None
        GarageCars: Optional[float] = None
        GarageArea: Optional[float] = None
        GarageQual: Optional[str] = None
        GarageCond: Optional[str] = None
        PavedDrive: Optional[str] = None
        WoodDeckSF: Optional[int] = None
        OpenPorchSF: Optional[int] = None
        EnclosedPorch: Optional[int] = None
        ThreeSsnPortch: Optional[int] = None
        ScreenPorch: Optional[int] = None
        PoolArea: Optional[int] = None
        PoolQC: Optional[str] = None
        Fence: Optional[str] = None
        MiscFeature: Optional[str] = None
        MiscVal: Optional[int] = None
        MoSold: Optional[int] = None
        YrSold: Optional[int] = None
        SaleType: Optional[str] = None
        SaleCondition: Optional[str] = None


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]


class MultipleHouseDataInputs(BaseModel):
    inputs: List[HouseDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "MSSubClass": 20,
                        "MSZoning": "RH",
                        "LotFrontage": 80.0,
                        "LotArea": 11622,
                        "Street": "Pave",
                        "Alley": None,
                        "LotShape": "Reg",
                        "LandContour": "Lvl",
                        "Utilities": "AllPub",
                        "LotConfig": "Inside",
                        "LandSlope": "Gtl",
                        "Neighborhood": "NAmes",
                        "Condition1": "Feedr",
                        "Condition2": "Norm",
                        "BldgType": "1Fam",
                        "HouseStyle": "1Story",
                        "OverallQual": 5,
                        "OverallCond": 6,
                        "YearBuilt": 1961,
                        "YearRemodAdd": 1961,
                        "RoofStyle": "Gable",
                        "RoofMatl": "CompShg",
                        "Exterior1st": "VinylSd",
                        "Exterior2nd": "VinylSd",
                        "MasVnrType": "None",
                        "MasVnrArea": 0.0,
                        "ExterQual": "TA",
                        "ExterCond": "TA",
                        "Foundation": "CBlock",
                        "BsmtQual": "TA",
                        "BsmtCond": "TA",
                        "BsmtExposure": "No",
                        "BsmtFinType1": "Rec",
                        "BsmtFinSF1": 468.0,
                        "BsmtFinType2": "LwQ",
                        "BsmtFinSF2": 144.0,
                        "BsmtUnfSF": 270.0,
                        "TotalBsmtSF": 882.0,
                        "Heating": "GasA",
                        "HeatingQC": "TA",
                        "CentralAir": "Y",
                        "Electrical": "SBrkr",
                        "FirstFlrSF": 896,
                        "SecondFlrSF": 0,
                        "LowQualFinSF": 0,
                        "GrLivArea": 896,
                        "BsmtFullBath": 0.0,
                        "BsmtHalfBath": 0.0,
                        "FullBath": 1,
                        "HalfBath": 0,
                        "BedroomAbvGr": 2,
                        "KitchenAbvGr": 1,
                        "KitchenQual": "TA",
                        "TotRmsAbvGrd": 5,
                        "Functional": "Typ",
                        "Fireplaces": 0,
                        "FireplaceQu": None,
                        "GarageType": "Attchd",
                        "GarageYrBlt": 1961.0,
                        "GarageFinish": "Unf",
                        "GarageCars": 1.0,
                        "GarageArea": 730.0,
                        "GarageQual": "TA",
                        "GarageCond": "TA",
                        "PavedDrive": "Y",
                        "WoodDeckSF": 140,
                        "OpenPorchSF": 0,
                        "EnclosedPorch": 0,
                        "ThreeSsnPortch": 0,
                        "ScreenPorch": 120,
                        "PoolArea": 0,
                        "PoolQC": None,
                        "Fence": "MnPrv",
                        "MiscFeature": None,
                        "MiscVal": 0,
                        "MoSold": 6,
                        "YrSold": 2010,
                        "SaleType": "WD",
                        "SaleCondition": "Normal",
                    }
                ]
            }
        }
