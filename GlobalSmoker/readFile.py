import numpy
import pandas as pd

# 地区ID
district_id = [5, 9, 31, 64, 103, 137, 158, 166]
# district_name = ["East Asia", "Southeast Asia", "Central Europe, Eastern Europe, and Central Asia", "High-income",
#                  "Latin America and Caribbean", "North Africa and Middle East", "South Asia", "Sub-Saharan Africa"]

Asia_name = ["China", "Indonesia", "Japan", "India", "Singapore", "Russian Federation", 'Singapore']
Europe_name = ["France", 'Germany', 'United Kingdom', 'Denmark', 'Finland', 'Norway', 'Netherlands', 'Greenland']
North_America = ['Canada', 'United States of America', 'Mexico']
South_America = ['Argentina', 'Chile', 'Brazil']
Africa_name = ['Egypt', 'Congo', 'Madagascar']

# 缩小倍数
shrink = 1000


def read(years, district="All"):
    """
    根据 '年份' 和 '地区' 筛选数据

    :param years: 年份: int. 为 0 则选取 1991-2019 的奇数年份
    :param district: 地区: str. 可选 "Asia", "Europe", "North America", "South America", "Africa"
    :return: 返回格式已根据需求进行自动更改.
    """

    # 读文件
    smoker = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")

    # 通用筛选
    smoker = smoker.loc[(smoker.sex_id == 3) & (smoker.sex_name == "Both")]

    # 地区筛选: 各国或地区
    if district != "All":
        dist_name = []
        match district:
            case 'Asia':
                dist_name = Asia_name
            case 'Europe':
                dist_name = Europe_name
            case 'North America':
                dist_name = North_America
            case 'South America':
                dist_name = South_America
            case 'Africa':
                dist_name = Africa_name

        smoker = smoker.loc[smoker.location_name.isin(dist_name)]

    # 年份筛选 并切出特定列
    # if len(years) == 1 and years[0] != 0:
    #     smoker = smoker.loc[smoker.year_id == years]
    #     smoker = smoker.loc[:, ('location_name', 'val')]
    #     smoker.columns = ['name', 'value']
    # else:
    #     if years[0] != 0:
    #         smoker = smoker.loc[smoker.year_id.isin(years)]
    #     else:
    #         smoker = smoker.loc[smoker.year_id.isin(range(1991, 2020, 2))]
    #     smoker = smoker.loc[:, ('location_name', 'year_id', 'val')]
    #     smoker.columns = ['name', 'year', 'value']

    if years != 0:
        smoker = smoker.loc[smoker.year_id == years]
        smoker = smoker.loc[:, ('location_name', 'val')]
        smoker.columns = ['name', 'value']
    else:
        smoker = smoker.loc[smoker.year_id.isin(range(1991, 2020, 2))]
        smoker = smoker.loc[:, ('location_name', 'year_id', 'val')]
        smoker.columns = ['name', 'year', 'value']

    # 数值缩小 1/shrink
    smoker['value'] = smoker.value.map(lambda x: int(x / shrink))

    # 转为数组 [{},{},...]
    # if len(years) == 1 and years[0] != 0:
    #     smoker = smoker.to_dict(orient='records')
    # elif years[0] == 0:
    #     smoker = to_list(smoker)

    if years != 0:
        smoker = smoker.to_dict(orient='records')
    elif years == 0:
        smoker = to_list(smoker)

    return smoker


def to_list(data):
    data_list = list()
    columns = list(data.columns)
    data_list.append(columns)

    for index in data.index:
        temp = []
        for column in columns:
            elem = data[column][index]
            if type(elem) == numpy.int64:
                elem = int(elem)
            temp.append(elem)
        data_list.append(temp)

    return data_list


def get_global():

    data = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")
    data = data.loc[(data.sex_id == 3) & (data.location_name == 'Global') & (data.sex_name == "Both")]
    data = data.loc[:, "val"]
    data = list(data.map(lambda x: int(x / shrink)))
    return data


if __name__ == "__main__":
    # smokers = read([0], )
    # smokers = smokers.to_json()
    # print(smokers)

    print(read(0, district="Asia"))
