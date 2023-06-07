import fromFile as fFile
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("test.html")


@app.route('/<int:year>')
def request_year(year):
    return "response: "+str(year)


@app.route('/map_<int:year>')
def smokers(year):
    data = fFile.read(year)

    developed = ['United States', 'United Kingdom', 'Japan', 'Korea', 'Canada', 'Australia', 'New Zealand', 'France', 'Germany', 'Italy', 'Spain', 'Austria', 'Belgium', 'Ireland', 'Norway', 'Sweden', 'Finland', 'Denmark', 'Iceland', 'Switzerland', 'Luxembourg', 'Netherlands', 'Greece', 'Czech Republic', 'Hungary', 'Slovakia', 'Andorra', 'Israel', 'Estonia', 'Cyprus', 'Liechtenstein', 'Malta', 'Slovenia', 'Singapore', 'United Arab Emirates', 'Bahrain', 'Qatar', 'Brunei']

    data.columns = ['name', 'value']
    # print(data.keys())

    for i in data.index:
        # print(data['location_name'][i])
        # data_dict = {'name': data['location_name'][i], 'value': "{:.2} K".format(data['val'][i]/1000)}
        # data.loc[i, 'value'] = "{:.2} K".format(data['value'][i]/1000)
        data.loc[i, 'value'] = int(data['value'][i]/1000)

    # return data.to_json('../Data/somker.json', orient='records')
    return data.to_json(orient='records')


if __name__ == "__main__":
    app.run()


