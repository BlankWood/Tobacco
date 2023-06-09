# 全球吸烟情况分析与可视化展示

import requests
import pandas as pd


def crawl_pct(year=0):
    """
    爬取特定年份的吸烟率信息, 如果为 0, 则爬取 2010-2016.
    :param year: 年份
    :return: 吸烟率列表
    """

    url = 'https://vizhub.healthdata.org/tobacco/php/getOverviewData.php'
    payload = {'year': '2015',
                'age': '22',
                'sex': '3',
                'metric': 'prevalence',
                'metric2': 'prevalence',
                'cache': 'false'
               }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        return "请求出错"

    data = response.json()['data']['model']

    data_list = []
    world_map = crawl_map()

    for key in data.keys():
        years = data[key]
        data_dict = {'name': world_map[key]}
        if year == 0:
            for year in range(2010, 2016):
                mean = years[str(year)]['22']['3']['prevalence']['pct']['mean']
                data_dict['value'] = mean
        else:
            mean = years[str(year)]['22']['3']['prevalence']['pct']['mean']
            data_dict['value'] = mean

        data_list.append(data_dict)

    return data_list


def crawl_map():
    """
    爬取 地区id 与 地区名字 对应关系
    :return:
    """
    map_url = 'https://vizhub.healthdata.org/tobacco/php/locationsMap.php'
    world_map = requests.get(url=map_url).json()['data']
    return world_map


def crawl(year=2010):
    """
    根据年份爬取吸烟人数数据
    :param year: 年份
    :return: 吸烟人数数量的列表
    """

    # 数据请求 url 和 headers.
    data_url = "https://vizhub.healthdata.org/tobacco/php/getYearData.php"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37 '
    }

    # post 请求需要填写的参数
    payload = {'age': '22', 'sex': '3', 'metric': 'prevalence', 'unit': 'num', 'year': str(year), 'cache': 'false'}

    # post请求
    response = requests.post(data_url, headers=header, data=payload)

    # 根据数据的 key值提取有效数据
    # 转json并提取部分数据
    data = response.json()['data']['model']
    data_list = []

    # 进一步提取数据
    for i in data.keys():
        mean = data[i]['2010']['22']['3']['prevalence']['num']
        # item = [world_map[i], mean['mean'], mean['lower'], mean['upper']]
        data_dict = {'name': i, 'value': int(mean['mean'])}
        data_list.append(data_dict)

    return data_list


def to_df(data: list):
    df = pd.DataFrame(data)
    return df


def print_format(data):
    for item in data:
        print("{name: '"+item['name']+"', value: "+str(item['value'])+"},")


def save(data):
    data = pd.DataFrame(data)
    data.to_csv('global_pct.csv')


if __name__ == "__main__":
    # 启动程序 main()
    # map_id = crawl_map()
    # print(map_id)
    # save(crawl_pct(2015))

    for year in range(2000, 2020):
        for i in crawl_pct(year):
            if i['name'] == 'Global':
                print(i['value'])
