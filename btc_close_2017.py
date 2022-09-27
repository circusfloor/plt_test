import json
import pygal
import math
from itertools import  groupby
import requests

# json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# req = requests.get(json_url)
# # 写入文件
# with open('btc_close_2017.json', 'w') as f:
#     f.write(req.text)
# file_requests = req.json()


filename = 'btc_close_2017.json'
with open(filename) as f:
    btc_data = json.load(f)

# 创建5个列表，分别存储日期和收盘价
dates = []
months = []
weeks = []
weekdays = []
close = []
# 每一天的信息
for btc_dict in btc_data:
    dates.append(btc_dict['date'])
    months.append(int(btc_dict['month']))
    weeks.append(int(btc_dict['week']))
    weekdays.append(btc_dict['weekday'])
    close.append(int(float(btc_dict['close'])))

line_chart = pygal.Line(x_labe_rotation=20, show_minor_x_labels=False)
line_chart.title = '收盘价（￥）'
line_chart.x_labels = dates
N = 20
line_chart.x_labels_major = dates[::N]
close_log = [math.log10(_) for _ in close]
line_chart.add('log收盘价', close_log)
line_chart.render_to_file('收盘价折线图（￥）.svg')


def draw_line(x_data, y_data, title, y_legend):
    xy_map = []
    for x, y in groupby(sorted(zip(x_data, y_data)), key=lambda _: _[0]):
        y_list = [v for _, v in y]
        xy_map.append([x, sum(y_list) / len(y_list)])
    x_unique, y_mean = [*zip(*xy_map)]
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_unique
    line_chart.add(y_legend, y_mean)
    line_chart.render_to_file(title + '.svg')
    return line_chart


idx_month = dates.index('2017-12-01')
line_chart_month = draw_line(months[:idx_month], close[:idx_month], '收盘价月日均值（￥）', '月日均值')
line_chart_month

idx_week= dates.index('2017-12-11')
line_chart_week = draw_line(weeks[1:idx_week], close[1:idx_week], '收盘价周日均值（￥）', '周日均值')
line_chart_week

with open('收盘价dashboard.html', 'w', encoding='utf8') as html_file:
    html_file.write('<html><head><title>收盘价Dashboard</title><metacharset="utf-8"></head><body>\n')
    for svg in ['收盘价折线图（￥）.svg', '收盘价周日均值（￥）.svg', '收盘价月日均值（￥）.svg']:
        html_file.write('   <object type="image/svg+xml"data="{0}"height=500></object>\n'.format(svg))
    html_file.write('</body></html>')
