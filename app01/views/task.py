import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models

class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}


class TaskModelForm(MyModelForm):
    class Meta:
        model = models.task
        fields = "__all__"
        widgets = {
            # "datail":forms.Textarea,
            "datail":forms.TextInput,
        }


def task_list(request):
    form = TaskModelForm()
    return render(request, "task_list.html", {"form": form})


@csrf_exempt
def task_ajax(request):
    print(request.POST)  # <QueryDict: {'username': ['root'], 'age': ['34'], 'email': ['asda'], 'more': ['asdas']}>
    data = {
        "n1": "haha",
        "n2": [1, 2, "er", 90]
    }
    # return HttpResponse(json.dumps(data))
    return JsonResponse(data)

@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"stutas":True}
        return JsonResponse(data_dict)
    print(form.errors)
    print(form.errors.as_json())
    data_dict = {"stutas":False,"error":form.errors}
    return HttpResponse(json.dumps(data_dict,ensure_ascii=False))