# 全球吸烟情况分析与可视化展示

import requests
import pandas as pd


def crawl_pct():
    url = 'https://vizhub.healthdata.org/tobacco/php/getOverviewData.php'
    payload = {'year': '2015',
                'age': '22',
                'sex': '3',
                'metric': 'prevalence',
                'metric2': 'prevalence',
                'cache': 'false'
               }

    headers = {

    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        return "请求出错"

    data = response.json()['data']['model']

    data_list = []

    for key in data.keys():
        years = data[key]
        data_dict = {'name': key}
        for year in range(2010, 2016):
            mean = years[str(year)]['22']['3']['prevalence']['pct']['mean']
            data_dict[str(year)] = mean

        data_list.append(data_dict)

    return data_list


def crawl_map():
    map_url = 'https://vizhub.healthdata.org/tobacco/php/locationsMap.php'
    world_map = requests.get(url=map_url).json()['data']
    return world_map


def crawl(year=2010):

    data_url = "https://vizhub.healthdata.org/tobacco/php/getYearData.php"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37 '
    }
    payload = {'age': '22', 'sex': '3', 'metric': 'prevalence', 'unit': 'num', 'year': str(year), 'cache': 'false'}

    response = requests.post(data_url, headers=header, data=payload)

    data = response.json()['data']['model']
    data_list = []
    # name = ['Samoa', 'Ukraine', 'Vietnam', 'New Zealand', 'Mexico', 'United States', 'Panama', 'Australia']

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


if __name__ == "__main__":
    map_id = crawl_map()
    print(map)
