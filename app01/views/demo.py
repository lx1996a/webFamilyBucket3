from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.BootstrapModelForm import BootstrapModelForm
from app01.utils.encryp import md5



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







