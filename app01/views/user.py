from django.shortcuts import render,redirect
from app01.models import Department,UserInfo
from app01.utils.form import UserModelForm,UserInfoModelForm


def user_list(request):
    queryset = UserInfo.objects.all()
    return render(request,"user_list.html",{"queryset":queryset})

def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choices":UserInfo.gender_choices,
            "depart_list":Department.objects.all(),
        }
        return render(request,"user_add.html",context)

    username = request.POST.get("username")
    password = request.POST.get("password")
    age = request.POST.get("age")
    acount = request.POST.get("acount")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    depart = request.POST.get("depart")
    UserInfo.objects.create(name=username,password=password,age=age,acount=acount,create_time=create_time,gender=gender,depart_id=depart)
    return redirect("/user/list/")


""" 用户添加 """
def user_model_form_add(request):

    if request.method == 'GET':
        userInfoModelForm = UserInfoModelForm()
        return render(request,'user_model_form_add.html',{"form":userInfoModelForm})

    # POST获取数据和校验  data=request.POST
    form = UserInfoModelForm(data=request.POST)
    # 数据校验
    if form.is_valid():
        # 打印表单数据
        print(form.cleaned_data)
        # 将用户信息保存到数据库中
        form.save()
        return redirect("/user/list/")

    #数据校验失败
    print(form.errors)
    return render(request,'user_model_form_add.html',{"form":form})

def user_delete(request,nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


""" 编辑用户 """
def user_edit(request,nid):

    userObj = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据 (对象)
        form = UserModelForm(instance=userObj)
        return render(request,"user_edit.html",{"form":form})

    # instance=userObj
    form = UserModelForm(data=request.POST,instance=userObj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加额外的值
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list/")
    # 数据校验失败
    return render(request,"user_edit.html",{"form":form})




