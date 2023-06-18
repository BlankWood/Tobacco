import numpy
import pandas as pd

# 地区ID
district_id = [5, 9, 31, 64, 103, 137, 158, 166]
# district_name = ["East Asia", "Southeast Asia", "Central Europe, Eastern Europe, and Central Asia", "High-income",
#                  "Latin America and Caribbean", "North Africa and Middle East", "South Asia", "Sub-Saharan Africa"]

Asia_name = ["China", "Indonesia", "Japan", "India", "Singapore", "Russia"]
Europe_name = ["France", 'Germany', 'United Kingdom', 'Denmark', 'Finland', 'Netherlands']
North_America = ['Canada', 'Mexico', 'United States', 'El Salvador', 'Panama', 'Greenland']
South_America = ['Argentina', 'Chile', 'Brazil', 'Bolivia (Plurinational State of)', 'Paraguay', 'Uruguay']
Africa_name = ['Egypt', 'Congo', 'Madagascar', 'Morocco', 'Zambia', 'South Africa']

colors = ['#fc8251', '#5470c6', '#91cd77', '#ef6567', '#f9c956', '#75bedc']
# itemStyle

# 缩小倍数
shrink = 1000


def get_region(region):
    dist_name = []
    match region:
        case 'Asia':
            dist_name = Asia_name
        case 'Europe':
            dist_name = Europe_name
        case 'North-America':
            dist_name = North_America
        case 'South-America':
            dist_name = South_America
        case 'Africa':
            dist_name = Africa_name

    return dist_name


def read(year=0, region="All"):
    """
    根据 '年份' 和 '地区' 筛选数据
    :param year: 年份: int. 为 0 则选取 1991-2019 的奇数年份
    :param region: 地区: str. 可选 "Asia", "Europe", "North America", "South America", "Africa"
    :return: 返回格式已根据需求进行自动更改.
    """

    # 读文件
    smoker = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")

    # 通用筛选
    smoker = smoker.loc[(smoker.sex_id == 3)]

    # 地区筛选: 各国或地区
    if region != "All":
        dist_name = get_region(region)
        smoker = smoker.loc[smoker.location_name.isin(dist_name)]

    # 年份筛选 并切出特定列
    if year != 0:
        smoker = smoker.loc[smoker.year_id == year]
        smoker = smoker.loc[:, ('location_name', 'val')]
        smoker.columns = ['name', 'value']
    else:
        smoker = smoker.loc[smoker.year_id.isin(range(1991, 2020, 2))]
        smoker = smoker.loc[:, ('location_name', 'year_id', 'val')]
        smoker.columns = ['name', 'year', 'value']

    # 数值缩小 1/shrink
    smoker['value'] = smoker.value.map(lambda x: int(x / shrink))

    if year != 0:
        smoker = smoker.to_dict(orient='records')
    elif year == 0:
        smoker = to_list(smoker)

    return smoker


def get_pct():
    pct = pd.read_csv("global_pct.csv")
    pct = pct.loc[:, ('name', 'value')]
    pct.value = pct.value.map(lambda x: x * 100)
    pct = pct.to_dict(orient='records')
    return pct


def to_list(data):
    # 将数据转为特定格式的 list.

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


def get_color(data):
    index = 0
    for i in data:
        i['itemStyle'] = {'color': colors[index]}
        index += 1

    return data


def get_global(is_shrink=True):

    data = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")
    data = data.loc[(data.sex_id == 3) & (data.location_name == 'Global') & (data.sex_name == "Both")]
    data = data.loc[:, "val"]
    if is_shrink:
        data = data.map(lambda x: int(x / shrink))
    data = list(data)
    return data


def sort_gender(year):
    """
    根据年份返回对应的男女吸烟人数
    :param year:
    :return:
    """
    data = pd.read_csv("IHME_1990_2019_SMOKERS.CSV")
    data = data.loc[(data.sex_name.isin(['Male', 'Female'])) & (data.location_name == 'Global') & (data.year_id == year)]
    data = data.loc[:, ('sex_name', 'val')]
    data['val'] = data.val.map(lambda x: int(x / shrink))
    data.columns = ['name', 'value']
    return data.to_dict(orient='records')


if __name__ == "__main__":
    # smokers = read(year=2019, region="All")
    # smokers = smokers.to_json()
    # for i in smokers:
    #     print(i)

    # d = read(2019, region="Asia")
    # d = get_color(d)
    # print(d)

    # for year in range(2010, 2020):
    #     print(sort_gender(year))

    data_global = get_global()
    data_global_ = get_global(False)
    for i in range(0, len(data_global)):
        print("处理前:", data_global_[i], "处理后:", data_global[i])

    # print(get_pct())



