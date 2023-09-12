from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.models import UserInfo,PrettyNum
from .BootstrapModelForm import BootstrapModelForm


class UserInfoModelForm(BootstrapModelForm):
    # 自定义校验规则
    name = forms.CharField(min_length=3) #用户名最小字符串为3，小于三报错

    class Meta:
        model = UserInfo
        fields = ["name","password","age","acount","create_time","gender","depart"]


class UserModelForm(BootstrapModelForm):
    class Meta:
        model = UserInfo
        fields = ["name","password","age","acount","create_time","gender","depart"]



class PrettyNumModelForm(BootstrapModelForm):
    # 校验扩展方式一：手机号格式正则表达式校验
    mobile = forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误"),])
    class Meta:
        model = PrettyNum
        # 展示所有字段
        # fields = "__all__"
        # 展示指定字段
        fields = ["id","mobile","price","level","status"]
        # 排除指定字段
        # exclude = ["level"]

    # 校验扩展方式二：手机号不可重复
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            raise ValidationError("手机号格式错误")
        exists = PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

class PrettyModelForm(BootstrapModelForm):
    # 禁止编辑设置
    # mobile = forms.CharField(label="手机号",disabled=True)
    # 校验扩展方式一：手机号格式正则表达式校验
    mobile = forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误"),])
    class Meta:
        model = PrettyNum
        # 展示所有字段
        # fields = "__all__"
        # 展示指定字段
        fields = ["id","mobile","price","level","status"]
        # 排除指定字段
        # exclude = ["level"]

    # 校验扩展方式二：手机号不可重复
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            raise ValidationError("手机号格式错误")
        # 获取当前编辑行的ID
        txt_id = self.instance.pk
        exists = PrettyNum.objects.exclude(id=txt_id).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile
















