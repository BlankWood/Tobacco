import pandas as pd

# 地区ID
district_id = [5, 9, 31, 64, 103, 137, 158, 166]
# district_name = ["East Asia", "Southeast Asia", "Central Europe, Eastern Europe, and Central Asia", "High-income",
#                  "Latin America and Caribbean", "North Africa and Middle East", "South Asia", "Sub-Saharan Africa"]
# 缩小倍数
shrink = 1000


def read(*years, Global=True):
    # 年份判断, 超出范围则抛出异常
    for year in years:
        if year < 1990 or year > 2019:
            raise Exception("The year is not true!")

    # 读文件
    smoker = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")

    # 通用筛选
    smoker = smoker.loc[(smoker.sex_id == 3)]
    smoker = smoker.loc[(smoker.sex_name == "Both")]

    # 地区筛选: 各国或地区
    if not Global:
        smoker = smoker.loc[smoker.location_id.isin(district_id)]

    # 年份筛选 并切出特定列
    if len(years) == 1:
        smoker = smoker.loc[smoker.year_id == years]
        smoker = smoker.loc[:, ('location_name', 'val')]
        smoker.columns = ['name', 'value']
    else:
        smoker = smoker.loc[smoker.year_id.isin(years)]
        smoker = smoker.loc[:, ('location_name', 'year_id', 'val')]
        smoker.columns = ['name', 'year', 'value']

    # 数值缩小
    smoker['value'] = smoker.value.map(lambda x: int(x / shrink))

    # 转为数组 [{},{},...]
    smoker = smoker.to_dict(orient='records')

    return smoker


if __name__ == "__main__":
    smokers = read(2010)
    # smokers = smokers.to_json()
    print(smokers)
