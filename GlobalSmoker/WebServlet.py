import readFile as readF
from flask import Flask, render_template, request

app = Flask(__name__)

html_name = "test.html"


@app.route('/')
def main_html():
    """
    flask 启动页面
    :return: html_name 为主页面的名字, 在上方全局变量中设置
    """
    return render_template(html_name)


@app.route('/map_<int:year>')
def get_global(year):
    """
    根据年份返回全部的地区吸烟人数数据
    :param year: 年份. 为 0 ,则取 1991-2019 的奇数年份.
    :return: 列表, 元素为字典, [{name: , value: }]
    """
    data = readF.read(year, "All")
    return data


@app.route('/region_<region>')
def get_region(region):
    """
    返回特定地区的吸烟人数数据, 为 1991-2019 的奇数年份.
    :param region: 地区, 在 readFile 中设置
    :return:
    """
    data = readF.read(0, district=region)
    return data


@app.route('/plot', methods=["POST"])
def get_plot():
    """
    $("#getData").click(function () {
        var requestData = { numbers: [1, 2, 3, 4, 5] };

        // 发送 AJAX 请求
        $.ajax({
          method: "POST",
          url: "/api/v1/data",
          contentType: "application/json",
          data: JSON.stringify(requestData),
        })
          .done(function (response) {
            $("#result").text(`结果：${response.result}`);
          })
          .fail(function () {
            alert("请求失败!");
          });
      });

    通过 post 获取需要的年份, 返回对应年份特定地区的数据
    :return:
    """
    data = request.json
    years = data.get("years", [])
    result = readF.read(years)
    return result


@app.route('/test')
def test():
    # return [{'color': 'blue', 'num': 10}, {'color': 'red', 'num': 20}]
    return [['color', 'num'], ['blue', 10], ['red', 20]]


if __name__ == "__main__":
    # 当 debug=True 时, 不用重新启动, 只需保存, 即可在页面中运行修改后的代码
    app.run(debug=True)
    # print(get_region("Asia"))

