import os
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.conf import settings

from app01 import models


def one_file(request):
    if request.method == "GET":
        return render(request,"upload_one.html")
    print(request.POST)
    print(request.FILES)
    file_obj = request.FILES.get("avatar")
    print(file_obj.name)
    f = open(file_obj.name,mode="wb")
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("......")

class BootStrap:
    bootstrap_enclude_field = []

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            if name in self.bootstrap_enclude_field:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class":"form-control","placeholder":field.label}

class BootStrapForm(BootStrap,forms.Form):
    pass

class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass

class UpForm(BootStrapForm):
    bootstrap_enclude_field = ["imgs"]
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    imgs = forms.FileField(label="头像")

def upload_form(request):
    title = "form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request,'upload_form.html',{"title":title,"form":form})
    form = UpForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        # {'name': 'lxx', 'age': 29, 'imgs': < InMemoryUploadedFile: 1.jpg(image / jpeg) >}
        # print(form.cleaned_data)
        file = form.cleaned_data.get("imgs")
        # print(file.name) # 1.jpg
        # 文件在数据库中存储的路径
        # save_path = os.path.join("static","imags",file.name)
        # 文件在项目中存放的路径
        # abs_path = os.path.join("app01",save_path)
        media_path = os.path.join("media",file.name)
        file_obj = open(media_path,mode="wb")
        for chunk in file.chunks():
            file_obj.write(chunk)
        file_obj.close()
        models.Boss.objects.create(
            name = form.cleaned_data.get("name"),
            age = form.cleaned_data["age"],
            imgs= media_path
        )
        return HttpResponse("......")

    return render(request, 'upload_form.html', {"title": title, "form": form})

class UpModelForm(BootStrapModelForm):
    bootstrap_enclude_field = ["imgs"]
    class Meta:
        model = models.City
        fields = "__all__"

def upload_modelform(request):
    title = "modelform上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request,'upload_form.html',{"form":form, "title":title})
    form = UpModelForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        # 文件保存在下指定路径下，文件路径保存在数据库中
        form.save()
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, "title": title})

