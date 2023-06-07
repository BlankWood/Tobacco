import pandas as pd
from pandas import DataFrame


def read(*years) -> DataFrame:
    for year in years:
        if year < 1990 or year > 2019:
            raise Exception("The year is not true!")

    # smoker = pd.read_csv("GlobalSmoker/IHME_1990_2019_SMOKERS.CSV")
    smoker = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")

    smoker = smoker.loc[(smoker.sex_id == 3)]
    smoker = smoker.loc[(smoker.sex_name == "Both")]
    if len(years) == 1:
        smoker = smoker.loc[smoker.year_id == years]
    else:
        smoker = smoker.loc[smoker.year_id.isin(years)]

    # smoker = smoker.loc[:, ('location_name', 'year_id', 'val')]
    smoker = smoker.loc[:, ('location_name', 'val')]

    # print(smoker.head())
    return smoker


if __name__ == "__main__":
    smokers = read(2010)
    smokers = smokers.to_json()
    print(smokers)
