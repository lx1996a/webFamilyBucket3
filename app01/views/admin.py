from django.shortcuts import render, redirect,HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.BootstrapModelForm import BootstrapModelForm
from app01.utils.encryp import md5


def admin_list(request):
    # info = request.session.get("info")
    # print(info)
    # if not info:
    #     return redirect("/login/")

    search_data = request.GET.get("search_m")
    filter_dict = {}
    if search_data:
        filter_dict["name__contains"] = search_data

    data_list = models.Admin.objects.filter(**filter_dict)

    page_obj = Pagination(request, queryset=data_list)

    context = {
        "data_list": page_obj.page_queryset,
        "search_data": search_data,
        "page_string": page_obj.html(),
    }
    return render(request, "admin_list.html", context)

class AdminModelForm(BootstrapModelForm):
    # 密码和确认密码不明文展示，设置为密码框 即:widget=forms.PasswordInput
    # 当密码与确认密码不一致的时候，数据会清空，若不想数据清空，可设置widget=forms.PasswordInput(render_value=True)
    confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["name", "password", "confirm"]
        widgets = {
            # "name": forms.CharField(label="账户",max_length=32,validators=[RegexValidator(r'^1[3-9]\d{9}$'),"账户名称格式错误"]),
            "password": forms.PasswordInput(render_value=True,attrs={"style": "background-color: #4cae4c"}),
        }

    # 密码加密存储
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

    # 校验密码和确认密码是否一致
    def clean_confirm(self):
        password = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm"))
        if confirm != password:
            raise ValidationError("确认密码与密码不一致！")
        return confirm


def admin_add(request):
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, "change.html", context)
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title,"form": form })

class AdminModelForm2(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["name"]

def admin_edit(request,nid):
    title = "编辑管理员"
    data_obj = models.Admin.objects.filter(id=nid).first()
    if not data_obj:
        msg = "数据不存在"
        return render(request,"error.html",{"msg":msg})
    if request.method == "GET":
        form = AdminModelForm2(instance=data_obj)
        return render(request,"change.html",{"form":form,"title":title})
    form = AdminModelForm2(data=request.POST,instance=data_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request,nid):
    models.Admin.objects.filter(id = nid).delete()
    return redirect("/admin/list")

class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }
    # 校验当前密码与原密码是否一致，若是，则报错
    def clean_password(self):
        pwd = md5(self.cleaned_data.get("password"))
        exists = models.Admin.objects.filter(id=self.instance.pk,password=pwd).exists()
        if exists:
            raise ValidationError("当前密码与原密码一致，请修改！")
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        if confirm_pwd != pwd:
            raise ValidationError("确认密码与密码不一致！")
        return confirm_pwd

def admin_reset(request,nid):
    title = "重置密码"
    data_obj = models.Admin.objects.filter(id=nid).first()
    if not data_obj:
        return render(request,"error.html",{"msg":"数据不存在"})
    if request.method == "GET":
        # form = AdminResetModelForm(instance=data_obj)
        form = AdminResetModelForm()
        return render(request,"change.html",{"form":form,"title":title})
    form = AdminResetModelForm(data=request.POST,instance=data_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,"change.html",{"form":form,"title":title})


