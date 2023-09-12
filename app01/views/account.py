from django import forms
from django.shortcuts import render, redirect, HttpResponse

from app01.utils.BootstrapModelForm import BootstrapModelForm
from app01.utils.encryp import md5
from app01 import models


class LoginModelForm(BootstrapModelForm):
    # 参数中 required = True 表示不可为空，默认为True
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    class Meta:
        model = models.Admin
        fields = ["name", "password", "code"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


def login(request):
    if request.method == "GET":
        form = LoginModelForm()
        return render(request, "login.html", {"form": form})

    form = LoginModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data) # {'name': 'lx', 'password': 'd7518f15576f31d1347025dc176a1348', 'code': 'CZTCV'}
        # 校验用户验证码
        input_code = form.cleaned_data.pop("code")
        code = request.session.get("code")
        if code.upper() != input_code.upper():
            form.add_error("code", "验证码输入错误！")
            return render(request, "login.html", {"form": form
                                                  })
        # print(form.cleaned_data) # {'name': 'lx', 'password': 'd7518f15576f31d1347025dc176a1348'}
        data_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not data_obj:
            form.add_error("password", "用户名或密码错误！")
            return render(request, "login.html", {"form": form})
        # 网站生成随机字符串；写到用户浏览器的cookie中，再写入到session中
        request.session["info"] = {"id": data_obj.id, "name": data_obj.name}
        # 设置session有效期 7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")
    return render(request, "login.html", {"form": form})


from io import BytesIO
from app01.utils.code import check_code

def image_code(request):
    # 获取验证码图片和内容
    img, code_str = check_code()
    # print(code_str)
    # 保存正确的验证码
    request.session["code"] = code_str
    # 设置session有效期 60 秒
    request.session.set_expiry(60)
    # 将图片报错到内存中
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect("/login/")
