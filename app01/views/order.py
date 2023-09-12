import random
from datetime import datetime

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination

class MyModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }

class OrderModelForm(MyModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid","user"]


def order_list(request):

    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    context = {
        "form":form,
        "data_list": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request,'order_list.html',context)

@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data) # {'title': '纸巾', 'price': 43, 'status': 1, 'user': <Admin: lx>}
        # 额外增加一些不是用户输入的值 form.instance.XXX = xxxxxxxxx
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000,9999))
        form.instance.user_id = request.session["info"]["id"]
        # 保存到数据库中
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,"error":form.errors})


def order_delete(request):
    # print(request.GET) # <QueryDict: {'nid': ['1']}>
    nid = request.GET.get("nid")
    # 判断删除对象是否存在
    exists = models.Order.objects.filter(id=nid).exists()
    if not exists:
        return JsonResponse({"status":False,"error":"删除失败，数据不存在！"})
    models.Order.objects.filter(id=nid).delete()
    return JsonResponse({"status":True})

def order_detail(request):
    nid = request.GET.get("nid")
    # 获取数据字典
    data_dict = models.Order.objects.filter(id=nid).values("title","price","status").first()
    if not data_dict:
        return JsonResponse({"status":False,"error":"数据不存在！"})
    result = {
        "status": True,
        "data": data_dict,
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    nid = request.GET.get("nid")
    row_obj = models.Order.objects.filter(id=nid).first()
    if not row_obj:
        return JsonResponse({"status":False,"tips":"数据不存在，请刷新页面重试！"})
    form = OrderModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,"error":form.errors})











