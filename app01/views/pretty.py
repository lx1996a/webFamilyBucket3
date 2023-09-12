from django.shortcuts import render,redirect
from app01.models import PrettyNum
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyNumModelForm,PrettyModelForm


def pretty_list(request):

    search_data = request.GET.get("search_m","")
    data_dict = {}
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 列表数据排序,按级别降序排序
    data_list = PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_obj = Pagination(request,data_list,page_size=1)
    context = {
        "data_list": page_obj.page_queryset,
        "search_data": search_data,
        "page_string": page_obj.html(),
    }
    return render(request,'pretty_list.html',context)



def pretty_add(request):
    if request.method == 'GET':
        form = PrettyNumModelForm()
        return render(request,'pretty_add.html',{"form":form})
    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request,'pretty_add.html',{"form":form})

def pretty_delete(request,nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")



def pretty_edit(request,nid):
    obj = PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyModelForm(instance=obj)
        return render(request,'pretty_add.html',{"form":form})
    form = PrettyModelForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request,'pretty_add.html',{"form":form})





