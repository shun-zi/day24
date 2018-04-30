from django.shortcuts import render, HttpResponse, redirect
from django.forms import ModelForm
from django.forms import Form, fields as field, widgets as widget
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from blog import models
from utils.check_code import create_validate_code
import json

# Create your views here.
class AccountModelForm(ModelForm):
    pwd_again = field.CharField(max_length=16, required=True, min_length=6,
                                widget=widget.PasswordInput(attrs={'placeholder': '请重新输入密码', "id": "pwd_again"}))
    verification_code = field.CharField(widget=widget.TextInput(attrs={"placeholder": "请输入验证码","id": "code", "style": "width: 143px"}))
    class Meta:
        model = models.Account
        fields = ["username", "password"]
        widgets = {
            'username': widget.EmailInput(attrs={"placeholder": "请输入邮箱地址", "id": "username"}),
            'password': widget.PasswordInput(attrs={"placeholder": "请输入密码", "minlength": 6, "id": "password"}),
        }

def auth(func):
    def inner(request):
        username = request.session.get("username", None)
        if username is None:
            return redirect("/login/")
        return func(request)
    return inner

@csrf_exempt
def index(request):
    if request.method == "GET":
        username = request.session.get("username", None)
        return render(request, "index.html", {"username": username})
    elif request.method == "POST":
        op = request.POST.get("operation", None)
        if op == "logout":
            del request.session["username"]
            return render(request, "index.html", {"username": None})


def register(request):
    if request.method == "GET":
        account_obj = AccountModelForm()
        return  render(request, "register.html", {"form": account_obj})
    elif request.method == "POST":
        deal_dict = {"code": True, "status": True}
        mf_obj = AccountModelForm(request.POST)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        code = request.POST.get("verification_code", None)
        if code.upper() == request.session["CheckCode"].upper():
            account_obj = models.Account.objects.filter(username=username)
            if len(account_obj) == 0:
                if mf_obj.is_valid():
                    mf_obj.save()
                    request.session["username"]=username
            else:
                # 用户名已经存在
                deal_dict["status"] = False
        else:
            deal_dict["code"] = False
        return HttpResponse(json.dumps(deal_dict))

def login(request):
    if request.method == "GET":
        account_obj = AccountModelForm()
        return render(request, "login.html", {"form": account_obj})
    elif request.method == "POST":
        deal_dict = {"code": True, "status": True}
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        code = request.POST.get("verification_code", None)
        if code.upper() == request.session["CheckCode"].upper():
            account_obj = models.Account.objects.filter(username=username, password=password)

            if len(account_obj) == 0:
                deal_dict["status"] = False
            else:
                request.session["username"] = username
        else:
            deal_dict["code"] = False
        return HttpResponse(json.dumps(deal_dict))

def verification_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

