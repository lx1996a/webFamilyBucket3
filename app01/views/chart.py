from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    return render(request, 'chart_list.html')


""" 构造柱状图数据 """


def chart_bar(request):
    # 从数据库中获取数据
    legend_data = ['销售1', '销售2']
    xAxis_data = ["1月份", "2月份", "3月份", "4月份", "5月份", "6月份"]
    series = [{"name": '销售1', "type": 'bar', "data": [5, 20, 36, 10, 10, 20]},
              {"name": '销售2', "type": 'bar', "data": [15, 30, 26, 40, 60, 30]}]
    result = {
        "status": True,
        "data": {"legend_data": legend_data,
                 "xAxis_data": xAxis_data,
                 "series": series, }
    }
    return JsonResponse(result)


""" 构造饼图数据 """


def chart_pie(request):
    data_list = [
        {"value": 1335, "name": 'IT部门'},
        {"value": 2310, "name": '新媒体'},
        {"value": 234, "name": '运营'},
    ]
    result = {
        "status": True,
        "data": {"data_list": data_list, }
    }
    return JsonResponse(result)


""" 构造折线图数据 """


def chart_line(request):
    legend_data = ['邮件营销', '联盟广告']
    xAxis_data = ["1月份", "2月份", "3月份", "4月份", "5月份", "6月份", "7月份"]
    series = [{"name": '邮件营销',"type": 'line',"stack": '总量', "data": [120, 132, 101, 134, 90, 230, 210]},
              { "name": '联盟广告', "type": 'line', "stack": '总量',"data": [220, 182, 191, 234, 290, 330, 310]}]
    result = {
        "status": True,
        "data": {"legend_data": legend_data,
                 "xAxis_data": xAxis_data,
                 "series": series, }
    }
    return JsonResponse(result)


def highcharts(request):
    return render(request,"chart_highcharts.html")