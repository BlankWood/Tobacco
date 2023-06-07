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
    :param year: 年份
    :return: 列表, 元素为字典, [{name: , value: }]
    """
    return readF.read(year)


@app.route('/dist_<int:year>')
def get_dist(year):
    """
    根据年份返回特定地区的吸烟人数数据, 地区在 readFile 中设置
    :param year:
    :return:
    """
    return readF.read(year, Global=False)


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
    result = readF.read(years, Global=False)
    return result


if __name__ == "__main__":
    app.run()


